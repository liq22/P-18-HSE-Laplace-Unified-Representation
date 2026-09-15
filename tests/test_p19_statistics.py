import unittest

from experiments.p19.statistics import reduce_method


class P19StatisticsTests(unittest.TestCase):
    def test_group_macro_does_not_weight_groups_by_window_count(self):
        rows = []
        for unit in range(10):
            rows.append({"method": "M", "condition_id": "c", "group_id": "g1", "seed": "0", "unit_id": str(unit), "value": 1.0})
        rows.append({"method": "M", "condition_id": "c", "group_id": "g2", "seed": "0", "unit_id": "0", "value": 3.0})
        _, groups = reduce_method(rows, "M", "c")
        self.assertEqual(groups, {"g1": 1.0, "g2": 3.0})
        self.assertAlmostEqual(sum(groups.values()) / len(groups), 2.0)

    def test_seeds_are_averaged_inside_original_group(self):
        rows = [
            {"method": "M", "condition_id": "c", "group_id": "g", "seed": "0", "unit_id": "u", "value": 1.0},
            {"method": "M", "condition_id": "c", "group_id": "g", "seed": "1", "unit_id": "u", "value": 3.0},
        ]
        _, groups = reduce_method(rows, "M", "c")
        self.assertAlmostEqual(groups["g"], 2.0)


if __name__ == "__main__":
    unittest.main()
