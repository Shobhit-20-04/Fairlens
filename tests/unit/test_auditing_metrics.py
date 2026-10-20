"""
Unit tests for FairLens representation metrics calculations.
"""

import unittest
import pandas as pd
from fairlens.auditing.metrics import RepresentationMetrics


class TestRepresentationMetrics(unittest.TestCase):
    """Test suite for mathematical fairness and coverage metrics."""

    def test_missing_rate_calculation(self):
        """Verify missing rate with diverse null and marker values."""
        s = pd.Series(["valid", None, "unknown", "valid2", "n/a", "VALID3", ""])
        missing_cnt, valid_cnt, rate = RepresentationMetrics.calculate_missing_rate(
            s, missing_markers=["unknown", "n/a", ""]
        )
        self.assertEqual(missing_cnt, 4)
        self.assertEqual(valid_cnt, 3)
        self.assertAlmostEqual(rate, 4 / 7, places=3)

    def test_wilson_interval_bounds(self):
        """Verify Wilson score confidence interval satisfies [0, 1] bounds and symmetry."""
        # 50 out of 100 -> center is 0.5, symmetric
        ci_low, ci_high = RepresentationMetrics.calculate_wilson_interval(50, 100, confidence=0.95)
        self.assertLess(ci_low, 0.5)
        self.assertGreater(ci_high, 0.5)
        self.assertAlmostEqual(0.5 - ci_low, ci_high - 0.5, places=3)

        # Extreme case: 0 out of 100 -> lower bound must be exactly >= 0.0
        zero_low, zero_high = RepresentationMetrics.calculate_wilson_interval(0, 100)
        self.assertEqual(zero_low, 0.0)
        self.assertGreater(zero_high, 0.0)

        # Extreme case: 100 out of 100 -> upper bound must be <= 1.0
        one_low, one_high = RepresentationMetrics.calculate_wilson_interval(100, 100)
        self.assertLess(one_low, 1.0)
        self.assertEqual(one_high, 1.0)

    def test_category_coverage(self):
        """Test coverage ratio and zero-observation detection."""
        observed = ["Male", "Female"]
        expected = ["Male", "Female", "Non-Binary"]

        coverage, zero_obs, unlisted = RepresentationMetrics.calculate_category_coverage(observed, expected)
        self.assertAlmostEqual(coverage, 2 / 3, places=3)
        self.assertEqual(zero_obs, ["Non-Binary"])
        self.assertEqual(unlisted, [])

    def test_representation_deviations_and_jsd(self):
        """Test deviation calculations and Jensen-Shannon Divergence."""
        # Observed: 80% Male, 20% Female
        proportions = {
            "Male": {"count": 80, "share": 0.80},
            "Female": {"count": 20, "share": 0.20},
        }
        # Expected: 50% Male, 50% Female
        expected_dist = {"Male": 0.50, "Female": 0.50}

        devs, mean_dev, max_dev, jsd = RepresentationMetrics.calculate_representation_deviations(
            proportions, expected_dist
        )
        self.assertIsNotNone(devs)
        self.assertAlmostEqual(devs["Male"], 0.30, places=3)
        self.assertAlmostEqual(devs["Female"], -0.30, places=3)
        self.assertAlmostEqual(max_dev, 0.30, places=3)
        self.assertAlmostEqual(mean_dev, 0.30, places=3)
        self.assertGreater(jsd, 0.0)

    def test_intersectional_matrix(self):
        """Test cross-tabulation and sparse cell detection."""
        df = pd.DataFrame({
            "gender": ["M"] * 50 + ["F"] * 50 + ["M"] * 5,
            "region": ["Urban"] * 50 + ["Urban"] * 50 + ["Rural"] * 5,
        })
        res = RepresentationMetrics.calculate_intersectional_matrix(
            df, "gender", "region", missing_markers=[], min_sample_size=30
        )
        self.assertEqual(res["total_valid_intersection"], 105)
        # Rural & M has count = 5 (< 30) -> sparse cell
        self.assertGreaterEqual(res["sparse_cell_count"], 1)


if __name__ == "__main__":
    unittest.main()
