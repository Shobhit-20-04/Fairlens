# FairLens Testing Strategy and Verification Ledger

This document formalizes the testing methodology, automated test suites, execution procedures, and observed validation outcomes across FairLens Phases 1 through 4.

---

## 1. Testing Philosophy & Non-Negotiable Rules

In accordance with Section 2 of the FairLens Specification:
1. **Never Report Fabricated Outcomes:** Every test result recorded in this document reflects an actual executed command on Python 3.11.9 (Windows PowerShell).
2. **Zero-Network Default:** All test suites run locally without external network dependencies, using deterministic fixtures or mock modes.
3. **No Commits on Broken Code:** Git commits are pushed only after test suites achieve a 100% pass rate.

---

## 2. Test Architecture and Inventory

```
tests/
├── __init__.py
├── fixtures/
│   ├── auditing/
│   │   ├── balanced.csv                      (50/50 balanced test cases)
│   │   ├── imbalanced.csv                    (90/10 skewed test cases)
│   │   ├── missing_categories.csv            (Omitted target group test cases)
│   │   ├── with_nulls.csv                    (Missingness markers & nulls)
│   │   ├── single_category.csv               (Single-class edge cases)
│   │   ├── empty.csv                         (0-row empty dataset)
│   │   └── indian_legal_synthetic_audit.csv  (1,000-row multi-dimensional Indian legal data)
│   └── discovery/
│       └── sample_datasets.json              (Deterministic multi-repository fixtures)
└── unit/
    ├── test_config.py                        (Settings validation & secret masking filter)
    ├── test_api_client.py                    (OpenRouter client, caching, and auth checks)
    ├── test_pricing.py                       (Cost estimation formulas and budget gating)
    ├── test_discovery_schema.py              (Metadata normalization & suitability scoring)
    ├── test_discovery_engine.py              (Discovery search, deduplication, error isolation)
    ├── test_auditing_loader.py               (Tabular file formats, duplicates, and file errors)
    ├── test_auditing_metrics.py              (Wilson intervals, coverage, deviation, JSD)
    ├── test_auditing_engine.py               (End-to-end representation audits & reports)
    └── test_server.py                        (Flask REST API endpoints and error isolation)
```

---

## 3. Actual Test Execution Outcomes (Observed Ledger)

**Command Executed:**
```powershell
$env:PYTHONPATH="src"; python -m unittest discover -s tests -p "test_*.py" -v
```

**Observed Result:** `Ran 46 tests in 2.903s. OK.`

