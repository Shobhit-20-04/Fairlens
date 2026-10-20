# FairLens: A Generalized Fairness Gap-Detection Framework for AI Datasets and Models
### Demonstrated by Auditing and Correcting Nemotron 3 Ultra for Indian Legal and Financial Reasoning

---

## 1. Project Overview

FairLens is a two-layer system:

- **Layer 1 (General Framework)** — a reusable tool that lets anyone search for datasets in plain language, and scores any dataset for representation/fairness gaps (demographic, geographic, cultural).
- **Layer 2 (Case Study)** — a rigorous application of that same gap-detection method to a real, current problem: testing whether NVIDIA's self-disclosed gaps in Nemotron 3 Ultra actually affect its Indian legal and financial reasoning, then fixing what's found.

Everything below is grouped by the actual components that will exist in the finished project — code modules, datasets, models, documents, and outputs.

---

## 2. Component A — Dataset Discovery Engine

**Purpose:** Let a user describe a dataset need in plain language and get real, matching datasets back.

**What's inside it:**
- **Query parser (LLM-based):** Takes a free-text description ("I need X-ray images labeled for pneumonia") and extracts structured search parameters — domain, data type/modality, task type, minimum size, license needs.
- **Multi-source connectors:** Independent modules that query each external source's API/catalog:
  - Hugging Face Hub API (`huggingface_hub` Python library)
  - Kaggle API
  - UCI Machine Learning Repository (scraped/indexed, no formal API)
  - data.gov API
  - Zenodo API
- **Metadata indexer:** Periodically crawls all five sources and stores dataset metadata (title, description, tags, size, format, license, last updated) locally, so live queries don't hit external APIs every time.
- **Semantic search layer:** Converts dataset descriptions and the user's query into embeddings (via `sentence-transformers`) and finds nearest matches using a vector database (FAISS or ChromaDB), combined with keyword filtering.
- **Result ranker:** The LLM re-scores the top candidate datasets for actual relevance and eliminates poor matches (wrong modality, too small, incompatible license).

**Output:** A ranked list of matching datasets, each with a direct download link (not just a webpage), source, size, and license.

---

## 3. Component B — Gap-Detection Layer (the "Fairness" in FairLens)

**Purpose:** For any dataset returned by Component A (or fed in directly), assess how well it represents different demographic, geographic, and cultural groups.

**What's inside it:**
- **Metadata-based gap scan:** Checks available demographic/geographic fields (where present) for skew — e.g., gender balance, ethnicity mentions, country/language coverage.
- **Content-based gap scan:** For text datasets without explicit demographic labels, uses an LLM to sample and classify a subset of entries for implicit demographic/cultural signals (names, locations, framing) and estimates representation ratios.
- **Gap report generator:** Produces a structured score/report: what's well-covered, what's thin or missing, and a plain-language summary of risk ("this dataset is 80% Western-context text; use with caution for non-Western applications").
- **Recommendation layer:** If gaps are severe, suggests either an alternative dataset from Component A's index, or flags the dataset as a candidate for the synthetic-correction pipeline (Component E).

**Output:** A gap report per dataset — this is the general-purpose deliverable usable by anyone, any domain.

---

## 4. Component C — Nemotron 3 Ultra Dataset Audit (Case Study, Part 1)

**Purpose:** Apply Component B directly to NVIDIA's own released datasets tied to Nemotron 3 Ultra.

**What's inside it:**
- Download and run the gap-detection layer against:
  - **Nemotron-Pretraining-Legal-v1**
  - **Nemotron-Pretraining-Specialized-v1.2** (moral/ethical scenario data)
  - Relevant slices of **Nemotron-Posttraining-v3**
- **Jurisdiction/domain coverage analysis:** Specifically checks how much of the legal dataset touches Indian statutes, case law, or Indian financial regulation, versus US/generic/Western legal content.
- **Documentation of findings:** A quantified table — e.g., "X% of legal documents are US-jurisdiction, Y% mention Indian law, Z% are ambiguous."

**Output:** A written, numbers-backed audit report of exactly what's missing in Nemotron's own legal/ethics data, specifically for the Indian context.

---

## 5. Component D — Live Model Fairness Testing (Case Study, Part 2)

**Purpose:** Test the actual model (not just its training data) for bias in its outputs.

**What's inside it:**
- **Counterfactual test-case generator:** Builds pairs/sets of otherwise-identical legal and financial questions, varying only irrelevant details — names (Indian vs. Western), gender, regional framing (e.g., a contract dispute framed in a North Indian vs. South Indian context).
- **Query runner:** Sends all test cases to Nemotron 3 Ultra via the OpenRouter API and logs responses.
- **Flip-rate analyzer:** Measures how often the model's answer, confidence, or tone changes when only the irrelevant demographic detail changes — the core fairness metric (same method used in prior audits of sibling model Nemotron-3-Super).
- **Political/cultural framing probe:** A separate test set specifically designed to check whether India-specific political or cultural framing slips past NVIDIA's disclosed regex-based bias filter (since that filter was reportedly tuned on more US/Western-centric political content).

