"""
Core Mathematical Metrics for Representation-Gap Detection.

Implements transparent, reproducible formulas for coverage, category proportions,
Wilson score confidence intervals, representation deviations, Jensen-Shannon divergence,
and missingness analysis without artificial balance assumptions.
"""

import math
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from scipy.spatial.distance import jensenshannon
from scipy.special import erfcinv


class RepresentationMetrics:
    """Mathematical metric calculations for dataset representation auditing."""

    @staticmethod
    def calculate_missing_rate(
        series: pd.Series, missing_markers: List[str]
    ) -> Tuple[int, int, float]:
        """
        Calculate count of missing/unknown entries and missing rate.

        Returns: (missing_count, valid_count, missing_rate)
        """
        total = len(series)
        if total == 0:
            return 0, 0, 0.0

        # Build mask for pd.isna or string matching missing markers
        lower_markers = {m.lower().strip() for m in missing_markers}

        def is_missing_val(val: Any) -> bool:
            if pd.isna(val):
                return True
            s = str(val).strip().lower()
            return s in lower_markers

        missing_mask = series.map(is_missing_val)
        missing_count = int(missing_mask.sum())
        valid_count = total - missing_count
        missing_rate = missing_count / total

        return missing_count, valid_count, round(missing_rate, 4)

    @staticmethod
    def calculate_wilson_interval(
        count: int, total: int, confidence: float = 0.95
    ) -> Tuple[float, float]:
        """
        Compute Wilson score confidence interval for a category proportion.

        Guarantees interval bounds remain strictly within [0.0, 1.0] even for
        extreme proportions or small sample sizes.
        """
        if total == 0:
            return 0.0, 0.0

        # Normal critical value z (1.96 for 95%, 2.576 for 99%)
        # Standard normal inverse approximation
        alpha = 1.0 - confidence
        z = abs(math.sqrt(2.0) * float(erfcinv(alpha)))

        p_hat = count / total
        z2 = z * z
        denominator = 1.0 + (z2 / total)
        center = (p_hat + (z2 / (2.0 * total))) / denominator
        margin = (z / denominator) * math.sqrt((p_hat * (1.0 - p_hat) / total) + (z2 / (4.0 * (total ** 2))))

        ci_lower = max(0.0, center - margin)
        ci_upper = min(1.0, center + margin)
        return round(ci_lower, 4), round(ci_upper, 4)

    @staticmethod
    def compute_category_proportions(
        series: pd.Series,
        missing_markers: List[str],
        confidence: float = 0.95,
        min_sample_size: int = 30,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Calculate category counts, representation shares, and confidence intervals.
        """
        lower_markers = {m.lower().strip() for m in missing_markers}
        valid_series = series[~series.map(lambda v: pd.isna(v) or str(v).strip().lower() in lower_markers)]
        valid_total = len(valid_series)

        if valid_total == 0:
            return {}

        counts = valid_series.value_counts(dropna=True)
        results: Dict[str, Dict[str, Any]] = {}

        for cat, cnt in counts.items():
            cat_str = str(cat)
            cnt_int = int(cnt)
            share = cnt_int / valid_total
            ci_lower, ci_upper = RepresentationMetrics.calculate_wilson_interval(
                cnt_int, valid_total, confidence=confidence
            )

            results[cat_str] = {
                "count": cnt_int,
                "share": round(share, 4),
                "ci_lower": ci_lower,
                "ci_upper": ci_upper,
                "sample_size_sparse": cnt_int < min_sample_size,
            }

        return results

    @staticmethod
    def calculate_category_coverage(
        observed_categories: List[str], expected_categories: Optional[List[str]]
    ) -> Tuple[Optional[float], List[str], List[str]]:
        """
        Evaluate category coverage against documented target categories.

        Returns:
          (coverage_ratio, zero_observation_categories, unlisted_observed_categories)
        """
        if not expected_categories:
            return None, [], []

        expected_set = {str(c).strip().lower(): str(c) for c in expected_categories}
        observed_set = {str(c).strip().lower(): str(c) for c in observed_categories}

        zero_obs = [expected_set[k] for k in expected_set if k not in observed_set]
        unlisted = [observed_set[k] for k in observed_set if k not in expected_set]

        observed_expected_count = len(expected_set) - len(zero_obs)
        coverage_ratio = observed_expected_count / len(expected_set)

        return round(coverage_ratio, 4), zero_obs, unlisted

    @staticmethod
    def calculate_representation_deviations(
        observed_proportions: Dict[str, Dict[str, Any]],
        expected_distribution: Optional[Dict[str, float]],
    ) -> Tuple[Optional[Dict[str, float]], Optional[float], Optional[float], Optional[float]]:
        """
        Calculate difference from documented reference distribution.

        Returns:
          (deviations_by_category, mean_abs_deviation, max_abs_deviation, js_divergence)
        """
        if not expected_distribution:
            return None, None, None, None

        # Build matched probability vectors for shared categories
        all_cats = list(expected_distribution.keys())
        p_observed = []
        q_expected = []
        deviations = {}
        abs_diffs = []

        obs_map = {str(k).strip().lower(): v["share"] for k, v in observed_proportions.items()}

        for cat in all_cats:
            cat_key = str(cat).strip().lower()
            obs_share = obs_map.get(cat_key, 0.0)
            exp_share = expected_distribution[cat]

            diff = obs_share - exp_share
            deviations[str(cat)] = round(diff, 4)
            abs_diffs.append(abs(diff))

            p_observed.append(obs_share)
            q_expected.append(exp_share)

        mean_abs_dev = sum(abs_diffs) / len(abs_diffs) if abs_diffs else 0.0
        max_abs_dev = max(abs_diffs) if abs_diffs else 0.0

        # Jensen-Shannon Divergence using normalized vectors with small epsilon smoothing
        p_vec = np.array(p_observed, dtype=float) + 1e-9
        q_vec = np.array(q_expected, dtype=float) + 1e-9
        p_vec = p_vec / p_vec.sum()
        q_vec = q_vec / q_vec.sum()

        js_div = float(jensenshannon(p_vec, q_vec, base=2))

        return deviations, round(mean_abs_dev, 4), round(max_abs_dev, 4), round(js_div, 4)

    @staticmethod
    def calculate_intersectional_matrix(
        df: pd.DataFrame,
        col_a: str,
        col_b: str,
        missing_markers: List[str],
        min_sample_size: int = 30,
    ) -> Dict[str, Any]:
        """
        Compute 2D cross-tabulation for intersectional demographic analysis.
        """
        lower_markers = {m.lower().strip() for m in missing_markers}
        mask = (
            ~df[col_a].map(lambda v: pd.isna(v) or str(v).strip().lower() in lower_markers)
            & ~df[col_b].map(lambda v: pd.isna(v) or str(v).strip().lower() in lower_markers)
        )
        sub_df = df[mask]
        total_valid = len(sub_df)

        if total_valid == 0:
            return {"error": "No valid rows for intersectional pair"}

        cross_tab = pd.crosstab(sub_df[col_a], sub_df[col_b])
        sparse_cells = []
        zero_cells = []

        matrix_dict = {}
        for r_idx in cross_tab.index:
            matrix_dict[str(r_idx)] = {}
            for c_col in cross_tab.columns:
                count = int(cross_tab.loc[r_idx, c_col])
                matrix_dict[str(r_idx)][str(c_col)] = count
                if count == 0:
                    zero_cells.append((str(r_idx), str(c_col)))
                elif count < min_sample_size:
                    sparse_cells.append((str(r_idx), str(c_col), count))

        return {
            "dimension_a": col_a,
            "dimension_b": col_b,
            "total_valid_intersection": total_valid,
            "matrix": matrix_dict,
            "zero_cells": zero_cells,
            "sparse_cells": sparse_cells,
            "sparse_cell_count": len(sparse_cells),
        }
