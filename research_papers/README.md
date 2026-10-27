# FairLens Research Papers Library

This directory contains the curated, verified, and organized research paper collection supporting the M.Tech project **FairLens** (Finding and Fixing Fairness Gaps in AI Datasets and Models, Tested on Nemotron 3 Ultra for Indian Legal and Financial Reasoning).

## Directory Structure

```text
D:\fairlens\research_papers\
├── 00_Priority_Reading/                  # Ranked pointers to top foundational papers
├── 01_Indian_Fairness_and_Bias/          # Caste, religion, and regional Indian bias benchmarks
├── 02_Indian_Legal_NLP/                  # Indian Penal Code (IPC), BNS, and court judgment corpora
├── 03_Financial_Fairness_and_Benchmarks/ # Indian SEBI/RBI financial regulatory benchmarks
├── 04_Counterfactual_Fairness/           # Causal fairness theory and counterfactual perturbation
├── 05_Dataset_Discovery_and_Documentation/ # Metadata schemes, Data Cards, and catalog search
├── 06_Fine_Tuning_and_Synthetic_Data/    # LoRA, QLoRA, distillation, and data synthesis
├── 07_Legal_Reasoning_and_Evaluation/    # LegalBench, hallucination profiling, and LLM-as-a-judge
├── 08_Nemotron_and_NVIDIA/               # Nemotron 3 Ultra technical reports and model cards
├── 09_Clinical_Triage_and_Related_Work/  # EQUITRIAGE clinical triage flip-rate methodology
├── 10_Other_References/                  # General LLM surveys and foundation model risks
├── official_proof_screenshots/          # High-resolution dated visual proof from official websites
├── metadata/                             # Inventory CSV, reading list, and summary reports
└── download_logs/                        # Timestamped provenance and download logs
```

## Visual Proofs of Novelty

A dedicated collection of 10 high-resolution, dated visual screenshots is maintained in `official_proof_screenshots/` with an accompanying manifest (`proof_manifest.csv` and `README.md`). These artifacts prove that:
- Nemotron 3 Ultra is unaudited for demographic fairness with official model cards stating `Bias Mitigation: "None"`.
- InSaAF (JURIX 2024) is confined to criminal law (IPC) on LLaMA-2 without financial regulations or dataset auditing.
- IndiaFinBench evaluates QA accuracy without counterfactual perturbation or fairness testing.
- Existing Indian benchmarks (Indian-BhED) test associative stereotypes rather than high-stakes allocative decision flips.
- Major dataset search engines index metadata without representation gap scoring.

## Naming Convention

Every downloaded PDF is renamed using its **verified full document title**, formatted for Windows compatibility:
- Spaces are converted to single underscores (`_`).
- Windows-invalid characters (`\ / : * ? " < > |`) are stripped.
- Consecutive punctuation is normalized.
- Example: `1703.06856.pdf` -> `Counterfactual_Fairness.pdf`.

## Metadata Inventory

The complete paper registry is maintained in `metadata/paper_inventory.csv` with 22 structured columns:
`paper_id`, `exact_title`, `authors`, `year`, `venue`, `doi`, `arxiv_id`, `official_url`, `pdf_source_url`, `original_filename`, `final_filename`, `verified_document_title`, `local_pdf_path`, `research_category`, `relevance_to_fairlens`, `access_status`, `download_status`, `verification_status`, `rename_status`, `duplicate_of`, `sha256`, `notes`.

## How to Rerun the Workflow Safely

The pipeline is fully idempotent, resumable, and safe against duplicate downloads. To re-audit and download any newly added papers, execute:

```powershell
python scripts/paper_collector.py
```

To re-capture or update the visual evidence screenshots, execute:

```powershell
python scripts/capture_proof_screenshots.py
```
