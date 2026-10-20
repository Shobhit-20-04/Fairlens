# FairLens Research Gaps Analysis: G1 through G6

This document formalizes the six research gaps identified and frozen for the FairLens project, in accordance with Section 4.4 of the FairLens Specification and Review-1 requirements.

Each gap is critically evaluated against current peer-reviewed literature and preprints. To preserve scientific integrity, explicit counterevidence, confidence ratings, and sensitivity conditions are documented.

---

## Gap 1 (G1): Dataset Discovery Tools Lack Systematic Representation and Fairness Scoring

### Statement
Current dataset discovery systems (e.g., Google Dataset Search [R3], Aurum [R4], DataChat [R32], CHORUS [R24], and Pneuma [R25]) index datasets primarily by keywords, semantic similarity, relational schema overlap, or task modality. None of these production or research search engines evaluate who the indexed data includes or leaves out, nor do they calculate standardized demographic, geographic, or cultural representation gap scores.

### Supporting Evidence
- **Google Dataset Search (Noy et al., WWW 2019 [R3]):** Relies entirely on Schema.org structured metadata provided by data publishers. It reports formats, download URLs, and author metadata, but contains zero mechanisms to profile demographic distribution or detect missing social groups.
- **Aurum (Fernandez et al., IEEE ICDE 2018 [R4]):** Utilizes hypergraph data structures to model semantic and structural relationships across relational tables, optimizing purely for relational joining and column similarity.
- **CHORUS (arXiv 2023 [R24]) & Pneuma (arXiv 2025 [R25]):** Apply modern LLM semantic embeddings to convert natural language queries into candidate datasets. However, ranking criteria are restricted to semantic relevance, size, and licensing.
- **Outcome:** A researcher seeking an Indian demographic dataset or a clinical cohort can retrieve datasets that are 95% urban or overwhelmingly male without receiving an automated warning.

### Counterevidence & Competing Work
- General data profiling tools (e.g., Great Expectations, Pandas-Profiling/YData Profiling) compute distribution statistics (entropy, skewness, missingness), but do not contextualize these numbers against demographic or jurisdictional fairness benchmarks.
- Google Data Cards [R2] emphasize downstream suitability, but rely on human documentation rather than automated discovery scoring.

### Confidence Level
**High (90%).** No identified production or published discovery engine computes integrated fairness or demographic gap scores at the time of retrieval.

### What Could Alter This Conclusion
The release of a dataset hub (such as an updated Hugging Face Hub or Kaggle feature) that automatically computes and displays demographic disparity indexes on tabular dataset landing pages.

---

## Gap 2 (G2): Dataset Documentation and Representation Assessment Remain Manual or Task-Specific

### Statement
Standard approaches to dataset transparency (such as Datasheets for Datasets [R31] and Data Cards [R2]) are qualitative, labor-intensive, human-written documents. Automated approaches (such as GoalCover [R19] or Competency Gaps [R27]) are strictly task-specific—measuring token overlap or instruction coverage for a single fine-tuning objective rather than demographic, geographic, or cultural representation balance.

### Supporting Evidence
- **Datasheets for Datasets (Gebru et al., CACM 2021 [R31]):** Proposes a comprehensive questionnaire across dataset lifecycle stages. Adoption surveys indicate that fewer than 5% of open-source datasets possess completed datasheets due to high author friction.
- **Data Cards (Pushkarna et al., ACM FAccT 2022 [R2]):** Standardizes visual summaries of dataset lineage and boundaries, but authors acknowledge that cards require multi-week expert curation.
- **GoalCover (arXiv 2026 [R19]):** Automates subset selection for instruction tuning, but targets coverage of functional task skills (e.g., coding, translation) rather than protected demographic categories.

### Counterevidence & Competing Work
- Fairness libraries such as AIF360 (IBM) and Fairlearn (Microsoft) calculate disparate impact and statistical parity on tabular datasets. However, these tools require pre-labelled binary protected attributes, assume binary outcomes, and lack domain-specific geographic/cultural profiling with statistical uncertainty reporting.

### Confidence Level
**High (85%).** Existing tooling bifurcates between manual qualitative cards and narrow statistical libraries requiring predefined labels, leaving general-purpose configurable representation gap scanning unaddressed.

### What Could Alter This Conclusion
An open-source library that automates demographic and geographic profiling against regional census baselines with built-in confidence intervals for arbitrary tabular schemas.

