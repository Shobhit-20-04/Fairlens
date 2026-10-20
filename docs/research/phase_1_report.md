# FairLens Phase 1 Completion & Validation Report: Literature Review and Scope Freeze
**Milestone:** Phase 1 (M.Tech Review-1 Preparation)  
**Date:** 2026-10-20  
**Status:** **Done** (All Phase 1 Acceptance Criteria Satisfied)  
**Deliverables Produced:**
1. `docs/research/literature_review.md` (Critical literature review, ~4,200 words, IEEE citations)
2. `docs/research/reference_verification.csv` (Traceability ledger for all 52 references R1–R52)
3. `docs/research/references.bib` (IEEE-compatible BibTeX database)
4. `docs/research/research_gaps.md` (In-depth analysis of gaps G1–G6 with counterevidence)
5. `docs/research/phase_1_report.md` (This document)

---

## 1. Acceptance Criteria Checklist & Evidence Audit

| Acceptance Criterion | Status | Evidence Location & Verification Notes |
|---|:---:|---|
| **1. Critical Literature Review Exists** | **Passed** | `docs/research/literature_review.md` covers Sections 1 through 12, explicitly differentiating prior art, limitations, and FairLens hypotheses. |
| **2. Reference Verification Ledger** | **Passed** | `docs/research/reference_verification.csv` tracks R1 through R52 with verified venue, author list, DOI/arXiv, and status (`Verified from Primary Source` or `Verified from Abstract/Secondary Source`). |
| **3. Four Priority Papers Verified** | **Passed** | **InSaAF** (arXiv:2402.10567, JURIX 2024), **EQUITRIAGE** (arXiv:2605.03998), **Indian-BhED** (arXiv:2309.08573), and **IndiaFinBench** (arXiv:2604.19298) were inspected from primary author papers/abstracts and verified. |
| **4. Numerical Claims Verified** | **Passed** | - InSaAF: IPC binary statutory reasoning, $LSS_\beta$ formulation verified from paper.<br>- EQUITRIAGE: 43.8% flip rate on Nemotron-3-Super across 18,714 vignettes in MIMIC-IV-ED verified.<br>- Indian-BhED: Caste bias (63%–79%) and religion bias (69%–72%) stereotype preference verified.<br>- IndiaFinBench: 406 QA pairs from 192 SEBI/RBI documents (1992–2026) verified. |
| **5. Six Research Gaps Supported** | **Passed** | `docs/research/research_gaps.md` details G1 through G6 with supporting evidence, counterevidence, confidence ratings, and sensitivity factors. |
| **6. IEEE Citations Cross-Checked** | **Passed** | All 52 references in `references.bib` correspond 1:1 with citations in `literature_review.md` and rows in `reference_verification.csv`. |
| **7. Versioned Scope Frozen** | **Passed** | In-scope and out-of-scope boundaries for Review-1 are finalized in Section 10 of the literature review and Section 2 below. |
| **8. Remaining Literature Backlog Documented**| **Passed** | Catalogued below for ongoing monitoring prior to Review-2. |

---

## 2. Frozen Scope for Review-1 and Phases 1–4

### 2.1 Fixed Research Scope
1. **Core Problem:** Machine learning datasets and commercial foundation models deployed in India lack automated, domain-configurable representation gap detection and suffer from unmeasured counterfactual flip rates in legal and financial reasoning.
2. **Layer A (Dataset Auditing):** Reusable, domain-configurable Python framework calculating Category Coverage, Representation Share, Absolute Representation Deviation, Jensen-Shannon Divergence, Missingness Rates, and bootstrap confidence intervals over tabular datasets. Supported by an offline-capable multi-source discovery engine.
3. **Layer B (Nemotron 3 Ultra Audit):** Target model identified by OpenRouter ID `nvidia/nemotron-3-ultra-550b-a55b`. Prior NVIDIA safety cards list bias mitigation as "None". Focus is on Indian statutory law (IPC/BNS [R52]) and financial regulation (SEBI/RBI [R18]).
4. **Three-Way Evaluation Design:** Later-stage corrective evaluation will evaluate Base Student Model vs. Debiased Fine-Tuned Model vs. Factual Control Model (with legally relevant personal law controls separated from demographic bias).

### 2.2 Explicit Out-of-Scope Items for Phases 1–4
- Full model fine-tuning (QLoRA or LoRA) is strictly out of scope for Phases 1–4.
- Live paid API calls or bulk prompt testing against Nemotron 3 Ultra without prior cost approval.
- Training or fine-tuning on evaluation benchmarks (IndiaFinBench or InSaAF holdouts).
- Scraping or automated demographic profiling of free-text columns without explicit column mapping.

---

## 3. Remaining Literature Backlog (For Monitoring Towards Review-2)

The following references are monitored as preprints or secondary sources whose peer-reviewed journal or conference outcomes should be refreshed during Review-2:
1. **GoalCover (R19):** Monitor for final conference proceedings venue (NeurIPS/ICLR 2026).
2. **DECASTE (R21) & IndiCASA (R22):** Check for peer-reviewed ACL anthology publication updates.
3. **CAFFE (R23):** Verify publication venue following ACM review.
4. **FinTrust (R29) & BFSI-Bench (R36):** Track benchmark release versions on Hugging Face.
5. **NVIDIA Nemotron 3 Ultra Technical Updates:** Track model card updates or subsequent fine-tuned variants released by NVIDIA.
