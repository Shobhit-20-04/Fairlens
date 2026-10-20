"""
Unit tests for FairLens cost estimation engine and budget controls.
"""

import unittest
from fairlens.api.exceptions import FairLensBudgetExceededError
from fairlens.api.pricing import CostEstimator


class TestCostEstimator(unittest.TestCase):
    """Test suite for inference cost calculation formulas and budget gating."""

    def setUp(self):
        self.estimator = CostEstimator(
            default_input_price_per_m=0.60,
            default_output_price_per_m=3.60,
            max_spend_usd=5.00,
            warn_spend_usd=2.00,
        )

    def test_known_calculation_values(self):
        """Verify cost formulas against hand-calculated values with paid rates."""
        # 1,000 requests, 500 in, 200 out
        # Billable: 1,000
        # In: 500k tokens * $0.60 / 1M = $0.30
        # Out: 200k tokens * $3.60 / 1M = $0.72
        # Base: $1.02
        # Safety Margin 15%: $1.02 * 1.15 = $1.173
        est = self.estimator.estimate(
            total_requests=1000,
            avg_input_tokens=500,
            avg_output_tokens=200,
            cache_hit_rate=0.0,
            safety_margin=0.15,
            use_free_tier=False,
        )
        self.assertAlmostEqual(est.base_input_cost, 0.30, places=4)
        self.assertAlmostEqual(est.base_output_cost, 0.72, places=4)
        self.assertAlmostEqual(est.base_total_cost, 1.02, places=4)
        self.assertAlmostEqual(est.projected_total_cost, 1.173, places=3)
        self.assertTrue(est.within_budget)

    def test_cache_hit_rate_reduction(self):
        """Verify that cache hit rate reduces billable requests proportionally."""
        est_no_cache = self.estimator.estimate(
            total_requests=1000,
            avg_input_tokens=500,
            avg_output_tokens=200,
            cache_hit_rate=0.0,
            use_free_tier=False,
        )
        est_with_cache = self.estimator.estimate(
            total_requests=1000,
            avg_input_tokens=500,
            avg_output_tokens=200,
            cache_hit_rate=0.5,
            use_free_tier=False,
        )
        self.assertEqual(est_with_cache.billable_requests, 500)
        self.assertAlmostEqual(
            est_with_cache.projected_total_cost,
            est_no_cache.projected_total_cost / 2.0,
            places=3,
        )

    def test_free_tier_pricing(self):
        """Verify that official free tier for Nemotron 3 Ultra projects $0.00."""
        est = self.estimator.estimate(
            total_requests=500,
            avg_input_tokens=800,
            avg_output_tokens=300,
            model="nvidia/nemotron-3-ultra-550b-a55b",
            use_free_tier=True,
        )
        self.assertEqual(est.base_input_cost, 0.0)
        self.assertEqual(est.base_output_cost, 0.0)
        self.assertEqual(est.projected_total_cost, 0.0)
        self.assertTrue(est.within_budget)

    def test_budget_exceeded_raises_error(self):
        """Ensure exceeding budget threshold triggers FairLensBudgetExceededError."""
        # 10,000 requests, 2000 in, 1000 out -> ~ $12 + $36 = $48 base > $5 budget
        with self.assertRaises(FairLensBudgetExceededError):
            self.estimator.estimate(
                total_requests=10000,
                avg_input_tokens=2000,
                avg_output_tokens=1000,
                use_free_tier=False,
                enforce_budget=True,
            )


if __name__ == "__main__":
    unittest.main()
