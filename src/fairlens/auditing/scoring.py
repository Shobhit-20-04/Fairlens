"""
Explainable Scoring and Rule-Based Warning System for FairLens.

Generates transparent score breakdowns, explicit component separation,
and contextualized warnings with severity levels and recommended actions.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AuditWarning:
    """Actionable warning triggered by representation gaps or statistical fragility."""

    warning_id: str
    dimension: str
    severity: str  # HIGH, MEDIUM, INFO
    title: str
    message: str
    trigger_metric: str
    observed_value: Any
    threshold_value: Any
    recommended_action: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "warning_id": self.warning_id,
            "dimension": self.dimension,
            "severity": self.severity,
            "title": self.title,
            "message": self.message,
            "trigger_metric": self.trigger_metric,
            "observed_value": self.observed_value,
            "threshold_value": self.threshold_value,
            "recommended_action": self.recommended_action,
        }


@dataclass
class Scorecard:
    """Explainable multi-component score breakdown."""

    coverage_score: Optional[float]  # 0 to 100
    parity_score: Optional[float]    # 0 to 100 (None if no reference distribution)
    completeness_score: float        # 0 to 100
    composite_score: Optional[float] # Weighted combination if all components present
    scoring_notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "coverage_score": self.coverage_score,
            "parity_score": self.parity_score,
            "completeness_score": round(self.completeness_score, 2),
            "composite_score": round(self.composite_score, 2) if self.composite_score is not None else None,
            "scoring_notes": self.scoring_notes,
        }


class ExplainableScoringFramework:
    """Computes transparent scores and evaluates rule-based warnings."""

    def __init__(self, warning_thresholds: Optional[Dict[str, float]] = None):
        self.thresholds = warning_thresholds or {
            "max_missing_rate": 0.15,
            "max_abs_deviation": 0.20,
            "min_subgroup_size": 30,
            "max_js_divergence": 0.15,
        }

    def evaluate_warnings(
        self,
        dimension_name: str,
        missing_rate: float,
        zero_observation_categories: List[str],
        proportions: Dict[str, Dict[str, Any]],
        max_abs_deviation: Optional[float],
        js_divergence: Optional[float],
    ) -> List[AuditWarning]:
        """Generate rule-based warnings for a specific audit dimension."""
        warnings: List[AuditWarning] = []

        # 1. Missingness Warning
        if missing_rate > self.thresholds["max_missing_rate"]:
            warnings.append(
                AuditWarning(
                    warning_id="WARN_HIGH_MISSINGNESS",
                    dimension=dimension_name,
                    severity="HIGH" if missing_rate > 0.30 else "MEDIUM",
                    title="Elevated Missing / Undisclosed Rate",
                    message=f"Dimension '{dimension_name}' has {missing_rate:.1%} missing, null, or undisclosed entries.",
                    trigger_metric="missing_rate",
                    observed_value=round(missing_rate, 4),
                    threshold_value=self.thresholds["max_missing_rate"],
                    recommended_action="Inspect data pipeline to determine if missing values reflect non-reporting bias.",
                )
            )

        # 2. Zero-Observation Categories Warning
        if zero_observation_categories:
            warnings.append(
                AuditWarning(
                    warning_id="WARN_ZERO_OBSERVATION",
                    dimension=dimension_name,
                    severity="HIGH",
                    title="Documented Target Category Entirely Absent",
                    message=(
                        f"Categories {zero_observation_categories} are documented in target population "
                        f"but have exactly 0 observations in dataset."
                    ),
                    trigger_metric="zero_observation_count",
                    observed_value=len(zero_observation_categories),
                    threshold_value=0,
                    recommended_action="Supplement dataset with targeted sampling of omitted groups before training.",
                )
            )

        # 3. Sparse Subgroups Sample Size Warning
        sparse_cats = [
            cat for cat, data in proportions.items()
            if data["count"] < self.thresholds["min_subgroup_size"]
        ]
        if sparse_cats:
            warnings.append(
                AuditWarning(
                    warning_id="WARN_SPARSE_SUBGROUP",
                    dimension=dimension_name,
                    severity="MEDIUM",
                    title="Small Subgroup Sample Size",
                    message=(
                        f"Categories {sparse_cats} have fewer than {int(self.thresholds['min_subgroup_size'])} "
                        f"observations. Estimates for these groups carry wide statistical confidence intervals."
                    ),
                    trigger_metric="min_subgroup_size",
                    observed_value=[(c, proportions[c]["count"]) for c in sparse_cats],
                    threshold_value=int(self.thresholds["min_subgroup_size"]),
                    recommended_action="Avoid drawing definitive fairness conclusions on sparse subgroups without additional data.",
                )
            )

        # 4. Severe Representation Deviation Warning (Only when reference exists)
        if max_abs_deviation is not None and max_abs_deviation > self.thresholds["max_abs_deviation"]:
            warnings.append(
                AuditWarning(
                    warning_id="WARN_SEVERE_DEVIATION",
                    dimension=dimension_name,
                    severity="HIGH",
                    title="Substantial Deviation from Reference Distribution",
                    message=(
                        f"Maximum category share deviation ({max_abs_deviation:.1%}) exceeds threshold "
                        f"({self.thresholds['max_abs_deviation']:.1%}) relative to configured reference population."
                    ),
                    trigger_metric="max_abs_deviation",
                    observed_value=max_abs_deviation,
                    threshold_value=self.thresholds["max_abs_deviation"],
                    recommended_action="Verify whether sampling intentionality explains deviation or indicates collection bias.",
                )
            )

        # 5. Jensen-Shannon Divergence Warning
        if js_divergence is not None and js_divergence > self.thresholds["max_js_divergence"]:
            warnings.append(
                AuditWarning(
                    warning_id="WARN_DISTRIBUTION_DIVERGENCE",
                    dimension=dimension_name,
                    severity="MEDIUM",
                    title="Elevated Distribution Divergence (JSD)",
                    message=(
                        f"Jensen-Shannon divergence ({js_divergence:.3f}) indicates noticeable structural "
                        f"difference from expected distribution."
                    ),
                    trigger_metric="js_divergence",
                    observed_value=js_divergence,
                    threshold_value=self.thresholds["max_js_divergence"],
                    recommended_action="Review demographic cross-tabs to identify which specific categories drive the divergence.",
                )
            )

        return warnings

    def calculate_scorecard(
        self,
        coverage_ratio: Optional[float],
        max_abs_deviation: Optional[float],
        missing_rate: float,
    ) -> Scorecard:
        """
        Compute an explainable scorecard for an audited dimension.

        Scoring Rules:
        - Coverage Score = coverage_ratio * 100 (if expected categories provided; else None)
        - Parity Score = max(0, (1.0 - max_abs_deviation) * 100) (if reference distribution provided; else None)
        - Completeness Score = max(0, (1.0 - missing_rate) * 100)
        - Composite Score = computed only when all components are available. NEVER silently redistributes weights.
        """
        notes = []

        cov_score = round(coverage_ratio * 100.0, 2) if coverage_ratio is not None else None
        if cov_score is None:
            notes.append("Coverage score unavailable: No expected categories list configured.")

        par_score = None
        if max_abs_deviation is not None:
            par_score = round(max(0.0, (1.0 - max_abs_deviation) * 100.0), 2)
        else:
            notes.append("Parity score unavailable: No reference target distribution configured (descriptive profiling only).")

        comp_score = round(max(0.0, (1.0 - missing_rate) * 100.0), 2)

        # Composite score calculation (40% Coverage, 40% Parity, 20% Completeness)
        composite = None
        if cov_score is not None and par_score is not None:
            composite = (0.40 * cov_score) + (0.40 * par_score) + (0.20 * comp_score)
            notes.append("Composite score computed using: 40% Coverage + 40% Parity + 20% Completeness.")
        else:
            notes.append("Composite score omitted to prevent misleading scores when reference components are absent.")

        return Scorecard(
            coverage_score=cov_score,
            parity_score=par_score,
            completeness_score=comp_score,
            composite_score=composite,
            scoring_notes=notes,
        )
