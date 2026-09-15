import unittest
from experiments.p19.routing import weighted_headroom

class RoutingHeadroomTests(unittest.TestCase):
    def test_zero_when_one_arm_dominates(self):
        self.assertAlmostEqual(weighted_headroom([[.1,.2],[.3,.4]],[.5,.5]),0.)
    def test_positive_for_conditional_crossing(self):
        self.assertAlmostEqual(weighted_headroom([[.1,.3],[.4,.2]],[.5,.5]),.1)

if __name__ == '__main__': unittest.main()
