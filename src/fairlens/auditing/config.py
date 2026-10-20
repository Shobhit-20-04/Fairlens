"""
Configuration Models and Dimension Specifications for Representation Auditing.

Allows users to configure demographic, geographic, and cultural audit dimensions,
provide optional target population reference distributions, and tune warning thresholds.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class AuditDimension:
    """Specification of an audit dimension (e.g. gender, state, religion, caste)."""

    name: str
    column_name: str
    dimension_type: str = "demographic"  # demographic, geographic, cultural, custom
    expected_categories: Optional[List[str]] = None
    expected_distribution: Optional[Dict[str, float]] = None  # e.g. {"Male": 0.51, "Female": 0.49}
    min_sample_size: int = 30  # Subgroups with N < min_sample_size trigger uncertainty warnings

    def __post_init__(self):
        """Validate dimension configuration."""
        if not self.name or not self.column_name:
            raise ValueError("AuditDimension must have non-empty 'name' and 'column_name'")
        if self.min_sample_size < 1:
            raise ValueError(f"min_sample_size must be >= 1, got {self.min_sample_size}")

        if self.expected_distribution:
            total_prob = sum(self.expected_distribution.values())
            if not (0.98 <= total_prob <= 1.02):
                raise ValueError(
                    f"Expected distribution probabilities for '{self.name}' must sum to ~1.0, got {total_prob:.4f}"
                )
            # If expected_categories not explicitly provided, infer from expected_distribution keys
            if self.expected_categories is None:
                self.expected_categories = list(self.expected_distribution.keys())


@dataclass
class AuditConfig:
    """Master configuration for dataset representation-gap auditing."""

    dimensions: List[AuditDimension]
    intersectional_pairs: Optional[List[Tuple[str, str]]] = None  # e.g. [("gender", "state")]
    excluded_columns: List[str] = field(default_factory=list)
    id_columns: List[str] = field(default_factory=list)
    target_column: Optional[str] = None

    # Missing value markers
    missing_value_markers: List[str] = field(
        default_factory=lambda: [
            "", "null", "none", "nan", "unknown", "undisclosed", "n/a", "na", "?", "missing", "unspecified"
        ]
    )

    # Statistical Parameters
    confidence_level: float = 0.95
    warning_thresholds: Dict[str, float] = field(
        default_factory=lambda: {
            "max_missing_rate": 0.15,
            "max_abs_deviation": 0.20,
            "min_subgroup_size": 30,
            "max_js_divergence": 0.15,
        }
    )

    def __post_init__(self):
        """Validate audit configuration."""
        if not self.dimensions:
            raise ValueError("AuditConfig must contain at least one AuditDimension")
        col_names = [d.column_name for d in self.dimensions]
        if len(col_names) != len(set(col_names)):
            raise ValueError(f"Duplicate column mappings detected in dimensions: {col_names}")
        if not (0.50 <= self.confidence_level < 1.0):
            raise ValueError("confidence_level must be between 0.50 and 0.999")
