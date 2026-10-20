# FairLens Data Dictionary and Schema Reference

This document formalizes the data models, metadata parameters, and audit output schemas across FairLens.

---

## 1. Discovery Metadata Schema (`NormalizedDatasetMetadata`)

| Field Name | Type | Description | Example |
|---|---|---|---|
| `name` | `str` | Clean human-readable dataset title | `"InSaAF Indian Legal Statutory Reasoning"` |
| `dataset_id` | `str` | Unique provider-specific identifier | `"crai-iitm/insaaf-ipc-v1"` |
| `source_provider` | `str` | Host repository name | `"huggingface"`, `"zenodo"`, `"uci"`, `"data_gov"`, `"kaggle"` |
| `canonical_url` | `str` | Stable landing or download URL | `"https://huggingface.co/datasets/crai-iitm/insaaf-ipc-v1"` |
| `description` | `str` | Abstract or summary from source | `"Binary statutory reasoning dataset evaluating IPC..."` |
| `domain` | `str` | Substantive application domain | `"legal"`, `"finance"`, `"sociodemographic"`, `"general"` |
| `task_type` | `str` | Machine learning modality or task | `"tabular"`, `"nlp"`, `"classification"`, `"scientific-data"` |
| `geography` | `List[str]` | Geographic scope self-reported by source | `["India"]`, `["Global"]` |
| `languages` | `List[str]` | ISO language codes | `["en"]`, `["hi"]` |
| `documented_demographics` | `List[str]` | Self-reported protected attributes | `["gender", "state", "caste"]` |
| `available_features` | `List[str]` | Column names or feature labels | `["scenario_text", "ipc_section", "label"]` |
| `format` | `str` | Data container format | `"csv"`, `"parquet"`, `"json"`, `"tabular"` |
| `size_bytes` | `Optional[int]` | Total byte size on disk | `1048576` |
| `row_count` | `Optional[int]` | Verified row or record count | `3200` |
| `license` | `str` | Documented licensing terms | `"Apache-2.0"`, `"CC-BY-4.0"`, `"unknown"` |
| `license_verified` | `bool` | True if license confirmed from metadata | `True` |
| `metadata_completeness_score` | `float` | Completeness index $\in [0.0, 1.0]$ | `0.875` |
| `audit_suitability` | `str` | Suitability for Phase 4 gap scan | `"high"`, `"medium"`, `"low"` |
| `audit_suitability_reasons` | `List[str]` | Explicit rationale for suitability score | `["Tabular format supported", "India-centric"]` |
| `verification_status` | `str` | Lineage of metadata | `"verified_api"`, `"fixture"`, `"unverified"` |

---

## 2. Audit Configuration Schema (`AuditConfig` & `AuditDimension`)

### `AuditDimension`
- `name` (`str`): Label for the audit dimension (e.g. `"gender"`, `"state"`, `"caste"`).
- `column_name` (`str`): Corresponding column header in the tabular dataset.
- `dimension_type` (`str`): Categorization (`"demographic"`, `"geographic"`, `"cultural"`, `"custom"`).
- `expected_categories` (`Optional[List[str]]`): List of categories expected in target population.
- `expected_distribution` (`Optional[Dict[str, float]]`): Target population proportions (must sum to ~1.0).
- `min_sample_size` (`int`): Subgroup threshold (default `30`); below this triggers statistical uncertainty warnings.

### `AuditConfig`
- `dimensions` (`List[AuditDimension]`): List of audit dimensions.
- `intersectional_pairs` (`Optional[List[Tuple[str, str]]]`): Pairs of dimension names for 2D cross-tabulation.
- `missing_value_markers` (`List[str]`): Strings treated as missing/unknown (`["", "null", "none", "unknown", "n/a", "?"]`).
- `confidence_level` (`float`): Statistical confidence level for Wilson intervals (default `0.95`).
- `warning_thresholds` (`Dict[str, float]`): Tolerances for missingness (0.15), deviation (0.20), and JSD (0.15).

---

## 3. Dimension Audit Output Schema (`DimensionAuditResult`)

| Field Name | Type | Description |
|---|---|---|
| `dimension_name` | `str` | Configured name of dimension |
| `column_name` | `str` | Audited dataset column |
| `total_records` | `int` | Total rows evaluated |
| `missing_records` | `int` | Count of null, missing, or marker entries |
| `valid_records` | `int` | Rows with valid categorical entries |
| `missing_rate` | `float` | Proportion of records missing $\in [0.0, 1.0]$ |
| `observed_category_count` | `int` | Number of distinct valid categories observed |
| `proportions` | `Dict[str, Dict]` | Map of category $\to$ `{count, share, ci_lower, ci_upper, sample_size_sparse}` |
| `coverage_ratio` | `Optional[float]` | Observed expected categories / Total expected categories |
| `zero_observation_categories`| `List[str]` | Categories in expected list with 0 observations |
| `deviations` | `Optional[Dict[str, float]]` | Difference $\hat{p}_c - q_c$ per category relative to reference |
| `max_abs_deviation` | `Optional[float]` | Maximum absolute difference from reference distribution |
| `js_divergence` | `Optional[float]` | Jensen-Shannon divergence $\in [0.0, 1.0]$ |
| `scorecard` | `Scorecard` | `{completeness_score, coverage_score, parity_score, composite_score, notes}` |
| `warnings` | `List[AuditWarning]` | List of active rule-based warnings triggered |