---

## Gap 3 (G3): Nemotron 3 Ultra Is Unaudited for Indian Legal and Financial Fairness

### Statement
NVIDIA Nemotron 3 Ultra (`nvidia/nemotron-3-ultra-550b-a55b`) has not been subjected to an independent fairness audit within the Indian legal or financial regulatory domains. NVIDIA’s official Content Safety documentation explicitly acknowledges that its safety layer does not mitigate demographic bias, leaving the model's behavior in high-stakes Indian contexts unmeasured.

### Supporting Evidence
- **NVIDIA Nemotron Content Safety Model Card [R40]:** Under "Bias Mitigation Measures", official documentation states `"None"`. The documented safety layer is a fine-tuned classifier trained to intercept overt toxicity, weapons, and self-harm, rather than subtle demographic outcome flips.
- **EQUITRIAGE (Young & Matthews, arXiv 2026 [R17]):** Audited the predecessor model *Nemotron-3-Super* and revealed the highest counterfactual flip rate in the evaluated cohort (43.8% acuity flip under gender swaps in emergency department triage). However, EQUITRIAGE evaluated clinical triage and gender only; it did not evaluate legal or financial reasoning, nor did it evaluate Nemotron 3 Ultra.
- **Nemotron-3-Ultra-550B Technical Report [R26]:** Documents pre-training datasets including `Nemotron-Pretraining-Legal-v1` and `Nemotron-Pretraining-Specialized-v1.2`, but provides zero breakdown of Indian statutory representation (e.g., IPC/BNS, CrPC, SEBI, RBI).

### Counterevidence & Competing Work
- It is possible that proprietary internal evaluations by NVIDIA exist, but no peer-reviewed or public independent audit of Nemotron 3 Ultra on Indian jurisprudence or financial regulation has been published to date.

### Confidence Level
**Very High (95%).** Extensive literature search across Google Scholar, arXiv, and ACL Anthology confirms zero published audits of Nemotron 3 Ultra on Indian legal or financial reasoning.

### What Could Alter This Conclusion
A newly published preprint or benchmark specifically auditing Nemotron 3 Ultra on Indian statutory tasks.

---

## Gap 4 (G4): Indian Legal and Financial Fairness Are Evaluated in Isolation

### Statement
Existing AI fairness evaluations in the Indian context address legal reasoning and financial decision-making in separate silos. No established research framework evaluates whether a single foundational model maintains consistent demographic parity and counterfactual invariance across both legal statutory interpretation and financial regulatory advice.

### Supporting Evidence
- **Indian Legal Fairness Work:** InSaAF (Gupta et al., JURIX 2024 [R7]) evaluates criminal law under the Indian Penal Code (IPC). Girhepuje et al. (SAIL 2023 [R30]) evaluate bail prediction in High Courts. Neither addresses financial transactions, lending, or SEBI/RBI regulations.
- **Indian Financial Work:** IndiaFinBench (arXiv 2026 [R18]) evaluates QA accuracy on 406 SEBI/RBI regulatory pairs. BFSI-Bench (arXiv 2025 [R36]) tests banking domain comprehension. Neither benchmark includes demographic counterfactual perturbation testing or fairness scoring.
- **Global Financial Bias:** Works such as the ACM ICAIF 2025 study [R5] and FinTrust [R29] evaluate financial bias exclusively in US and European regulatory contexts.

### Counterevidence & Competing Work
- Multitask evaluation suites like HELM [R46] evaluate models across diverse subjects, but do not combine Indian statutory law and Indian financial compliance within a unified counterfactual fairness protocol.

### Confidence Level
**High (88%).** No unified cross-domain benchmark connects Indian legal statutory reasoning with Indian financial regulatory fairness.

### What Could Alter This Conclusion
An integrated Indian professional reasoning benchmark that jointly measures legal statutory and financial regulatory fairness.

---

## Gap 5 (G5): Existing Indian Bias Benchmarks Test Stereotypes, Not Downstream Adjudication Outcomes

### Statement
Prevailing Indian NLP bias benchmarks (e.g., Indian-BhED [R20], IndiBias [R14], DECASTE [R21], and IndiCASA [R22]) evaluate token-level associations, masked word probabilities, and overt stereotypical representations. They do not evaluate whether demographic variations alter high-stakes downstream reasoning outcomes (e.g., statutory guilt determinations, loan eligibility, or regulatory compliance assessments).