**Output:** A fairness scorecard for the base (un-fine-tuned) model — flip rates, example failures, and filter-bypass cases.

---

## 6. Component E — Corrective Synthetic Dataset Generator

**Purpose:** Generate new training data that specifically targets the gaps found in Components C and D.

**What's inside it:**
- **Seed corpus collector:** Gathers real, verifiable Indian legal/financial source material (public court judgments, bare acts, financial regulations) to ground generation in fact, not hallucination.
- **Teacher-model generation pipeline:** Prompts Nemotron 3 Ultra (or another available teacher model) to generate structured reasoning traces — QA pairs, issue-spotting exercises, statute application examples — tied to the seed material.
- **Balance-aware generation:** Explicitly generates counterfactual-balanced examples (same scenario, varied names/genders/regions) to directly counter the flip-rate problems found in Component D.
- **Validation filter:** Manual or semi-automated review of a sample of generated data to catch legal/factual errors before it's used for training — critical, since flawed synthetic legal data teaches confident wrongness.

**Output:** A cleaned, verified, bias-corrective training dataset (India-specific legal/financial reasoning).

---

## 7. Component F — Fine-Tuning Pipeline

**Purpose:** Train a small model on the corrective dataset and prove the fix works.

**What's inside it:**
- **Base student model:** A 3B–8B parameter open model (e.g., Llama-3-8B, Phi-3-mini, or Nemotron Nano).
- **QLoRA fine-tuning setup:** 4-bit quantized fine-tuning via PEFT + bitsandbytes (or Unsloth for extra memory efficiency), sized to run on a single consumer GPU.
- **Training run tracking:** Logs loss curves, hyperparameters, and checkpoints for reproducibility.

**Output:** A fine-tuned small model specialized for fairer Indian legal/financial reasoning.

---

## 8. Component G — Evaluation & Comparison

**Purpose:** Prove, with numbers, whether the correction actually worked.

**What's inside it:**
- **Benchmark set:** A held-out set of Indian legal/financial questions, separate from training data.
- **Three-way comparison:** Base student model (no fine-tuning) vs. fine-tuned student model vs. Nemotron 3 Ultra teacher — scored on accuracy, citation/fact correctness, and hallucination rate.
- **Re-run of Component D's counterfactual suite** on the fine-tuned model, to directly compare flip rates before and after correction.
- **Results tables and plots** summarizing all of the above.

**Output:** The core evidence chapter of your report — did the fix work, and by how much.

---

## 9. Component H — User-Facing Interface (the "chatbot")

**Purpose:** Tie Components A, B, and E together into something usable, not just backend scripts.

**What's inside it:**
- **Chat interface (web-based):** User types a plain-language dataset request or asks to audit a specific dataset.
- **Backend (FastAPI):** Routes requests to the discovery engine (A), gap-detection layer (B), or serves the corrective dataset (from E) directly.
- **Download trigger:** Once a dataset/link is selected, the frontend auto-triggers the download rather than just displaying a link to click through multiple pages.

**Output:** A working demo application — this is what you'd actually show in a viva/demo.

---

## 10. Supporting Documents (non-code deliverables)

- **Literature review** — covering LLM-based dataset search (CHORUS, Pneuma, DataChat), gap-detection precedent (GoalCover, Competency Gaps), and fairness-audit methodology (EQUITRIAGE-style counterfactual testing).
- **Nemotron dataset audit report** (from Component C).
- **Fairness scorecard** (from Component D, run twice — before and after correction).
- **Final project report** — methodology, results, limitations, and future work.
- **Presentation/demo materials.**

---

## 11. Tech Stack Summary

| Purpose | Tool/Library |
|---|---|
| LLM access | Nemotron 3 Ultra via OpenRouter API |
| Dataset APIs | `huggingface_hub`, Kaggle API, UCI scraping, data.gov API, Zenodo API |
| Embeddings/search | `sentence-transformers`, FAISS or ChromaDB |
| Backend | Python, FastAPI |
| Frontend | React (or simple HTML/JS chat UI) |
| Fine-tuning | PEFT, bitsandbytes / Unsloth, QLoRA |
| Evaluation | Custom benchmark scripts, pandas/matplotlib for reporting |

---

## 12. Final Deliverables Checklist

- [ ] Working dataset discovery + gap-detection tool (web app)
- [ ] Nemotron 3 Ultra dataset audit report
- [ ] Counterfactual fairness test suite (reusable code)
- [ ] Fairness scorecard: base model
- [ ] Corrective synthetic dataset (Indian legal/financial)
- [ ] Fine-tuned small model
- [ ] Fairness scorecard: fine-tuned model (comparison)
- [ ] Final written report + literature review
- [ ] Demo presentation
