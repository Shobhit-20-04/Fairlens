# FairLens Frontend Architecture & Backend Integration Guide

**M.Tech Project (MASET697) — SCOPE, VIT Vellore**  
**Review-1 Preparation (20–23 October 2026)**  
**Author:** Shobhit  
**Document Version:** 1.0.0 (Phases 1–4 Integrated Full-Stack)

---

## 1. Executive Summary

This document describes the design, implementation, and integration of the **FairLens** research-grade frontend web interface. The frontend seamlessly connects to the Python backend services created in Phases 1 through 4, providing an interactive, accessible, and reproducible research dashboard for demographic representation auditing and statutory fairness evaluation.

### Key Architecture Highlights
- **Strict Styling Convention:** Styled entirely with **Vanilla CSS and semantic custom properties (design tokens)**. Strictly no Tailwind CSS.
- **Source of Truth:** All mathematical calculations (Wilson score intervals, Jensen-Shannon Divergence, category coverage, and explainable penalty scoring) remain in the Python backend. The frontend acts as a pure presentation and configuration layer.
- **Zero Fabricated Claims:** Layer B (Indian legal and financial fairness evaluation of NVIDIA Nemotron 3 Ultra) is clearly demarcated as a future experimental phase with verified model card specs and zero fabricated benchmark results.
- **Hardware Telemetry:** Direct runtime detection of the user's **NVIDIA GeForce RTX 3050 6GB GPU** (CUDA 12.1) displayed live in the top bar.

---

## 2. Component Hierarchy & Navigation Structure

```
App (Theme Provider: Dark/Light, Polling Health & Hardware Telemetry)
├── Sidebar (Brand, M.Tech Review-1 Badge, Navigation Items)
│   ├── Overview (/)
│   ├── Dataset Discovery (/discovery)
│   ├── Data Profiler (/profiler)
│   ├── Representation Audit (/audit)
│   ├── Reports & Export (/reports)
│   ├── Research Workspace (/research) [Layer B]
│   └── System & Settings (/settings)
└── MainWrapper
    ├── TopBar (Review-1 Badge, Active Dataset Pill, GPU Status, API Status, Theme Toggle)
    └── PageContent (Routed Page Views)
```

---

## 3. Screen Specifications

### 3.1 Overview (`/`)
- **System Telemetry:** Live detection of Python 3.11.9, NVIDIA RTX 3050 6GB VRAM, and offline zero-leakage mode.
- **Two-Layer Architecture Map:** Visual breakdown of Layer A (Universal Dataset Auditing) and Layer B (Indian Legal & Financial Nemotron Case Study).
- **M.Tech Review-1 Rubric:** Explicit mapping to evaluation criteria:
  - *Problem Relevance (5 Marks):* Representation gaps in statutory AI systems.
  - *Objectives (10 Marks):* Wilson CIs, category coverage ratio, explainable scoring.
  - *Methodology (10 Marks):* 52 verified literature references, primary source ledger, deterministic caching.
- **1-Click Demo Launcher:** Dispatches direct audit of the 1,000-case Indian Legal Synthetic dataset.

### 3.2 Dataset Discovery (`/discovery`)
- **Federated Multi-Source Search:** Integrates Phase 3 adapters across Hugging Face Hub, Zenodo (CERN), Data.gov, UCI Machine Learning Repository, and Kaggle.
- **Offline Fixture Toggle:** Allows deterministic, instant demonstration during academic viva without live internet dependencies.
- **Quality & Audit Suitability Badges:** Every result displays an automated suitability score (`HIGH`, `MEDIUM`, `LOW`) evaluating tabular format, geographic relevance, and metadata completeness.
- **Slide-Over Inspection Drawer:** Deep inspection of 20+ standardized metadata attributes and canonical source links.

### 3.3 Data Profiler & Ingestion (`/profiler`)
- **Pre-Loaded Benchmark Fixtures:** 1-click loading of research fixtures (`indian_legal_synthetic_audit.csv`, `balanced.csv`, `imbalanced.csv`, `with_nulls.csv`, `missing_categories.csv`).
- **File Upload Support:** Drag-and-drop support for CSV, Parquet, TSV, and Excel files.
- **Quality Telemetry:** Total rows, feature columns, duplicate rows, duplication rate, and memory footprint.
- **Schema & Quality Table:** Inferred statistical types (`numeric`, `categorical`, `datetime`), null counts, null rates, and sample values.
- **Sample Preview:** Interactive view of the first 20 records.