### Supporting Evidence
- **Indian-BhED (Khandelwal et al., arXiv 2023 [R20]):** Measures whether an LLM completes associative sentences with stereotypical caste (63%–79%) or religious (69%–72%) attributes. It does not evaluate legal guilt or financial creditworthiness.
- **IndiBias (Gupta et al., NAACL 2024 [R14]):** Uses pseudo-log-likelihood scores on masked sentence pairs to evaluate social bias, reflecting linguistic associations rather than multi-step deliberative reasoning.
- **Legal and Financial Reality:** In professional domains, what matters to an affected citizen is not whether a model associates a name with a stereotype in open text, but whether changing an applicant's surname from Sharma to Valmiki flips a statutory liability or credit verdict.

### Counterevidence & Competing Work
- InSaAF [R7] takes an important step by evaluating binary statutory reasoning under the IPC. However, InSaAF tested only base LLaMA models, lacked financial scenarios, and did not incorporate background model noise floor subtractions.

### Confidence Level
**Very High (92%).** The disconnect between association-based stereotype metrics and deliberative outcome-flip metrics in Indian NLP is documented and persistent.

### What Could Alter This Conclusion
A new benchmark that systematically evaluates outcome-flip rates across legal, financial, and administrative domains using causal counterfactual pairs.

---

## Gap 6 (G6): Synthetic Correction Lacks Attribution Controls and Noise Floor Separation

### Statement
While synthetic data generation via Self-Instruct [R38] and Counterfactual Data Augmentation (CDA) [R39] are established techniques, prior attempts to mitigate domain-specific LLM bias rarely isolate the effect of demographic balancing from factual grounding (source attribution). Furthermore, standard evaluations fail to separate genuine demographic flips from baseline stochastic model noise.

### Supporting Evidence
- **Stochastic Model Noise:** Generative LLMs exhibit non-zero output variation across identical prompts run with standard decoding temperatures. If a model has a 12% intrinsic flip rate under identical prompts (prompt noise floor), reporting a 15% flip rate under counterfactual name swapping without baseline subtraction exaggerates demographic bias.
- **Conflation of Grounding and Debias:** InSaAF [R7] and similar fine-tuning studies train on curated legal corpora, but do not employ an attribution control run (training on factual corpus without demographic balancing) to disentangle accuracy gains from bias mitigation.
- **Personal Law Nuances:** In Indian jurisprudence, personal laws governing marriage, succession, and guardianship vary legitimately by religion and custom (e.g., Hindu Succession Act vs. Muslim Personal Law). A naive counterfactual swap that changes religion in a succession scenario will flag a legally mandated difference in outcome as "bias" unless legally relevant statutory controls are separated from discriminatory bias.

### Counterevidence & Competing Work
- In causal inference literature, Kusner et al. [R8] explicitly model causal graphs. However, empirical fine-tuning studies in NLP frequently bypass explicit attribution controls due to computational expense.

### Confidence Level
**High (85%).** Rigorous three-way evaluation (Base Student vs. Debiased Student vs. Factually Grounded Control) with explicit personal law separation is rare in current Indian NLP literature.

### What Could Alter This Conclusion
A published study demonstrating an identical three-way attribution control and noise floor subtraction protocol on Indian legal fine-tuning.

---

## Summary Matrix of Gaps and FairLens Deliverables

| Gap ID | Short Title | FairLens Component / Deliverable | Status in Review-1 |
|---|---|---|---|
| **G1** | Discovery without fairness scoring | Component A (Discovery Engine) + Component B (Audit Layer) | Core Architecture & Adapters Built |
| **G2** | Manual/task-specific dataset auditing | Component B: Domain-configurable representation gap engine | Full Python Engine & Metrics Built |
| **G3** | Nemotron 3 Ultra unaudited for Indian domain | Component C (Dataset Audit) + Component D (Fairness Test) | Feasibility, API Client & Plan Built |
| **G4** | Legal and financial fairness isolated | Cross-domain evaluation suite (IPC/BNS + SEBI/RBI) | Frozen Scope & Benchmark Specifications |
| **G5** | Stereotype metrics vs. outcome flips | Counterfactual flip-rate metric with paired cases | Metric Formulation & Scoring Engine Built |
| **G6** | Missing attribution controls and noise floors | Three-way evaluation design (Base vs. Debiased vs. Control) | Experimental Protocol Formalized |
