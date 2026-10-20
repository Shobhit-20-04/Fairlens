# FairLens: Review-1 Academic Status & Evaluation Report
**Programme:** M.Tech, School of Computer Science and Engineering (SCOPE), VIT Vellore  
**Course:** MASET697 — Project Work (Review-1)  
**Evaluation Rubric:** Problem Relevance (5) | Objectives (10) | Methodology (10)  
**Date:** 2026-10-20  
**Candidate Name:** Shobhit (Reg No: 26MCS0057)  
**Project Workspace:** `D:\fairlens`  
**Git Remote:** `https://github.com/Shobhit-20-04/Fairlens.git` (Private)

---

## 1. Executive Summary for Review Panel

FairLens proposes and delivers a working two-layer fairness framework:
1. **Layer A (General Framework):** An open-source, automated dataset representation-gap auditing framework paired with a multi-source dataset discovery engine.
2. **Layer B (Indian Legal & Financial Fairness Case Study):** An empirical audit of NVIDIA Nemotron 3 Ultra (`nvidia/nemotron-3-ultra-550b-a55b`), investigating whether training data representation skews induce downstream counterfactual outcome flips on Indian statutory (IPC/BNS) and financial regulatory (SEBI/RBI) reasoning tasks.

All four planned Review-1 phases (Phases 1 through 4) have been implemented, tested, and validated in code with a **100% test pass rate across 37 automated tests** and a reproducible, offline end-to-end demonstration.

---

## 2. Alignment with Review-1 Evaluation Rubric

### 2.1 Problem Relevance (5 Marks)
- **High-Stakes AI Deployment in India:** Generative LLMs and legal/financial co-pilots are increasingly used for criminal justice triage, statutory compliance, micro-lending, and insurance advisory. Unmitigated demographic biases in these domains lead to severe allocative harms (e.g. bail denial, discriminatory credit refusal).
- **Western Bias Benchmarks Fail in India:** As established by Sambasivan et al. (ACM FAccT 2021 [R1]) and Indian-BhED (arXiv 2023 [R20]), Western racial categories do not map onto Indian social hierarchies. Caste, religious personal laws, and regional disparities dominate Indian fairness considerations.
- **Unmeasured Model Safety:** NVIDIA's official Content Safety model card for Nemotron lists bias mitigation as `"None"` [R40]. Nemotron 3 Ultra has never been audited for Indian legal and financial reasoning.
- **Gaps in Dataset Discovery:** Existing discovery platforms (Google Dataset Search [R3], Aurum [R4], CHORUS [R24]) optimize purely for keywords and schema similarity, completely omitting demographic and geographic representation scoring.

### 2.2 Objectives (10 Marks)
All four project objectives are clearly defined, measurable, and bounded:
- **Objective 1 (Dataset Auditing):** Build a domain-configurable Python framework that measures representation gaps across demographic, geographic, and cultural dimensions in arbitrary tabular datasets, reporting 95% Wilson confidence intervals, category coverage, and Jensen-Shannon divergence without artificial balance assumptions. *(Delivered & Validated in Phase 4)*.
- **Objective 2 (Dataset Discovery):** Develop a multi-source dataset discovery engine connecting Hugging Face, Zenodo, Data.gov, UCI, and Kaggle with a normalized 20+ field metadata schema, deduplication, and offline fixture fallbacks. *(Delivered & Validated in Phase 3)*.
- **Objective 3 (Auditing Infrastructure & Cost Feasibility):** Construct a resilient inference infrastructure for NVIDIA Nemotron 3 Ultra featuring deterministic SHA-256 caching, exponential backoff, secret masking, and mathematical cost estimation enforcing spending caps ($5.00). *(Delivered & Validated in Phase 2)*.
- **Objective 4 (Literature Traceability & Scope Freeze):** Produce a critical, peer-reviewed literature review (~4,200 words, 12 sections, IEEE citations) establishing six frozen research gaps (G1–G6) supported by primary source evidence. *(Delivered & Validated in Phase 1)*.

