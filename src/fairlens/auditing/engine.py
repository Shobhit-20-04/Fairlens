"""
Master Representation-Gap Audit Engine for FairLens.

Coordinates tabular data ingestion, multi-dimensional metric computation,
confidence interval estimation, explainable scorecards, and report generation.
"""

import csv
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import pandas as pd

from fairlens.auditing.config import AuditConfig, AuditDimension
from fairlens.auditing.loader import TabularDataLoader
from fairlens.auditing.metrics import RepresentationMetrics
from fairlens.auditing.scoring import AuditWarning, ExplainableScoringFramework, Scorecard
from fairlens.config.logging import get_logger

logger = get_logger("auditing.engine")


@dataclass
class DimensionAuditResult:
    """Audit outcomes for a single demographic, geographic, or cultural dimension."""

    dimension_name: str
    column_name: str
    dimension_type: str
    total_records: int
    missing_records: int
    valid_records: int
    missing_rate: float
    observed_category_count: int
    proportions: Dict[str, Dict[str, Any]]
    expected_categories: Optional[List[str]]
    coverage_ratio: Optional[float]
    zero_observation_categories: List[str]
    deviations: Optional[Dict[str, float]]
    max_abs_deviation: Optional[float]
    mean_abs_deviation: Optional[float]
    js_divergence: Optional[float]
    scorecard: Scorecard
    warnings: List[AuditWarning]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dimension_name": self.dimension_name,
            "column_name": self.column_name,
            "dimension_type": self.dimension_type,
            "total_records": self.total_records,
            "missing_records": self.missing_records,
            "valid_records": self.valid_records,
            "missing_rate": self.missing_rate,
            "observed_category_count": self.observed_category_count,
            "proportions": self.proportions,
            "expected_categories": self.expected_categories,
            "coverage_ratio": self.coverage_ratio,
            "zero_observation_categories": self.zero_observation_categories,
            "deviations": self.deviations,
            "max_abs_deviation": self.max_abs_deviation,
            "mean_abs_deviation": self.mean_abs_deviation,
            "js_divergence": self.js_divergence,
            "scorecard": self.scorecard.to_dict(),
            "warnings": [w.to_dict() for w in self.warnings],
        }


