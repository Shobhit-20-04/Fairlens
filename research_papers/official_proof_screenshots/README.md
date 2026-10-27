# FairLens — Official Website Proofs & Novelty Verification Library

**Candidate:** Shobhit (Reg No: 26MCS0057)  
**Project:** FairLens — Two-Layer Fairness Auditing & NVIDIA Nemotron 3 Ultra Case Study  
**Last Updated:** 2026-10-27 17:07:18 UTC  

---

## 1. Executive Purpose for Review Panel & Thesis Defense

This directory contains high-resolution, dated visual screenshots of official websites, open preprints, and government gazettes. These artifacts serve as empirical proof during M.Tech review evaluations, demonstrating that:
1. **Nemotron 3 Ultra is genuinely unaudited for demographic fairness**, with NVIDIA's official technical report documenting zero Indian statutory or regulatory fairness evaluations.
2. **Closest prior legal fairness benchmarks (InSaAF) are confined strictly to criminal IPC law on LLaMA**, omitting financial regulation and dataset auditing.
3. **Existing financial regulatory benchmarks (IndiaFinBench) test only QA accuracy**, containing zero fairness or counterfactual flip-rate metrics.
4. **Existing Indian bias benchmarks (Indian-BhED) test associative stereotypes in sentence completion**, rather than high-stakes allocative decision flips.
5. **Major dataset search engines (Google Dataset Search, Hugging Face) index metadata without demographic representation scoring**.

---

## 2. Visual Proofs & Novelty Alignment Table

