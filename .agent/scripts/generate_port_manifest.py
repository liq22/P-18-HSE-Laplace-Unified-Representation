#!/usr/bin/env python3
"""Generate .agent/skills/PORT_MANIFEST.yaml from canonical skills.

Reproducible provenance manifest: merges a hardcoded tier/category/known-issue map
with filesystem-derived facts (bundled subdirs, env vars, frontmatter description).
Re-run after adding/removing ported skills to keep the manifest in sync.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / ".agent" / "skills"
OUT = SKILLS_DIR / "PORT_MANIFEST.yaml"

UPSTREAM_REPO = "https://github.com/K-Dense-AI/scientific-agent-skills"
UPSTREAM_REF = "v2.53.0"
UPSTREAM_COMMIT = (ROOT / ".agent" / "references" / "scientific_agent_skills_upstream_commit.txt").read_text().splitlines()[0].strip() if (ROOT / ".agent" / "references" / "scientific_agent_skills_upstream_commit.txt").exists() else "9c9bd2e92af12311ecd0c1a643e0931643f9ea04"
PORT_DATE = "2026-07-02"

# tier -> {skill: category}
TIERS = {
    "core": {
        "scientific-writing": "writing", "literature-review": "literature", "peer-review": "review",
        "citation-management": "citation", "venue-templates": "venue", "scientific-critical-thinking": "review",
        "hypothesis-generation": "methodology", "scientific-brainstorming": "methodology",
        "experimental-design": "methodology", "scientific-visualization": "viz", "matplotlib": "viz",
        "statistical-analysis": "statistics", "statistical-power": "statistics",
        "exploratory-data-analysis": "statistics", "scikit-learn": "ml", "shap": "ml",
        "pdf": "docs", "docx": "docs", "xlsx": "docs", "pptx": "docs",
        "markdown-mermaid-writing": "communication", "scientific-slides": "communication", "scientific-schematics": "viz",
    },
    "tool": {
        "seaborn": "viz", "statsmodels": "statistics", "networkx": "data", "polars": "data", "dask": "data",
        "pymc": "ml", "umap-learn": "ml", "pytorch-lightning": "ml", "torch-geometric": "ml",
        "transformers": "ml", "stable-baselines3": "ml", "timesfm-forecasting": "ml",
        "markitdown": "docs", "liteparse": "docs", "open-notebook": "communication",
    },
    "external": {
        "paper-lookup": "literature", "research-lookup": "literature", "bgpt-paper-search": "literature",
        "scholar-evaluation": "review", "pyzotero": "citation", "generate-image": "viz",
        "research-grants": "grants", "latex-posters": "communication", "pptx-posters": "communication",
        "infographics": "communication",
    },
}

KNOWN_ISSUES = {
    "bgpt-paper-search": ["Upstream allowed-tools vs MCP-search workflow mismatch; local Boundaries notes the caution."],
    "pptx-posters": ["Upstream export checklist incomplete; local Boundaries instructs user to verify the export checklist."],
    "generate-image": ["Restricted to conceptual/illustrative/outreach visuals; data/quantitative/evidence figures forbidden (route via scientific-visualization)."],
    "scientific-writing": ["Upstream mandates AI-generated figures via OPENROUTER-keyed scripts; scripts/ excluded, figure work delegated to figure/schematic skills."],
}

ENV_RE = re.compile(r"\b[A-Z][A-Z0-9_]{2,}_(?:API_KEY|KEY|TOKEN|SECRET)\b")
PLACEHOLDER_PREFIXES = ("YOUR_", "MY_", "EXAMPLE_", "EXAMPLES_", "REPLACE_", "TEST_", "FOO_", "BAR_", "XXX", "ENTER_", "THE_", "A_", "AN_", "PASTE_", "INSERT_", "PROVIDED_")
FM_DESC_RE = re.compile(r"(?m)^description:\s*(.+?)\s*$")
ALLOWED_BUNDLED = {"references", "assets", "scripts", "templates", "examples"}
EXCLUDE_BUNDLED_NOTE_DIRS = set()  # keep examples out of bundled_assets list but note its presence


def find_tier(name: str) -> str:
    for t, m in TIERS.items():
        if name in m:
            return t
    return "uncategorized"


def yaml_scalar(s: str) -> str:
    s = s.strip()
    # emit as a double-quoted YAML string with minimal escaping
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def skill_block(name: str) -> str:
    tier = find_tier(name)
    category = TIERS.get(tier, {}).get(name, "general")
    skill_dir = SKILLS_DIR / name
    skill_md = skill_dir / "SKILL.md"
    desc = ""
    if skill_md.is_file():
        m = FM_DESC_RE.search(skill_md.read_text(encoding="utf-8", errors="replace"))
        if m:
            desc = m.group(1).strip().strip("\"'")

    # bundled subdirs (non-empty)
    bundled = []
    for sub in sorted(ALLOWED_BUNDLED):
        d = skill_dir / sub
        if d.is_dir() and any(d.rglob("*")):
            if sub == "examples":
                continue  # examples is expected, list separately only if absent
            bundled.append(sub)
    examples_present = (skill_dir / "examples" / "prompts.md").is_file()

    # env vars across SKILL.md + bundled .py/.md
    envs: set[str] = set()
    scan_files = [skill_md] + list(skill_dir.rglob("*.py")) + list(skill_dir.rglob("*.md"))
    for f in scan_files:
        if f.is_file():
            envs.update(ENV_RE.findall(f.read_text(encoding="utf-8", errors="replace")))
    env_list = sorted(e for e in envs if e.upper() == e and not e.startswith(PLACEHOLDER_PREFIXES))

    external_api = tier == "external" or bool(env_list) or ("credential" in desc.lower()) or ("api key" in desc.lower())
    issues = list(KNOWN_ISSUES.get(name, []))

    lines = [f"  {name}:"]
    lines.append(f"    tier: {tier}")
    lines.append(f"    category: {category}")
    lines.append(f'    upstream_path: "skills/{name}/SKILL.md"')
    lines.append(f'    local_path: ".agent/skills/{name}/SKILL.md"')
    lines.append(f"    bundled_assets: {bundled if bundled else '[]'}")
    lines.append(f"    examples_present: {str(examples_present).lower()}")
    lines.append(f"    external_api: {str(external_api).lower()}")
    lines.append(f"    env_vars_noted: {env_list if env_list else '[]'}")
    if issues:
        lines.append("    known_upstream_issues:")
        for it in issues:
            lines.append(f"      - {yaml_scalar(it)}")
    else:
        lines.append("    known_upstream_issues: []")
    return "\n".join(lines)


def main() -> int:
    names = []
    for t in ("core", "tool", "external"):
        names.extend(sorted(TIERS[t].keys()))

    missing = [n for n in names if not (SKILLS_DIR / n / "SKILL.md").is_file()]
    if missing:
        print(f"ERROR: ported skill dirs missing for: {missing}", file=sys.stderr)
        return 1

    parts = []
    parts.append("# PORT_MANIFEST.yaml — provenance & per-skill metadata for ported capability skills.")
    parts.append("# Generated by .agent/scripts/generate_port_manifest.py — re-run to refresh; do not hand-edit.")
    parts.append("upstream:")
    parts.append(f'  repo: "{UPSTREAM_REPO}"')
    parts.append(f'  ref: "{UPSTREAM_REF}"')
    parts.append(f'  commit: "{UPSTREAM_COMMIT}"')
    parts.append(f'  license: "MIT (repo); per-skill licenses vary, see NOTICE.md"')
    parts.append(f'  port_date: "{PORT_DATE}"')
    parts.append(f'  port_mode: "adapted house-format canonical skills (not verbatim)"')
    parts.append("skills:")
    for n in names:
        parts.append(skill_block(n))
    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} with {len(names)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
