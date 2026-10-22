# FairLens — Research Paper Library Audit & Download Summary

**Execution Timestamp:** 2026-10-22 14:39:06 UTC  
**Total References in Manifest:** 55  
**PDFs Downloaded and Validated:** 48  
**PDFs Reused (Already Correct):** 47  
**PDFs Renamed from Verified Titles:** 1  
**Paywalled / Physical Books (Requiring Library Access):** 2  
**Official Web Specifications & API Docs:** 5  
**Failed Downloads:** 0  

---

## Category Breakdown

| Category | Directory | Verified Papers | Downloaded PDFs |
| :--- | :--- | :---: | :---: |
| **01_Indian_Fairness_and_Bias** | `research_papers/01_Indian_Fairness_and_Bias/` | 5 | 5 |
| **02_Indian_Legal_NLP** | `research_papers/02_Indian_Legal_NLP/` | 7 | 7 |
| **03_Financial_Fairness_and_Benchmarks** | `research_papers/03_Financial_Fairness_and_Benchmarks/` | 6 | 6 |
| **04_Counterfactual_Fairness** | `research_papers/04_Counterfactual_Fairness/` | 5 | 5 |
| **05_Dataset_Discovery_and_Documentation** | `research_papers/05_Dataset_Discovery_and_Documentation/` | 10 | 6 |
| **06_Fine_Tuning_and_Synthetic_Data** | `research_papers/06_Fine_Tuning_and_Synthetic_Data/` | 6 | 6 |
| **07_Legal_Reasoning_and_Evaluation** | `research_papers/07_Legal_Reasoning_and_Evaluation/` | 7 | 7 |
| **08_Nemotron_and_NVIDIA** | `research_papers/08_Nemotron_and_NVIDIA/` | 3 | 1 |
| **09_Clinical_Triage_and_Related_Work** | `research_papers/09_Clinical_Triage_and_Related_Work/` | 1 | 1 |
| **10_Other_References** | `research_papers/10_Other_References/` | 5 | 4 |

---

## Papers Requiring Institutional / VIT Library Access

The following foundational publications are published under commercial or proprietary licenses and cannot be downloaded via open-access endpoints:

1. **Aurum: A Data Discovery System**  
   - Authors: Raul Castro Fernandez, Ziawasch Abedjan, Famien Koko, Gina Yuan, Samuel Madden, Michael Stonebraker (2018)  
   - Venue: IEEE 34th International Conference on Data Engineering (ICDE)  
   - Official Link: [https://doi.org/10.1109/icde.2018.00094](https://doi.org/10.1109/icde.2018.00094)  
   - Access Requirement: VIT Library subscription (IEEE Xplore / Book Access)  

1. **The Alignment Problem: Machine Learning and Human Values**  
   - Authors: Brian Christian (2020)  
   - Venue: W. W. Norton & Company (Book)  
   - Official Link: [https://wwnorton.com/books/9780393635829](https://wwnorton.com/books/9780393635829)  
   - Access Requirement: VIT Library subscription (IEEE Xplore / Book Access)  

---

## Integrity & Structural Validation

All downloaded PDF files were inspected with `pypdf` to ensure:
1. File begins with valid PDF magic bytes (`%PDF-`).
2. File size exceeds minimum payload threshold (> 1 KB; average paper is 0.5 MB - 3 MB).
3. Page 1 text stream and document metadata were extracted without PDF syntax errors.
4. Filenames strictly adhere to Windows-safe naming conventions without illegal characters.
5. SHA-256 cryptographic hashes are recorded for reproducible provenance tracking.
