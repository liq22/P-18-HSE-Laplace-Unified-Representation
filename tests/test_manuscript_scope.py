"""Small checks for the requested manuscript split, not a document scoring system."""
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class ManuscriptScopeTests(unittest.TestCase):
    def test_external_protocols_belong_to_tpami(self):
        industrial=(ROOT/'paper/experiments.md').read_text()
        for name in ['PhysioNet','UCI HAR','USHCN','ETTh1','Japanese Vowels']:
            self.assertNotIn(name,industrial)
            self.assertIn(name,(ROOT/'paper_TPAMI/experiments.md').read_text())
        self.assertFalse((ROOT/'paper/assets/routing_controls.csv').exists())
        self.assertTrue((ROOT/'paper_TPAMI/assets/routing_controls.csv').is_file())
    def test_proofs_have_same_stem_notebooks(self):
        for path in ['paper/theory_main.md','paper_TPAMI/theory_main.md','paper_TPAMI/theory/policy_certificate.md']:
            self.assertTrue((ROOT/path).is_file())
            self.assertTrue((ROOT/path).with_suffix('.ipynb').is_file())
    def test_shared_bibliography_resolves_both_manuscripts(self):
        bib=(ROOT/'literature/references.bib').read_text()
        entries=re.findall(r'@\w+\{([^,]+),',bib)
        self.assertEqual(len(entries),len(set(entries)))
        for folder in ['paper','paper_TPAMI']:
            for name in ['main.md','related_work.md']:
                used=set(re.findall(r'@([A-Za-z0-9_]+)',(ROOT/folder/name).read_text()))
                self.assertFalse(used-set(entries),(folder,name,used-set(entries)))
    def test_tpami_does_not_copy_training_or_phm_code(self):
        self.assertFalse(list((ROOT/'paper_TPAMI').rglob('*trainer*.py')))
        self.assertTrue((ROOT/'paper_TPAMI/run_official_baselines.sh').is_file())
        self.assertFalse((ROOT/'paper/run_official_baselines.sh').exists())

if __name__=='__main__':unittest.main()
