from pathlib import Path
import unittest


THEORY_DIR = Path(__file__).resolve().parents[1] / "theory"
EXPECTED = [
    "00_axioms_and_notation.md",
    "01_observable_subspace_decomposition.md",
    "02_constructive_existence.md",
    "03_diffusion_flow_marginal_equivalence.md",
    "04_observed_private_invariance.md",
    "05_global_invariance_risk_lower_bound.md",
    "06_posterior_representation_sufficiency.md",
    "07_laplace_modal_stability.md",
    "08_shared_estimation_perturbation_bound.md",
    "09_unified_representation_risk_bound.md",
    "10_sampling_gap_shift_bound.md",
    "11_private_preserving_optimal_transport.md",
    "12_commuting_block_generators.md",
    "13_identifiability_and_failure_boundaries.md",
]


class TheoryCorpusTests(unittest.TestCase):
    def test_expected_independent_documents_exist(self) -> None:
        actual = sorted(path.name for path in THEORY_DIR.glob("*.md"))
        self.assertEqual(actual, EXPECTED)

    def test_no_non_whitespace_control_characters(self) -> None:
        for path in THEORY_DIR.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            invalid = [
                (index, ord(character))
                for index, character in enumerate(text)
                if ord(character) < 32 and character not in "\t\n\r"
            ]
            self.assertEqual(invalid, [], msg=f"invalid control characters in {path}")

    def test_axioms_are_explicit(self) -> None:
        text = (THEORY_DIR / EXPECTED[0]).read_text(encoding="utf-8")
        for index in range(10):
            self.assertIn(f"Axiom A{index}", text)
        self.assertIn("## 5. Unified representation", text)
        self.assertIn("## 8. Non-claims", text)

    def test_each_main_result_has_proof_and_boundary(self) -> None:
        boundary_markers = (
            "failure bound",
            "boundary",
            "does not prove",
            "counterexample",
            "limitation",
            "harmless",
        )
        consequence_markers = (
            "experimental implication",
            "falsifiable implementation consequences",
        )
        for name in EXPECTED[1:13]:
            text = (THEORY_DIR / name).read_text(encoding="utf-8")
            lower = text.lower()
            self.assertIn("## Status", text, msg=name)
            self.assertIn("Lemma", text, msg=name)
            self.assertIn("Theorem", text, msg=name)
            self.assertIn("proof", lower, msg=name)
            self.assertTrue(
                any(marker in lower for marker in boundary_markers),
                msg=f"no explicit boundary or counterexample in {name}",
            )
            self.assertTrue(
                any(marker in lower for marker in consequence_markers),
                msg=f"no empirical or implementation consequence in {name}",
            )

    def test_identifiability_document_contains_constructive_failures(self) -> None:
        text = (THEORY_DIR / EXPECTED[13]).read_text(encoding="utf-8")
        self.assertIn("Proposition 13.1", text)
        self.assertIn("Proposition 13.8", text)
        self.assertIn("Construction and proof", text)
        self.assertIn("Required negative controls", text)
        self.assertIn("Scientific boundary", text)


if __name__ == "__main__":
    unittest.main()
