"""Focused checks of this paper/figure slice, not a manuscript scoring framework."""
from pathlib import Path
import os
import re
import unittest
import xml.etree.ElementTree as ET
import csv

ROOT=Path(__file__).resolve().parents[1]

class SupportFrontMatterTests(unittest.TestCase):
    def test_read_originals_are_used_and_citations_resolve(self):
        body='\n'.join((ROOT/'paper'/f).read_text() for f in ['main.md','related_work.md'])
        cited=set(re.findall(r'@([A-Za-z0-9_]+)',body))
        keys=re.findall(r'@\w+\{([^,]+),',(ROOT/'literature/references.bib').read_text())
        self.assertEqual(len(keys),len(set(keys)))
        self.assertFalse(cited-set(keys))
        matrix=(ROOT/'paper/literature_matrix.md').read_text()
        originals=set(re.findall(r'\(`([A-Za-z0-9_]+)`\)',matrix))
        self.assertGreaterEqual(len(originals),30)
        self.assertFalse(originals-cited)
    def test_vector_is_editable_not_a_bitmap_wrapper(self):
        root=ET.parse(ROOT/'paper/figures/motivation.svg').getroot()
        tags=[e.tag.split('}')[-1] for e in root.iter()]
        self.assertNotIn('image',tags)
        self.assertNotIn('foreignObject',tags)
        self.assertGreater(tags.count('text'),35)
        ids=[e.attrib['id'] for e in root.iter() if 'id' in e.attrib]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertGreater(len(ids),70)
        self.assertNotIn('base64',(ROOT/'paper/figures/motivation.svg').read_text())
    def test_formulation_keeps_key_boundaries(self):
        theory=(ROOT/'paper/theory_main.md').read_text()
        for phrase in ['correlated prior','range(A_e^T)','not a universal necessity','rank(G_e)=0']:
            self.assertIn(phrase,theory)
        self.assertIn('Laplace-noise',(ROOT/'paper/related_work.md').read_text())
    def test_actual_witness_numbers_when_build_requested(self):
        out=os.environ.get('TII_BUILD_OUTPUT')
        if not out:
            self.skipTest('finite witness numbers checked by the manuscript build, not fabricated')
        with (Path(out)/'support_witness.csv').open() as f: rows=list(csv.DictReader(f))
        values={r['witness']:float(r['value']) for r in rows}
        self.assertEqual(len(rows),14)
        self.assertEqual(values['source_partition_sum_residual'],0)
        self.assertEqual(values['target_common_rank'],0)
        self.assertEqual(values['unpaired_same_marginal_conditional_gap'],1)
        self.assertAlmostEqual(values['correlated_prior_null_posterior_mean'],.4)
        self.assertAlmostEqual(values['correlated_prior_null_posterior_variance'],.68)
        self.assertEqual(values['projected_update_max_forbidden_energy'],0)

if __name__=='__main__':unittest.main()
