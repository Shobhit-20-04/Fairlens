"""
Live Pricing Investigation and Cost Estimation Engine for FairLens.

Tracks verified model pricing, calculates projected inference costs,
enforces pre-execution spending thresholds, and logs cost breakdowns.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional
from fairlens.api.exceptions import FairLensBudgetExceededError
from fairlens.config.logging import get_logger

logger = get_logger("api.pricing")


# Documented Model Pricing and Verification Records
VERIFIED_MODEL_PRICING = {
    "nvidia/nemotron-3-ultra-550b-a55b": {
        "verified_endpoint": "https://openrouter.ai/models/nvidia/nemotron-3-ultra-550b-a55b",
        "verified_at": "2026-10-20T19:34:00+05:30",
        "free_tier_available": True,
        "input_price_per_m": 0.00,
        "output_price_per_m": 0.00,
        "fallback_paid_input_per_m": 0.60,
        "fallback_paid_output_per_m": 3.60,
        "context_window": 1_000_000,
        "max_output_tokens": 16_384,
        "rate_limits": "Free tier: ~20 req/min, 200 req/day",
        "data_logging_policy": "OpenRouter logs prompts on free endpoint for safety monitoring. Synthetic test cases only.",
        "pricing_uncertainty": "Low for free tier; high for enterprise routing variations across OpenRouter providers.",
    }
}


@dataclass
class CostEstimate:
    """Detailed breakdown of projected API inference costs."""
    model: str
    total_requests: int
    billable_requests: int
    estimated_input_tokens: int
    estimated_output_tokens: int
    input_price_per_m: float
    output_price_per_m: float
    base_input_cost: float
    base_output_cost: float
    base_total_cost: float
    safety_margin: float
    projected_total_cost: float
    cache_hit_rate: float
    within_budget: bool
    budget_limit: float

    def format_summary(self) -> str:
        """Return a formatted text summary of the cost estimate."""
        return (
            f"=== FairLens Cost Estimate ===\n"
            f"Model: {self.model}\n"
            f"Total Requests: {self.total_requests:,}\n"
            f"Cache Hit Rate: {self.cache_hit_rate:.1%}\n"
            f"Billable Requests: {self.billable_requests:,}\n"
            f"Est. Input Tokens: {self.estimated_input_tokens:,} (@ ${self.input_price_per_m:.2f}/M)\n"
            f"Est. Output Tokens: {self.estimated_output_tokens:,} (@ ${self.output_price_per_m:.2f}/M)\n"
            f"Base Projected Cost: ${self.base_total_cost:.4f}\n"
            f"Safety Margin: +{self.safety_margin:.1%}\n"
            f"Final Projected Cost: ${self.projected_total_cost:.4f} USD\n"
            f"Configured Budget Limit: ${self.budget_limit:.2f} USD\n"
            f"Status: {'APPROVED (Within Budget)' if self.within_budget else 'BLOCKED (Exceeds Budget)'}\n"
            f"=============================="
        )


class CostEstimator:
    """Calculates inference costs and validates spending limits before execution."""

    def __init__(
        self,
        default_input_price_per_m: float = 0.60,
        default_output_price_per_m: float = 3.60,
        max_spend_usd: float = 5.00,
        warn_spend_usd: float = 2.00,
    ):
        self.default_input_price_per_m = default_input_price_per_m
        self.default_output_price_per_m = default_output_price_per_m
        self.max_spend_usd = max_spend_usd
        self.warn_spend_usd = warn_spend_usd

    def get_pricing_info(self, model: str) -> Dict[str, Any]:
        """Retrieve verified pricing and policy metadata for a model."""
        if model in VERIFIED_MODEL_PRICING:
            return VERIFIED_MODEL_PRICING[model]
        return {
            "verified_endpoint": "Unknown / Unverified",
            "verified_at": "Unverified",
            "free_tier_available": False,
            "input_price_per_m": self.default_input_price_per_m,
            "output_price_per_m": self.default_output_price_per_m,
            "fallback_paid_input_per_m": self.default_input_price_per_m,
            "fallback_paid_output_per_m": self.default_output_price_per_m,
            "context_window": 8192,
            "max_output_tokens": 4096,
            "rate_limits": "Unknown",
            "data_logging_policy": "Unknown",
            "pricing_uncertainty": "High — Model not in verified ledger.",
        }

    def estimate(
        self,
        total_requests: int,
        avg_input_tokens: int,
        avg_output_tokens: int,
        model: str = "nvidia/nemotron-3-ultra-550b-a55b",
        cache_hit_rate: float = 0.0,
        safety_margin: float = 0.15,
        use_free_tier: bool = True,
        enforce_budget: bool = True,
    ) -> CostEstimate:
        """
        Compute projected costs.

        Formulas:
          Billable Requests = Total * (1 - cache_hit_rate)
          Input Cost = (Billable * avg_in * price_in) / 1,000,000
          Output Cost = (Billable * avg_out * price_out) / 1,000,000
          Projected Total = (Input Cost + Output Cost) * (1 + safety_margin)
        """
        pricing = self.get_pricing_info(model)
        if use_free_tier and pricing.get("free_tier_available", False):
            price_in = 0.0
            price_out = 0.0
        else:
            price_in = pricing.get("fallback_paid_input_per_m", self.default_input_price_per_m)
            price_out = pricing.get("fallback_paid_output_per_m", self.default_output_price_per_m)

        cache_hit_rate = max(0.0, min(1.0, cache_hit_rate))
        billable_requests = int(round(total_requests * (1.0 - cache_hit_rate)))

        total_input_tokens = billable_requests * avg_input_tokens
        total_output_tokens = billable_requests * avg_output_tokens

        base_input_cost = (total_input_tokens * price_in) / 1_000_000.0
        base_output_cost = (total_output_tokens * price_out) / 1_000_000.0
        base_total = base_input_cost + base_output_cost

        projected_total = base_total * (1.0 + safety_margin)
        within_budget = projected_total <= self.max_spend_usd

        estimate = CostEstimate(
            model=model,
            total_requests=total_requests,
            billable_requests=billable_requests,
            estimated_input_tokens=total_input_tokens,
            estimated_output_tokens=total_output_tokens,
            input_price_per_m=price_in,
            output_price_per_m=price_out,
            base_input_cost=round(base_input_cost, 6),
            base_output_cost=round(base_output_cost, 6),
            base_total_cost=round(base_total, 6),
            safety_margin=safety_margin,
            projected_total_cost=round(projected_total, 6),
            cache_hit_rate=cache_hit_rate,
            within_budget=within_budget,
            budget_limit=self.max_spend_usd,
        )

        if projected_total > self.warn_spend_usd:
            logger.warning(
                "Cost warning: Projected cost ($%.4f) exceeds warning threshold ($%.2f)",
                projected_total,
                self.warn_spend_usd,
            )

        if enforce_budget and not within_budget:
            logger.error(
                "Budget exceeded: Projected cost ($%.4f) exceeds maximum limit ($%.2f)",
                projected_total,
                self.max_spend_usd,
            )
            raise FairLensBudgetExceededError(projected_total, self.max_spend_usd)

        return estimate
