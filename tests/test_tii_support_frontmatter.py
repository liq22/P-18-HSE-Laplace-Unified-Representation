"""Focused manuscript, figure and finite-scientific-witness checks."""
from pathlib import Path
import csv
import os
import re
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]

class SupportFrontMatterTests(unittest.TestCase):
    def test_read_originals_are_used_and_citations_resolve(self):
        body='\n'.join((ROOT/'paper'/f).read_text() for f in
                       ['main.md','related_work.md','formulation.md','method.md'])
        cited=set(re.findall(r'@([A-Za-z0-9_]+)',body))
        keys=re.findall(r'@\w+\{([^,]+),',(ROOT/'literature/references.bib').read_text())
        self.assertEqual(len(keys),len(set(keys)))
        self.assertFalse(cited-set(keys))
        originals=set(re.findall(r'\(`([A-Za-z0-9_]+)`\)',
                                 (ROOT/'paper/literature_matrix.md').read_text()))
        self.assertGreaterEqual(len(originals),30)
        self.assertFalse(originals-cited)

    def test_both_figures_are_editable(self):
        for name,required in [('motivation',{'support-panel','ambiguity-panel','world-plus','world-minus'}),
                              ('overview',{'qualified-target','temporal-denoiser','velocity-conversion','restricted-update','observed-readout','fixed-diagnostic-head'})]:
            with self.subTest(figure=name):
                path=ROOT/'paper/figures'/f'{name}.svg'
                root=ET.parse(path).getroot()
                tags=[e.tag.split('}')[-1] for e in root.iter()]
                self.assertNotIn('image',tags)
                self.assertNotIn('foreignObject',tags)
                self.assertGreater(tags.count('text'),15)
                ids=[e.attrib['id'] for e in root.iter() if 'id' in e.attrib]
                self.assertEqual(len(ids),len(set(ids)))
                self.assertTrue(required<=set(ids),required-set(ids))
                self.assertNotIn('base64',path.read_text())

    def test_chapter_roles_and_equations(self):
        formulation=(ROOT/'paper/formulation.md').read_text()
        method=(ROOT/'paper/method.md').read_text()
        related=(ROOT/'paper/related_work.md').read_text()
        self.assertIn('## 2. Basic Theory and Problem Formulation',formulation)
        self.assertIn('## 3. Method',method)
        self.assertNotRegex(related,r'(?m)^#+ 2[. ]')
        self.assertIn('figures/motivation.pdf',formulation)
        self.assertNotIn('figures/overview.pdf',formulation)
        self.assertIn('figures/overview.pdf',method)
        tags=re.findall(r'\\tag\{(\d+)\}',formulation+'\n'+method)
        self.assertEqual(list(map(int,tags)),list(range(1,15)))

    def test_actual_witness_numbers_when_build_requested(self):
        output=os.environ.get('TII_BUILD_OUTPUT')
        if not output:
            self.skipTest('Run the manuscript build to execute the finite witnesses.')
        def values(name):
            with (Path(output)/f'{name}_witness.csv').open() as f:
                rows=list(csv.DictReader(f))
            return rows,{r['witness']:float(r['value']) for r in rows}
        support,s=values('support')
        self.assertEqual(len(support),14)
        self.assertEqual(s['unpaired_same_marginal_conditional_gap'],1)
        self.assertAlmostEqual(s['correlated_prior_null_posterior_variance'],.68)
        method,m=values('method')
        self.assertEqual(len(method),13)
        for key in ['velocity_clean_conversion_max_error','velocity_clean_weighted_loss_max_error',
                    'intrinsic_ddim_oracle_path_max_error','intrinsic_ddim_forbidden_max_norm',
                    'intrinsic_ddim_observed_drift_max_norm','intrinsic_ddim_terminal_max_error']:
            self.assertLess(m[key],1e-12)
        self.assertAlmostEqual(m['joint_score_slice_implied_variance'],.36)
        self.assertEqual(m['true_marginal_variance'],1)
        self.assertAlmostEqual(m['coherent_cross_covariance'],.8)
        self.assertEqual(m['independent_cross_covariance'],0)
        self.assertAlmostEqual(m['coherent_sum_variance'],3.6)
        self.assertEqual(m['independent_sum_variance'],2)

if __name__=='__main__':unittest.main()
