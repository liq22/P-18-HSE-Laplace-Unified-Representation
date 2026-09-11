import unittest

from experiments.p19.toy_routing import headroom


class RoutingHeadroomTests(unittest.TestCase):
    def test_zero_when_one_arm_dominates(self):
        rows = [
            {"condition": "a", "arm": "R", "risk": .1},
            {"condition": "a", "arm": "M", "risk": .2},
            {"condition": "b", "arm": "R", "risk": .3},
            {"condition": "b", "arm": "M", "risk": .4},
        ]
        self.assertAlmostEqual(headroom(rows), 0.0)

    def test_positive_for_conditional_crossing(self):
        rows = [
            {"condition": "a", "arm": "R", "risk": .1},
            {"condition": "a", "arm": "M", "risk": .3},
            {"condition": "b", "arm": "R", "risk": .4},
            {"condition": "b", "arm": "M", "risk": .2},
        ]
        self.assertAlmostEqual(headroom(rows), .1)


if __name__ == "__main__":
    unittest.main()