@dataclass
class AuditReport:
    """Complete structured audit report with dataset profile, dimensions, and caveats."""

    dataset_profile: Dict[str, Any]
    dimensions: Dict[str, DimensionAuditResult]
    intersectional_results: Dict[str, Any]
    total_warnings_count: int
    high_severity_warnings: int
    execution_time_seconds: float
    assumptions_and_limitations: List[str] = field(
        default_factory=lambda: [
            "Dataset representation auditing measures sample composition; it does not automatically establish downstream model discrimination.",
            "Absence of a demographic category does not imply malicious exclusion unless the target domain population warrants its presence.",
            "Confidence intervals rely on Wilson score intervals with configured 95% confidence level.",
            "Subgroup categories with N < 30 carry elevated statistical uncertainty and should be interpreted with caution.",
        ]
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dataset_profile": self.dataset_profile,
            "dimensions": {k: v.to_dict() for k, v in self.dimensions.items()},
            "intersectional_results": self.intersectional_results,
            "total_warnings_count": self.total_warnings_count,
            "high_severity_warnings": self.high_severity_warnings,
            "execution_time_seconds": round(self.execution_time_seconds, 4),
            "assumptions_and_limitations": self.assumptions_and_limitations,
        }

    def format_text_summary(self) -> str:
        """Render readable markdown text summary of audit findings."""
        lines = [
            "==================================================================",
            "             FAIRLENS DATASET REPRESENTATION AUDIT REPORT         ",
            "==================================================================",
            f"Dataset: {self.dataset_profile.get('file_name', 'In-Memory DataFrame')}",
            f"Total Records: {self.dataset_profile.get('total_rows', 0):,} | Columns: {self.dataset_profile.get('total_columns', 0)}",
            f"Duplicate Rows: {self.dataset_profile.get('duplicate_rows', 0):,} ({self.dataset_profile.get('duplicate_rate', 0.0):.1%})",
            f"Audit Execution Time: {self.execution_time_seconds:.3f}s",
            f"Total Warnings: {self.total_warnings_count} ({self.high_severity_warnings} High Severity)",
            "\n--- DIMENSION BREAKDOWN ---",
        ]

        for dim_name, res in self.dimensions.items():
            lines.append(f"\n[Dimension: {dim_name.upper()} (Column: '{res.column_name}')]")
            lines.append(f"  Valid: {res.valid_records:,} | Missing/Unknown: {res.missing_records:,} ({res.missing_rate:.1%})")

            if res.coverage_ratio is not None:
                lines.append(f"  Target Category Coverage: {res.coverage_ratio:.1%}")
                if res.zero_observation_categories:
                    lines.append(f"  !! Zero-Observation Categories: {res.zero_observation_categories}")

            if res.max_abs_deviation is not None:
                lines.append(f"  Max Absolute Deviation: {res.max_abs_deviation:.1%} | JSD: {res.js_divergence:.4f}")

            # Scorecard
            sc = res.scorecard
            score_parts = [f"Completeness={sc.completeness_score:.1f}"]
            if sc.coverage_score is not None:
                score_parts.append(f"Coverage={sc.coverage_score:.1f}")
            if sc.parity_score is not None:
                score_parts.append(f"Parity={sc.parity_score:.1f}")
            if sc.composite_score is not None:
                score_parts.append(f"Composite={sc.composite_score:.1f}/100")
            lines.append(f"  Scores: {', '.join(score_parts)}")

            lines.append("  Category Proportions (Observed vs 95% CI):")
            for cat, data in list(res.proportions.items())[:8]:
                sparse_flag = " [SPARSE N<30]" if data["sample_size_sparse"] else ""
                lines.append(
                    f"    - {cat}: {data['count']:,} ({data['share']:.1%}) "
                    f"[95% CI: {data['ci_lower']:.1%} - {data['ci_upper']:.1%}]{sparse_flag}"
                )
            if len(res.proportions) > 8:
                lines.append(f"    ... and {len(res.proportions) - 8} more categories.")

            if res.warnings:
                lines.append("  Active Warnings:")
                for w in res.warnings:
                    lines.append(f"    * [{w.severity}] {w.title}: {w.message}")

        if self.intersectional_results:
            lines.append("\n--- INTERSECTIONAL DEMOGRAPHIC ANALYSIS ---")
            for pair_key, inter_data in self.intersectional_results.items():
                lines.append(f"  Pair: {pair_key}")
                lines.append(f"    Total Valid Intersected: {inter_data.get('total_valid_intersection', 0):,}")
                lines.append(f"    Sparse Cells (N<30): {inter_data.get('sparse_cell_count', 0)}")
                if inter_data.get("zero_cells"):
                    lines.append(f"    Zero Cells: {inter_data.get('zero_cells')[:5]}")

        lines.append("\n--- ASSUMPTIONS & LIMITATIONS ---")
        for caveat in self.assumptions_and_limitations:
            lines.append(f"  • {caveat}")

        lines.append("==================================================================")
        return "\n".join(lines)