### 2.3 Methodology (10 Marks)
FairLens employs a mathematically sound, reproducible methodology:
1. **Representational Gap Metrics (Not Arbitrary Ratios):**
   - *Representation Share* with 95% Wilson Score Confidence Intervals ensuring exact $[0, 1]$ bounds.
   - *Category Coverage* tracking zero-observation groups against documented target populations.
   - *Absolute Deviation & Jensen-Shannon Divergence* when reference distributions exist.
   - *Subgroup Fragility Safeguards:* Explicitly flags subgroups with $N < 30$ to prevent false confidence on sparse data.
2. **Explainable Scoring Framework:**
   - Separates Completeness, Coverage, and Parity scores.
   - **Never silently redistributes weights** when a reference distribution is missing; instead marks parity as `None` and reports descriptive proportions.
3. **Causal Attribution Controls:**
   - For later-stage fine-tuning (Review-2), FairLens defines a **three-way evaluation protocol**: Base Student Model vs. Debiased Fine-Tuned Model vs. Factual Control Model (trained on identical data without demographic perturbation) to prove that bias reduction is attributable to demographic balancing rather than domain knowledge transfer.
   - Distinguishes legally relevant personal law controls (e.g. Hindu Succession Act vs Muslim Personal Law) from impermissible demographic bias.
   - Subtracts the model's intrinsic prompt noise floor from counterfactual flip rates.

---

## 3. Review-1 Demonstrable Progress Matrix

| Work Item | Planned Milestone | Code Status | Automated Tests | Live Demo Status |
|---|---|:---:|:---:|:---:|
| Critical Literature Review (4,200 words) | Phase 1 | **Done** | Cross-check verified | `docs/research/literature_review.md` |
| R1–R52 Reference Verification Ledger | Phase 1 | **Done** | 52/52 verified | `docs/research/reference_verification.csv` |
| Research Gaps G1–G6 Analysis | Phase 1 | **Done** | Supported | `docs/research/research_gaps.md` |
| Settings & Secret Masking Filter | Phase 2 | **Done** | 5 passed | Verified in `run.ps1 api-check` |
| Cached OpenRouter Client & Cache | Phase 2 | **Done** | 4 passed | Verified in `run.ps1 demo` |
| Pricing Ledger & Cost Estimator | Phase 2 | **Done** | 4 passed | Tested with hand calculations |
| Standardized Metadata Schema (20+ fields)| Phase 3 | **Done** | 2 passed | Tested |
| Multi-Source Discovery Adapters (5 repos)| Phase 3 | **Done** | 6 passed | Verified in `run.ps1 demo` |
| Tabular Data Loader (CSV/Parquet/Excel) | Phase 4 | **Done** | 4 passed | Verified |
| Representation Metrics Suite (Wilson/JSD)| Phase 4 | **Done** | 5 passed | Verified |
| Explainable Scorecard & Warning System | Phase 4 | **Done** | 7 passed | Verified in `run.ps1 demo` |
| Offline End-to-End Demo Script | Integration | **Done** | Validated | Reproducible via `run.ps1 demo` |

---

## 4. What Can Be Safely Claimed vs. What Remains Ongoing

### What Can Be Safely Claimed in Review-1:
- A fully functional, tested, and reproducible Python framework for tabular dataset representation-gap auditing exists locally in `src/fairlens`.
- The engine calculates Wilson confidence intervals, category coverage, representation deviations, Jensen-Shannon divergence, missingness rates, and 2D intersectional cross-tabs.
- Multi-source dataset discovery connecting Hugging Face, Zenodo, Data.gov, UCI, and Kaggle is implemented with a normalized metadata schema and error isolation.
- OpenRouter API infrastructure with deterministic SHA-256 caching, pre-execution cost estimation, and mock modes is complete.
- Complete literature review and verification ledger for 52 references is documented with IEEE citations.

### What Must Be Described as Ongoing / Next Steps (Review-2 & Beyond):
- **Nemotron 3 Ultra Live Model Auditing:** Live counterfactual prompt generation and querying of `nvidia/nemotron-3-ultra-550b-a55b` belongs to Review-2.
- **Model Fine-Tuning:** QLoRA fine-tuning of a 3B–4B student model on consumer GPU (RTX 3050 6GB) belongs to Review-2/Phase 5.
- **Evaluation on Benchmark Sets:** IndiaFinBench and InSaAF holdouts will be used strictly as external evaluations in Review-3.
