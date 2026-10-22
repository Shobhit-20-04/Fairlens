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
├── metadata/                             # Inventory CSV, reading list, and summary reports
└── download_logs/                        # Timestamped provenance and download logs
```

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

Existing valid PDFs are checked against their SHA-256 hashes and reused without unnecessary network downloads.