### 3.4 Representation Audit (`/audit`) — Core Engine Screen
- **Dimension Builder:** Dynamic configuration of demographic, geographic, cultural, and custom dimensions. Supports:
  - Dataset column mapping.
  - Target population distributions (e.g. Census gender or religion proportions).
  - Minimum sample size threshold ($N < 30$ uncertainty flagging).
- **Intersectional Analysis:** 2D cross-tabulation matrix (e.g. `gender × state`) identifying compounded exclusion cells and zero-observation gaps.
- **Scorecards:** Radial gauges displaying:
  - *Completeness Score (0–100):* Data hygiene and missing value penalties.
  - *Category Coverage Score (0–100):* Proportion of expected target categories observed.
  - *Parity Score (0–100):* Alignment against target distribution based on maximum absolute deviation and JSD.
  - *Composite Score (0–100):* Penalty-weighted composite quality.
- **Interactive Wilson 95% Confidence Interval Chart:** Custom SVG graphic rendering observed proportion bars, $[ci_{lower}, ci_{upper}]$ error whiskers, and target reference markers.
- **Severity Warnings:** Severity-coded alerts (`HIGH`, `MEDIUM`, `LOW`) with academic context and actionable remediation hints.

### 3.5 Reports & Export (`/reports`)
- **Executive Audit Summary:** High-level scorecard and dataset overview.
- **Full Markdown Preview:** Complete formatted academic audit report including all statistical breakdowns, warnings, and limitations.
- **Export Actions:** Download structured JSON report or CSV summary with 1-click.

### 3.6 Research Workspace (`/research`) — Layer B
- **Verified Nemotron Specs:** NVIDIA Nemotron 3 Ultra (550B MoE, ~55B active parameters, 1M context window, OpenRouter free tier).
- **Safety Card Findings:** Official NVIDIA content safety documentation recorded: bias mitigation = "None".
- **Pre-Execution Cost Estimator:** Interactive calculator estimating token spend against the $5.00 budget ceiling.
- **Methodology Protocol:** Counterfactual legal vignette construction (IPC/BNS & SEBI/RBI), prompt noise floor isolation, and planned QLoRA 3B–4B fine-tuning.

### 3.7 System & Settings (`/settings`)
- **Secret Masking:** Plaintext secrets are strictly scrubbed (`sk-o...4ab2`, `hf_***`).
- **Provider Status:** Live authentication states for OpenRouter, Hugging Face, Kaggle, Data.gov, and Zenodo.
- **Budget Ceilings:** Central enforcement limits ($5.00 max spend, $2.00 warning threshold).

---

## 4. REST API Endpoint Specifications

The Python backend REST API server (`src/fairlens/server/app.py`) runs on `http://127.0.0.1:5000` and provides:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | System health, version, offline status, GPU & CUDA telemetry |
| `GET` | `/api/settings` | Central application settings with masked secrets and budget limits |
| `GET` | `/api/discovery/providers` | Provider list and authentication status |
| `POST` | `/api/discovery/search` | Federated dataset discovery search |
| `GET` | `/api/profiler/samples` | List pre-loaded research benchmark sample files |
| `POST` | `/api/profiler/profile` | Ingest and profile tabular dataset (schema, nulls, duplicates) |
| `POST` | `/api/audit/run` | Execute multi-dimensional representation-gap audit |
| `POST` | `/api/audit/export` | Export audit report to disk as JSON or CSV |
| `GET` | `/api/research/status` | Layer B Nemotron case study facts, specs, and methodology |
| `POST` | `/api/research/estimate-cost` | Calculate pre-execution API inference costs |

---

## 5. Execution Guide

### 5.1 Run Everything via PowerShell (`run.ps1`)

From `D:\fairlens`:

```powershell
# Run the entire test suite (46 unit tests)
.\run.ps1 test

# Start the Python Flask backend REST API (port 5000)
.\run.ps1 server

# Start the Vite React frontend dev server (port 5173)
.\run.ps1 frontend

# Launch both backend and frontend concurrently in separate windows
.\run.ps1 app
```

### 5.2 Build for Production

```powershell
cd frontend
npm run build
```

Bundle output is generated in `frontend/dist/` in under 500ms with zero errors.
