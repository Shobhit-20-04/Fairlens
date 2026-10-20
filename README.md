# FairLens: A Generalized Fairness Gap-Detection Framework for AI Datasets and Models
### Tested on Nemotron 3 Ultra for Indian Legal and Financial Reasoning

[![M.Tech Project](https://img.shields.io/badge/M.Tech-VIT%20Vellore-blue)](https://vit.ac.in)
[![Course](https://img.shields.io/badge/Course-MASET697%20Project%20Work-brightgreen)]()
[![Review-1 Status](https://img.shields.io/badge/Review--1-Ready-success)]()
[![Python](https://img.shields.io/badge/Python-3.11.9-blue.svg)]()
[![Tests](https://img.shields.io/badge/Tests-46%2F46%20Passing-brightgreen)]()
[![Frontend](https://img.shields.io/badge/Frontend-React%2019%20%2B%20TypeScript-blue)]()
[![Styling](https://img.shields.io/badge/CSS-Vanilla%20Tokens%20(No%20Tailwind)-orange)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

FairLens is an academic research and engineering framework developed as an M.Tech project at the **School of Computer Science and Engineering (SCOPE), VIT Vellore**.

FairLens addresses a critical limitation in current artificial intelligence: **machine learning datasets and commercial foundation models deployed in high-stakes Indian domains lack systematic representation-gap auditing and exhibit unmeasured demographic outcome flips.**

---

## 1. Project Architecture (Two-Layer Design)

FairLens is structured into two complementary layers:

### Layer A — General-Purpose Dataset Representation & Discovery Framework
- **Multi-Source Dataset Discovery Engine:** Connects to Hugging Face Hub, Zenodo, Data.gov, UCI Machine Learning Repository, and Kaggle. Aggregates candidate datasets under a standardized 20+ field schema with URL deduplication and offline fixture support.
- **Domain-Configurable Representation-Gap Audit Engine:** Ingests tabular datasets (CSV, Parquet, TSV, Excel) and computes mathematically grounded metrics:
  - Representation Shares with **95% Wilson Score Confidence Intervals**.
  - **Category Coverage Ratio** tracking zero-observation groups against documented target populations.
  - **Representation Deviations** and **Jensen-Shannon Divergence** relative to reference distributions.
  - **Missing & Unknown Rate** analysis.
  - **2D Intersectional Demographic Analysis** with small-sample ($N < 30$) fragility safeguards.
  - **Explainable Multi-Component Scorecards** (Completeness, Coverage, Parity) with rule-based warnings.

### Layer B — Indian Legal & Financial Fairness Case Study
- **Target Model:** NVIDIA Nemotron 3 Ultra (`nvidia/nemotron-3-ultra-550b-a55b`), whose official Content Safety documentation acknowledges that bias mitigation is `"None"`.
- **Target Domains:** Indian Criminal & Civil Statutory Law (Indian Penal Code / Bharatiya Nyaya Sanhita) and Financial Regulatory Law (SEBI and RBI regulatory directions).
- **Evaluation Design:** Pre-execution cost estimation, deterministic SHA-256 caching, prompt noise floor subtraction, separation of legally relevant personal law controls, and a three-way attribution control study (Base vs. Debiased vs. Factual Control).

---

## 2. Repository Layout

```text
D:\fairlens\
├── README.md                           # Project overview, quickstart, and review summary
├── pyproject.toml                      # Package specifications and dependencies
├── run.ps1                             # Master PowerShell execution entry point
├── .gitignore                          # Strict secret, environment, and cache exclusions
├── .env.example                        # Template for optional API credentials
├── config/                             # Central configuration files
├── docs/                               # Comprehensive project documentation
│   ├── baseline_report.md              # Initial inspection & environment baseline
│   ├── architecture.md                 # System components and data flow
│   ├── frontend_architecture.md        # UI/UX, components, tokens, and REST contracts
│   ├── data_dictionary.md              # Discovery and audit data models
│   ├── testing_strategy.md             # Testing procedures and pass/fail ledger
│   ├── phase_2_report.md               # Infrastructure and feasibility findings
│   ├── phase_3_report.md               # Discovery adapters and schema audit
│   ├── phase_4_report.md               # Representation metrics and validation
│   ├── review_1_status.md              # M.Tech Review-1 rubric alignment
│   ├── progress_log.md                 # Dated work unit log with commit hashes
│   └── research/
│       ├── literature_review.md        # 4,200-word critical literature review (IEEE)
│       ├── reference_verification.csv  # Verification ledger for references R1–R52
│       ├── references.bib              # IEEE-compatible BibTeX database
│       ├── research_gaps.md            # Critical analysis of gaps G1–G6
│       └── phase_1_report.md           # Phase 1 verification audit & frozen scope
├── frontend/                           # Research-Grade React 19 + TypeScript Frontend
│   ├── index.html                      # HTML5 entry with accessible metadata
│   ├── src/
│   │   ├── styles/                     # Pure Vanilla CSS design tokens (NO Tailwind)
│   │   ├── api/                        # Typed REST client and data contracts
│   │   ├── components/                 # TopBar, Sidebar, SVG charts, Scorecard gauges
│   │   ├── pages/                      # 7 core research screens
│   │   └── App.tsx                     # Route management and telemetry polling
│   └── vite.config.ts                  # Vite config with backend API reverse proxy
├── src/
│   └── fairlens/
│       ├── __init__.py
│       ├── config/                     # Settings, environment, and secret masking
│       ├── api/                        # OpenRouter client, cache, pricing engine
│       ├── discovery/                  # Multi-source discovery adapters and engine
│       ├── auditing/                   # Loader, metrics, scoring, and audit engine
│       ├── server/                     # Flask REST API server exposing typed endpoints
│       └── demo.py                     # Master offline end-to-end integration demo
├── tests/
│   ├── fixtures/
│   │   ├── auditing/                   # 7 synthetic test fixtures (balanced, imbalanced, nulls, legal)
│   │   └── discovery/                  # Deterministic multi-repository candidate fixtures
│   └── unit/                           # 9 unit test suites (46 automated tests)
└── outputs/
    └── audit_reports/                  # Exported JSON and CSV audit reports
```

---

## 3. Quickstart & Execution Commands

FairLens is fully operational locally on Windows PowerShell. Zero external API calls or credentials are required for local testing or auditing.

### 3.1 Run All Automated Tests
Runs the complete test suite across all modules and REST endpoints (46 tests):
```powershell
.\run.ps1 test
```
*Expected Result:* `Ran 46 tests in ~2.9s. OK.`

### 3.2 Launch Full-Stack Application
Spawn both the Python Flask REST API server (port 5000) and the Vite React frontend (port 5173):
```powershell
.\run.ps1 app
```
Or start individually:
```powershell
.\run.ps1 server     # Starts Flask REST API on http://127.0.0.1:5000
.\run.ps1 frontend   # Starts Vite React UI on http://localhost:5173
```

### 3.3 Run Offline End-to-End Demonstration
Executes data ingestion, representation audit, structured JSON/CSV export, mock OpenRouter caching, and offline dataset discovery in sequence:
```powershell
.\run.ps1 demo
```

### 3.4 Verify Configuration & Model Pricing
Inspects settings, masks private secrets, and displays live verified pricing for Nemotron 3 Ultra:
```powershell
.\run.ps1 api-check
```

### 3.4 Run Tabular Representation Audit via CLI
Audit an arbitrary CSV or Parquet dataset for representation gaps:
```powershell
.\run.ps1 audit tests/fixtures/auditing/indian_legal_synthetic_audit.csv --dimension gender gender --dimension state state --dimension caste caste_category --export outputs/audit_reports/my_audit.json
```

### 3.5 Run Dataset Discovery Search via CLI
Search for datasets across repositories using keywords:
```powershell
.\run.ps1 discovery "Indian legal financial regulatory" --offline
```

---

## 4. Phase Status Summary (M.Tech Review-1)

| Phase | Description | Status | Verification Evidence |
|---|---|:---:|---|
| **Phase 1** | Literature Review, Reference Ledger & Scope Freeze | **Done** | `docs/research/literature_review.md`, 52/52 verified references, G1–G6 supported. |
| **Phase 2** | Infrastructure, Cached Client & Cost Estimation | **Done** | `src/fairlens/api`, 13 unit tests passed, `$5.00` budget cap verified. |
| **Phase 3** | Multi-Source Dataset Discovery Engine | **Done** | `src/fairlens/discovery`, 5 adapters, 8 unit tests passed, offline fixtures tested. |
| **Phase 4** | Tabular Representation-Gap Detection Engine | **Done** | `src/fairlens/auditing`, 16 unit tests passed, Wilson CI, JSD, explainable scorecards. |
| **Integration** | Offline End-to-End Pipeline Demonstration | **Done** | `src/fairlens/demo.py`, verified via `.\run.ps1 demo`. |

---

## 5. Methodological Principles & Ethics

1. **Descriptive Imbalance $\neq$ Proven Model Discrimination:** Auditing dataset representation measures sample composition. It does not automatically imply that an AI model trained on that dataset will make biased decisions.
2. **Contextual Target Populations:** Not all datasets require 50/50 uniform splits. FairLens only reports representation deviations when a defensible reference distribution is explicitly configured.
3. **No Automatic Demographic Profiling:** FairLens does not use external APIs or heuristics to predict sensitive attributes from names or free text, preserving individual privacy.
4. **Attribution Controls:** Model debiasing is evaluated against factual controls to separate genuine demographic debiasing from domain knowledge transfer.

---

## 6. Author and Academic Information

- **Candidate:** Shobhit (Reg No: 26MCS0057)
- **Programme:** M.Tech, School of Computer Science and Engineering (SCOPE), VIT Vellore
- **Course:** MASET697 — Project Work (Review-1 Milestone)
- **Date:** October 2026
- **Repository:** Private GitHub repository (`https://github.com/Shobhit-20-04/Fairlens.git`)
