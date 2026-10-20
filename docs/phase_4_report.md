# FairLens Phase 4 Completion Report: Dataset Representation-Gap Detection
**Milestone:** Phase 4 (Domain-Configurable Representation-Gap Detection Engine)  
**Date:** 2026-10-20  
**Status:** **Done** (All Phase 4 Acceptance Criteria Satisfied)  
**Deliverables Produced:**
1. `src/fairlens/auditing/config.py` (`AuditDimension` and `AuditConfig` models)
2. `src/fairlens/auditing/loader.py` (Safe tabular data ingestion supporting CSV, Parquet, Excel, TSV)
3. `src/fairlens/auditing/metrics.py` (Coverage, Representation Share, Wilson Intervals, Deviation, JSD)
4. `src/fairlens/auditing/scoring.py` (Explainable multi-component scorecards and rule-based warnings)
5. `src/fairlens/auditing/engine.py` (Master `RepresentationAuditEngine` and `AuditReport` generator)
6. `src/fairlens/auditing/cli.py` (Command-line interface for local audits)
7. `tests/fixtures/auditing/` (7 synthetic test fixtures covering balanced, imbalanced, missing categories, nulls, and 1,000-row Indian legal data)
8. `tests/unit/test_auditing_metrics.py` (5 unit tests for formulas, intervals, and JSD)
9. `tests/unit/test_auditing_loader.py` (4 unit tests for formats, duplicates, and file errors)
10. `tests/unit/test_auditing_engine.py` (7 unit tests for all scenario audits, scorecards, and exports)

---

## 1. Acceptance Criteria Verification

| Requirement | Test Suite / Artifact | Result |
|---|---|:---:|
| **Local Local Execution (Zero External APIs)** | `tests/unit/test_auditing_engine.py` | **Passed (7/7 tests)** |
| **Configurable Dimensions & Column Mappings** | `src/fairlens/auditing/config.py` | **Passed** |
| **Wilson Score Confidence Intervals [0, 1]** | `tests/unit/test_auditing_metrics.py` | **Passed** |
| **Category Coverage & Zero-Obs Detection** | `tests/unit/test_auditing_metrics.py` | **Passed** |
| **Explicit Missing & Unknown Value Handling** | `tests/unit/test_auditing_metrics.py` | **Passed** |
| **Representation Deviations & JSD Metric** | `tests/unit/test_auditing_metrics.py` | **Passed** |
| **Explainable Scores (No Silent Reweighting)** | `src/fairlens/auditing/scoring.py` | **Passed** |
| **Rule-Based Warnings with Severity Levels** | `tests/unit/test_auditing_engine.py` | **Passed** |
| **Intersectional Demographic Cross-Tabulation** | `tests/unit/test_auditing_engine.py` | **Passed** |
| **JSON & CSV Report Export** | `tests/unit/test_auditing_engine.py` | **Passed** |

---

## 2. Mathematical Metrics and Formulations

The Phase 4 engine implements mathematically verified metrics without artificial balance assumptions:

### 2.1 Representation Share and Wilson Confidence Interval
For category $c$ with observation count $k$ over valid total $n$:
$$\hat{p} = \frac{k}{n}$$

To ensure exact bounds in $[0.0, 1.0]$ for extreme proportions or small samples, the **Wilson score interval** with continuity correction is computed:
$$\tilde{n} = n + z^2, \quad \tilde{p} = \frac{k + \frac{z^2}{2}}{\tilde{n}}$$
$$\text{Margin} = \frac{z}{\tilde{n}} \sqrt{n \hat{p}(1 - \hat{p}) + \frac{z^2}{4}}$$
$$\text{CI}_{95\%} = \left[\max(0, \tilde{p} - \text{Margin}), \, \min(1, \tilde{p} + \text{Margin})\right]$$
Where $z = \sqrt{2} \cdot \text{erfcinv}(0.05) \approx 1.95996$.

### 2.2 Category Coverage Ratio
When an expected target population category set $E$ is supplied:
$$\text{Coverage Ratio} = \frac{|\{c \in E : \text{count}(c) > 0\}|}{|E|}$$
Zero-observation categories ($c \in E$ with $\text{count}(c) = 0$) are explicitly reported and trigger `WARN_ZERO_OBSERVATION`.

### 2.3 Representation Deviation and Jensen-Shannon Divergence
When a reference distribution $Q$ is configured:
$$\text{Deviation}(c) = \hat{p}_c - q_c$$
$$\text{MaxAbsDeviation} = \max_{c \in E} |\hat{p}_c - q_c|$$
$$\text{JSD}(P \parallel Q) = \frac{1}{2} D_{KL}(P \parallel M) + \frac{1}{2} D_{KL}(Q \parallel M), \quad M = \frac{1}{2}(P + Q)$$
*Note:* If no defensible reference distribution is provided, deviation metrics and parity scores are marked as **Unavailable / Descriptive Only**; target distributions are never fabricated.

---

## 3. Explainable Scoring & Warning Framework

### Scorecard Components (Scale 0 to 100):
1. **Completeness Score:** $100 \times (1.0 - \text{MissingRate})$
2. **Coverage Score:** $100 \times \text{CoverageRatio}$ (None if no expected category list configured)
3. **Parity Score:** $\max(0, 100 \times (1.0 - \text{MaxAbsDeviation}))$ (None if no reference distribution configured)
4. **Composite Score:** Weighted combination $(0.4 \times \text{Coverage} + 0.4 \times \text{Parity} + 0.2 \times \text{Completeness})$ **only computed when all components exist**. The engine never silently redistributes weights.

### Active Warning Registry:
- `WARN_HIGH_MISSINGNESS` (Severity: HIGH/MEDIUM): Missing rate exceeds threshold (15%).
- `WARN_ZERO_OBSERVATION` (Severity: HIGH): Documented category has 0 observations.
- `WARN_SPARSE_SUBGROUP` (Severity: MEDIUM): Subgroup count $N < 30$, statistical confidence interval is wide.
- `WARN_SEVERE_DEVIATION` (Severity: HIGH): Category share deviates by $>20\%$ from reference.
- `WARN_DISTRIBUTION_DIVERGENCE` (Severity: MEDIUM): Jensen-Shannon divergence $>0.15$.

---

## 4. Methodological Interpretation Boundaries (What FairLens Can and Cannot Conclude)

In strict adherence to Section 7.1 and 7.7:
1. **Dataset Balance $\neq$ Model Bias:** An observed demographic skew in a dataset describes its sample composition. It does not prove that a downstream AI model trained on it will exhibit discriminatory outputs.
2. **Context Matters:** Some datasets legitimately feature non-uniform demographic distributions (e.g., specialized medical cohorts, targeted regional surveys). A low parity score flags a statistical deviation from a reference population, not intentional bias.
3. **No Automatic Labelling:** FairLens never infers sensitive attributes from free text or names, preserving privacy and preventing biased heuristic assumptions.