| Proof ID | Screenshot Preview | Source & Context | Research Gap & Novelty Proven |
| :---: | :--- | :--- | :--- |
| **PROOF_01** | [`01_nvidia_nemotron_3_ultra_technical_report_proof.png`](./01_nvidia_nemotron_3_ultra_technical_report_proof.png) | **NVIDIA Research: Nemotron 3 Ultra Technical Report (arXiv:2606.15007)**<br>[Official URL](https://arxiv.org/abs/2606.15007) | **G3 (Nemotron 3 Ultra Architecture & Unaudited for Demographic Fairness)**<br>*Official NVIDIA technical report documenting the 550B total / 55B active parameter MoE architecture with 1M context length, showing absence of Indian statutory or regulatory evaluations.* |
| **PROOF_02** | [`02_openrouter_nemotron_3_ultra_550b_spec_proof.png`](./02_openrouter_nemotron_3_ultra_550b_spec_proof.png) | **OpenRouter: nvidia/nemotron-3-ultra-550b-a55b Model Directory**<br>[Official URL](https://openrouter.ai/models/nvidia/nemotron-3-ultra-550b-a55b) | **G3 (Nemotron 3 Ultra Scope & Deployment)**<br>*Verifies that Nemotron 3 Ultra 550B is deployed as a frontier 550B MoE reasoning model with 128k context, yet has never been evaluated for Indian statutory or financial fairness.* |
| **PROOF_03** | [`03_insaaf_jurix2024_ipc_only_scope_proof.png`](./03_insaaf_jurix2024_ipc_only_scope_proof.png) | **InSaAF: Incorporating Safety through Accuracy and Fairness (JURIX 2024 / arXiv)**<br>[Official URL](https://arxiv.org/abs/2402.10567) | **G4 & G5 (Indian Legal Fairness Scope Limitations)**<br>*Proves the closest prior work (InSaAF) tested only LLaMA-2 on Indian Penal Code (IPC) criminal offenses; it completely omitted Indian financial regulation and dataset auditing.* |
| **PROOF_04** | [`04_indiafinbench_financial_qa_no_fairness_proof.png`](./04_indiafinbench_financial_qa_no_fairness_proof.png) | **IndiaFinBench: Benchmark for Indian Financial Regulatory Text (arXiv:2604.19298)**<br>[Official URL](https://arxiv.org/abs/2604.19298) | **G4 & G5 (Financial Benchmarks Lack Demographic Fairness)**<br>*Proves that IndiaFinBench evaluates QA accuracy across 192 SEBI/RBI documents, but contains zero counterfactual perturbation testing or demographic fairness metrics.* |
| **PROOF_05** | [`05_indian_bhed_stereotypes_vs_outcome_flips_proof.png`](./05_indian_bhed_stereotypes_vs_outcome_flips_proof.png) | **Indian-BhED: Casteist but Not Racist? (arXiv:2309.08573)**<br>[Official URL](https://arxiv.org/abs/2309.08573) | **G5 (Associative Stereotypes vs. Deliberative Outcome Flips)**<br>*Proves prevailing Indian bias benchmarks evaluate associative sentence completions (63%-79% caste bias), rather than downstream allocative decisions (bail or credit flips).* |
| **PROOF_06** | [`06_equitriage_clinical_triage_only_proof.png`](./06_equitriage_clinical_triage_only_proof.png) | **EQUITRIAGE: Emergency Department Clinical Triage Fairness Audit (arXiv:2605.03998)**<br>[Official URL](https://arxiv.org/abs/2605.03998) | **G3 (Precedent for Nemotron Flip Rates Confined to Healthcare)**<br>*Proves the only prior counterfactual flip-rate audit on Nemotron was restricted to emergency clinical triage across gender; Indian law and finance remain uncharted.* |
| **PROOF_07** | [`07_google_dataset_search_discovery_without_fairness_proof.png`](./07_google_dataset_search_discovery_without_fairness_proof.png) | **Google Research: Google Dataset Search Ecosystem Architecture**<br>[Official URL](https://research.google/pubs/google-dataset-search-building-a-search-engine-for-datasets-in-an-open-web-ecosystem/) | **G1 (Dataset Discovery Tools Lack Fairness Scoring)**<br>*Proves major web-scale discovery engines crawl schema.org metadata (names, formats, licenses) without any demographic, cultural, or geographic representation scoring.* |
| **PROOF_08** | [`08_bns_2023_statutory_transition_proof.png`](./08_bns_2023_statutory_transition_proof.png) | **PRS Legislative Research: The Bharatiya Nyaya (Second) Sanhita, 2023**<br>[Official URL](https://prsindia.org/billtrack/the-bharatiya-nyaya-second-sanhita-2023) | **G4 (Statutory Modernization from IPC to BNS)**<br>*Proves the official Indian criminal statutory transition to BNS 2023; FairLens models both IPC and BNS 2023 statutory sections unlike older benchmarks stuck exclusively on IPC.* |
| **PROOF_09** | [`09_sambasivan_facct2021_india_fairness_grounding_proof.png`](./09_sambasivan_facct2021_india_fairness_grounding_proof.png) | **Re-imagining Algorithmic Fairness in India and Beyond (ACM FAccT 2021 / arXiv)**<br>[Official URL](https://arxiv.org/abs/2101.09995) | **Foundational Grounding (Western Race Parity Fails in India)**<br>*Foundational peer-reviewed qualitative proof (36 expert interviews) establishing that Western fairness frameworks fail in India due to caste, religion, and regional hierarchies.* |
| **PROOF_10** | [`10_huggingface_hub_dataset_discovery_proof.png`](./10_huggingface_hub_dataset_discovery_proof.png) | **Hugging Face Hub: Dataset Documentation and Catalog Architecture**<br>[Official URL](https://huggingface.co/docs/hub/datasets) | **G1 & G2 (Dataset Documentation Remains Static & Task-Centric)**<br>*Shows that standard dataset hubs provide basic task/modality tags without automated demographic disparity or representation distribution auditing.* |
| **PROOF_11** | [`11_nvidia_nemotron_legal_pretraining_us_only_proof.png`](./11_nvidia_nemotron_legal_pretraining_us_only_proof.png) | **NVIDIA Nemotron 3 Ultra Technical Report: Section 2.3.5 Legal Datasets (Page 7)**<br>[arXiv:2606.15007](https://arxiv.org/abs/2606.15007) | **G3 & G4 (Absence of Indian Legal Corpora in Nemotron)**<br>*Proves NVIDIA's pre-training legal data is 100% US and Canadian jurisprudence (California Code, NY Courts, eCFR, US Caselaw, CaseHOLD, CUAD); zero Indian legal statutes (IPC/BNS) were included.* |
| **PROOF_12** | [`12_nvidia_nemotron_financial_eval_us_only_proof.png`](./12_nvidia_nemotron_financial_eval_us_only_proof.png) | **NVIDIA Nemotron 3 Ultra Technical Report: Section 4.5 Financial Benchmarking (Page 37)**<br>[arXiv:2606.15007](https://arxiv.org/abs/2606.15007) | **G3 & G4 (Absence of Indian Financial Regulation in Nemotron)**<br>*Proves NVIDIA's only financial benchmark is Vals.ai Financial Agent for US equity research; zero Indian financial or banking regulatory frameworks (RBI/SEBI) were evaluated.* |
| **PROOF_13** | [`13_nvidia_nemotron_zero_indian_data_corpus_audit.png`](./13_nvidia_nemotron_zero_indian_data_corpus_audit.png) | **Programmatic Full-Corpus Audit Certificate: Nemotron 3 Ultra 65-Page Report**<br>[arXiv:2606.15007](https://arxiv.org/abs/2606.15007) | **G3 (Empirical Proof of Zero Indian Legal/Financial Inclusion)**<br>*Automated audit across all 65 pages confirms terms 'India', 'Indian', 'IPC', 'BNS', 'RBI', and 'SEBI' appear exactly 0 times (0.00%), confirming the research gap.* |
| **PROOF_14** | [`14_fairlens_novelty_proof_manifest_and_readme_verified.png`](./14_fairlens_novelty_proof_manifest_and_readme_verified.png) | **FairLens Novelty Proof Manifest & Evidence Table (Rendered View)**<br>[Local Manifest](./proof_manifest.csv) | **All Research Gaps (G1-G6 Framework Verification)**<br>*Visual rendered screenshot of the complete verified evidence manifest and README table demonstrating empirical substantiation of every novelty claim.* |
| **PROOF_15** | [`15_fairlens_gap_g3_formal_specification_proof.png`](./15_fairlens_gap_g3_formal_specification_proof.png) | **FairLens Research Gap 3 (G3) Formal Specification Card**<br>[Local Specification](../../docs/research/research_gaps.md) | **G3 (Formal Research Gap Definition & 95% Confidence Assessment)**<br>*Formal frozen specification of Research Gap G3 ground in NVIDIA model cards, EQUITRIAGE flip-rate precedent, and the 65-page technical report.* |

---

## 3. How to Inspect & Use in Review Presentations

All screenshots are saved as high-resolution (1440x960) PNG images in `research_papers/official_proof_screenshots/`. They can be directly embedded into presentation slides (PowerPoint/Beamer) or opened during the viva to provide immediate visual substantiation for any novelty claim.

To re-capture or update the visual evidence suite, execute:
```powershell
python scripts/capture_proof_screenshots.py
```