| Test Module | Test Case Name | Objective / Scenario | Status |
|---|---|---|:---:|
| `test_config.py` | `test_default_settings` | Verifies default configuration populated | **Passed** |
| `test_config.py` | `test_validation_errors` | Rejects negative timeout, retries, and token prices | **Passed** |
| `test_config.py` | `test_secret_masking_in_repr` | Masks keys (`sk-...`, `hf_...`) in `repr()` | **Passed** |
| `test_config.py` | `test_secret_masking_filter` | Redacts sensitive tokens from log records | **Passed** |
| `test_config.py` | `test_has_openrouter_credentials` | Checks placeholder vs valid API key presence | **Passed** |
| `test_api_client.py` | `test_mock_completion` | Returns structured completion in mock mode | **Passed** |
| `test_api_client.py` | `test_cache_hit_and_miss` | Verifies deterministic SHA-256 cache hit/miss | **Passed** |
| `test_api_client.py` | `test_cache_invalidation_and_clear`| Deletes single cache key and clears cache dir | **Passed** |
| `test_api_client.py` | `test_live_network_without_credentials_raises_auth_error` | Throws `FairLensAuthenticationError` without credentials | **Passed** |
| `test_pricing.py` | `test_known_calculation_values` | Tests exact hand-calculated cost formulas | **Passed** |
| `test_pricing.py` | `test_cache_hit_rate_reduction` | Verifies cache hit rate scales billable requests | **Passed** |
| `test_pricing.py` | `test_free_tier_pricing` | Verifies free tier endpoint estimates $0.00 | **Passed** |
| `test_pricing.py` | `test_budget_exceeded_raises_error` | Throws `FairLensBudgetExceededError` when spend > $5 | **Passed** |
| `test_discovery_schema.py` | `test_completeness_scoring` | Tests metadata completeness calculation | **Passed** |
| `test_discovery_schema.py` | `test_to_dict_serialization` | Verifies schema dictionary serialization | **Passed** |
| `test_discovery_engine.py` | `test_fixture_search_and_keyword_match`| Matches keywords across offline fixtures | **Passed** |
| `test_discovery_engine.py` | `test_domain_and_geography_filtering` | Applies secondary domain & geography filters | **Passed** |
| `test_discovery_engine.py` | `test_deduplication` | Removes duplicate records with identical URLs | **Passed** |
| `test_discovery_engine.py` | `test_pagination` | Tests offset and limit slicing | **Passed** |
| `test_discovery_engine.py` | `test_provider_error_isolation` | Failing adapter does not crash search engine | **Passed** |
| `test_discovery_engine.py` | `test_export_json_and_csv` | Exports discovery results to JSON and CSV | **Passed** |
| `test_auditing_loader.py` | `test_load_valid_csv` | Ingests CSV and returns profiling dictionary | **Passed** |
| `test_auditing_loader.py` | `test_load_empty_file_raises_value_error` | Rejects 0-row empty dataset | **Passed** |
| `test_auditing_loader.py` | `test_nonexistent_file_raises_error` | Throws FileNotFoundError on missing file | **Passed** |
| `test_auditing_loader.py` | `test_unsupported_extension_raises_error` | Rejects non-tabular extensions | **Passed** |
| `test_auditing_metrics.py` | `test_missing_rate_calculation` | Counts nulls, markers, and valid records | **Passed** |
| `test_auditing_metrics.py` | `test_wilson_interval_bounds` | Bounds Wilson intervals strictly within [0, 1] | **Passed** |
| `test_auditing_metrics.py` | `test_category_coverage` | Computes coverage and zero-observation groups | **Passed** |
| `test_auditing_metrics.py` | `test_representation_deviations_and_jsd` | Computes deviations and Jensen-Shannon divergence | **Passed** |
| `test_auditing_metrics.py` | `test_intersectional_matrix` | Cross-tabulates 2D pairs and flags sparse cells | **Passed** |
| `test_auditing_engine.py` | `test_balanced_dataset_audit` | Parity score = 100, zero warnings on balanced data | **Passed** |
| `test_auditing_engine.py` | `test_imbalanced_dataset_triggers_severe_deviation_warning` | Triggers WARN_SEVERE_DEVIATION on 90/10 skew | **Passed** |
| `test_auditing_engine.py` | `test_missing_category_triggers_zero_obs_warning` | Triggers WARN_ZERO_OBSERVATION on omitted group | **Passed** |
| `test_auditing_engine.py` | `test_high_missingness_triggers_warning` | Triggers WARN_HIGH_MISSINGNESS on >15% nulls | **Passed** |
| `test_auditing_engine.py` | `test_no_reference_distribution_omits_parity_score` | Parity score is None when no reference provided | **Passed** |
| `test_auditing_engine.py` | `test_realistic_indian_legal_audit_and_intersectional` | Audits 1,000-row Indian legal dataset | **Passed** |
| `test_auditing_engine.py` | `test_export_audit_report` | Exports audit reports to JSON and CSV | **Passed** |
| `test_server.py` | `test_health_check` | Returns healthy status and GPU telemetry | **Passed** |
| `test_server.py` | `test_settings_view` | Returns masked secrets and budget limit | **Passed** |
| `test_server.py` | `test_discovery_providers` | Lists discovery adapters and statuses | **Passed** |
| `test_server.py` | `test_discovery_search` | Executes federated search across mock fixtures | **Passed** |
| `test_server.py` | `test_profiler_samples` | Retrieves pre-loaded benchmark fixtures | **Passed** |
| `test_server.py` | `test_profiler_profile` | Ingests dataset, schema, nulls, duplicates | **Passed** |
| `test_server.py` | `test_audit_run_and_export` | Executes audit via REST, exports JSON/CSV | **Passed** |
| `test_server.py` | `test_research_status` | Returns Layer B case study specs and facts | **Passed** |
| `test_server.py` | `test_cost_estimator` | Computes token spend against budget ceiling | **Passed** |

**Summary:** 46/46 tests passed (100% pass rate).