class RepresentationAuditEngine:
    """Core engine evaluating representation gaps across tabular datasets."""

    def __init__(self, config: AuditConfig):
        self.config = config
        self.scorer = ExplainableScoringFramework(config.warning_thresholds)

    def audit(self, data_source: Union[Path, str, pd.DataFrame]) -> AuditReport:
        """Run audit against a tabular file path or in-memory DataFrame."""
        start_time = time.time()

        if isinstance(data_source, (str, Path)):
            df, profile = TabularDataLoader.load(Path(data_source))
        elif isinstance(data_source, pd.DataFrame):
            df = data_source
            profile = {
                "file_name": "In-Memory DataFrame",
                "format": "dataframe",
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "duplicate_rows": int(df.duplicated().sum()),
                "duplicate_rate": round(int(df.duplicated().sum()) / len(df), 4) if len(df) > 0 else 0.0,
                "columns": list(df.columns),
            }
        else:
            raise TypeError(f"data_source must be a file path or pd.DataFrame, got {type(data_source)}")

        # Validate that audit columns exist
        available_cols = set(df.columns)
        for dim in self.config.dimensions:
            if dim.column_name not in available_cols:
                raise ValueError(
                    f"Configured column '{dim.column_name}' for dimension '{dim.name}' not found in dataset. "
                    f"Available columns: {sorted(list(available_cols))}"
                )

        dimension_results: Dict[str, DimensionAuditResult] = {}
        total_warnings = 0
        high_severity_warnings = 0

        for dim in self.config.dimensions:
            series = df[dim.column_name]

            # Missingness
            missing_cnt, valid_cnt, missing_rate = RepresentationMetrics.calculate_missing_rate(
                series, self.config.missing_value_markers
            )

            # Category proportions & Wilson intervals
            proportions = RepresentationMetrics.compute_category_proportions(
                series,
                self.config.missing_value_markers,
                confidence=self.config.confidence_level,
                min_sample_size=dim.min_sample_size,
            )

            # Category Coverage & Zero-observation categories
            observed_cats = list(proportions.keys())
            coverage_ratio, zero_obs, unlisted = RepresentationMetrics.calculate_category_coverage(
                observed_cats, dim.expected_categories
            )

            # Deviations and JSD against reference distribution
            deviations, mean_dev, max_dev, js_div = RepresentationMetrics.calculate_representation_deviations(
                proportions, dim.expected_distribution
            )

            # Warnings evaluation
            warnings = self.scorer.evaluate_warnings(
                dimension_name=dim.name,
                missing_rate=missing_rate,
                zero_observation_categories=zero_obs,
                proportions=proportions,
                max_abs_deviation=max_dev,
                js_divergence=js_div,
            )

            # Scorecard calculation
            scorecard = self.scorer.calculate_scorecard(
                coverage_ratio=coverage_ratio,
                max_abs_deviation=max_dev,
                missing_rate=missing_rate,
            )

            dim_result = DimensionAuditResult(
                dimension_name=dim.name,
                column_name=dim.column_name,
                dimension_type=dim.dimension_type,
                total_records=len(series),
                missing_records=missing_cnt,
                valid_records=valid_cnt,
                missing_rate=missing_rate,
                observed_category_count=len(observed_cats),
                proportions=proportions,
                expected_categories=dim.expected_categories,
                coverage_ratio=coverage_ratio,
                zero_observation_categories=zero_obs,
                deviations=deviations,
                max_abs_deviation=max_dev,
                mean_abs_deviation=mean_dev,
                js_divergence=js_div,
                scorecard=scorecard,
                warnings=warnings,
            )
            dimension_results[dim.name] = dim_result

            total_warnings += len(warnings)
            high_severity_warnings += sum(1 for w in warnings if w.severity == "HIGH")

        # Intersectional Demographic Analysis
        intersectional_results: Dict[str, Any] = {}
        if self.config.intersectional_pairs:
            for pair in self.config.intersectional_pairs:
                name_a, name_b = pair
                # Find matching columns
                dim_map = {d.name: d.column_name for d in self.config.dimensions}
                col_a = dim_map.get(name_a)
                col_b = dim_map.get(name_b)
                if col_a and col_b:
                    inter_res = RepresentationMetrics.calculate_intersectional_matrix(
                        df,
                        col_a,
                        col_b,
                        self.config.missing_value_markers,
                        min_sample_size=30,
                    )
                    inter_res["pair"] = [name_a, name_b]
                    intersectional_results[f"{name_a}__x__{name_b}"] = inter_res

        elapsed = time.time() - start_time
        return AuditReport(
            dataset_profile=profile,
            dimensions=dimension_results,
            intersectional_results=intersectional_results,
            total_warnings_count=total_warnings,
            high_severity_warnings=high_severity_warnings,
            execution_time_seconds=elapsed,
        )

    def export_report(self, report: AuditReport, output_path: Union[str, Path], format: str = "json") -> None:
        """Export audit report to JSON or CSV."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if format.lower() == "json":
            with open(path, "w", encoding="utf-8") as f:
                json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)
            logger.info("Saved audit report to %s", path)
        elif format.lower() == "csv":
            # Flatten dimension proportions to CSV
            rows = []
            for dim_name, dim_data in report.dimensions.items():
                for cat, p in dim_data.proportions.items():
                    rows.append({
                        "dimension": dim_name,
                        "category": cat,
                        "count": p["count"],
                        "share": p["share"],
                        "ci_lower": p["ci_lower"],
                        "ci_upper": p["ci_upper"],
                        "sparse": p["sample_size_sparse"],
                        "dim_missing_rate": dim_data.missing_rate,
                        "dim_coverage_ratio": dim_data.coverage_ratio,
                        "dim_max_abs_deviation": dim_data.max_abs_deviation,
                    })
            if rows:
                with open(path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                    writer.writeheader()
                    writer.writerows(rows)
            logger.info("Saved audit summary CSV to %s", path)
        else:
            raise ValueError(f"Unsupported export format '{format}', must be 'json' or 'csv'")
