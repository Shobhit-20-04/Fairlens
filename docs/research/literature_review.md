# FairLens: Critical Literature Review and Conceptual Foundations
**Programme:** M.Tech, School of Computer Science and Engineering (SCOPE), VIT Vellore  
**Course:** MASET697 — Project Work (Review-1 Preparation)  
**Target Milestone:** Review-1 (October 2026)  
**Citation Convention:** IEEE Citation Format [R1]–[R52]

---

## 1. Introduction and Motivation

The rapid deployment of generative foundation models and Large Language Models (LLMs) across high-stakes domains marks a structural shift in automated decision support. In jurisdictions such as India, conversational AI systems, legal co-pilots, and automated financial advisory tools are increasingly accessed by ordinary citizens seeking legal triage, statutory interpretation, micro-lending guidance, and regulatory compliance assistance. Unlike general consumer applications where factual or demographic errors cause minor inconvenience, errors in legal and financial contexts carry allocative and legal consequences. Inaccurate or discriminatory outputs risk denial of bail, misinterpretation of fundamental rights, unfair credit allocation, and systemic exclusion of historically marginalized groups.

Despite widespread claims of alignment and safety in commercial foundation models, empirical research has repeatedly demonstrated that standard safety filters and reinforcement learning from human feedback (RLHF) reflect predominantly Western values, legal precedents, and demographic categories. When deployed in the Global South, these models encounter deeply ingrained socio-cultural structures—including caste, religious personal laws, linguistic diversity, and regional economic disparities—that cannot be captured by Western binaries such as Caucasian versus African-American racial categories.

This research project, titled **FairLens**, addresses this critical gap through a two-layer investigative framework:
1. **Layer A (General-Purpose Dataset Representation and Gap Auditing):** A domain-configurable, automated framework designed to inspect, profile, and score datasets for demographic, geographic, and cultural representation gaps prior to model training or fine-tuning, complemented by a multi-source dataset discovery engine.
2. **Layer B (Indian Legal and Financial Fairness Case Study):** A targeted, empirical audit of NVIDIA Nemotron 3 Ultra (`nvidia/nemotron-3-ultra-550b-a55b`), evaluating whether pre-training data deficiencies translate into systematic counterfactual flip rates across Indian statutory (IPC/BNS) and financial regulatory (SEBI/RBI) tasks, followed by source-grounded synthetic correction and parameter-efficient fine-tuning.

This review synthesizes existing research across dataset discovery, data documentation, algorithmic fairness, Indian socio-cultural representation, legal/financial NLP, and parameter-efficient model alignment, establishing the six foundational research gaps that justify FairLens.

---

## 2. Dataset Discovery and Dataset Quality Assessment

### 2.1 State of Prior Research
The volume of machine learning datasets published across open repositories has grown exponentially. Early enterprise data discovery systems, such as **Aurum** (Fernandez et al., IEEE ICDE 2018 [R4]), established foundational techniques for indexing large-scale relational repositories using hypergraph representations. Aurum constructs syntactical, semantic, and structural links across table schemas, enabling users to identify candidate join paths and find duplicate or complementary tabular data across heterogeneous corporate databases.

With the advent of web-scale data repositories, **Google Dataset Search** (Noy et al., WWW 2019 [R3]) established a decentralized discovery ecosystem. By ingesting structured metadata conforming to the Schema.org vocabulary (`schema.org/Dataset`) crawled across thousands of independent institutional repositories, Google Dataset Search made millions of datasets searchable through keyword queries, tracking licenses, authors, and download links.

More recently, natural language interfaces for data discovery have incorporated generative language models. Systems such as **DataChat** (ACM SIGMOD 2020 [R32]), **CHORUS** (arXiv 2023 [R24]), and **Pneuma** (arXiv 2025 [R25]) explore the conversion of conversational user intents into structured search filters. CHORUS leverages LLMs to interpret natural language data requirements (e.g., "radiology scans for pulmonary edema with DICOM format"), translating free text into structured API calls across multiple repositories. Pneuma integrates dense vector embeddings with metadata indexes to facilitate semantic dataset matching across enterprise data lakes.

### 2.2 Limitations of Existing Work
While these systems excel at indexing file formats, column types, and semantic descriptions, they exhibit a critical common limitation: **they treat dataset discovery as a purely syntactic or semantic retrieval problem, entirely detached from dataset fairness, demographic balance, or geographic representation.** 
1. *Google Dataset Search* relies exclusively on publisher-provided metadata. If a publisher tags a medical cohort dataset as "Indian Healthcare", Google Dataset Search indexes it accordingly, even if the underlying data was sampled exclusively from a single private tertiary hospital in South Delhi, completely omitting 70% of the rural Indian population.
2. *Aurum* evaluates column similarities via Jaccard distance and entropy profiles, optimizing for schema integration rather than demographic parity.
3. *CHORUS* and *Pneuma* rank search results based on semantic proximity to user prompts and metadata completeness, lacking any mechanism to audit the internal demographic distributions of candidate datasets.

### 2.3 FairLens Differentiation and Hypotheses
FairLens directly addresses this limitation by coupling dataset discovery with an automated, domain-configurable representation gap scoring engine. In FairLens:
- Component A executes multi-source discovery across Hugging Face Hub [R48], Kaggle [R49], UCI Machine Learning Repository, data.gov, and Zenodo [R50].
- However, rather than returning uninspected links, FairLens feeds discovered datasets into Component B (the Gap-Detection Layer). The engine scans demographic, geographic, and cultural distributions against user-specified target populations and generates a structured representation score.
- **Working Hypothesis:** Coupling dataset retrieval with automated gap scanning will prevent the silent propagation of unrepresentative datasets into downstream fine-tuning workflows, reducing demographic discovery bias.

---

## 3. Dataset Documentation and Representation Gaps

### 3.1 State of Prior Research
Recognizing that biased models often stem from undocumented datasets, the machine learning community introduced structured documentation standards. In their seminal work, **Datasheets for Datasets** (Gebru et al., Communications of the ACM 2021 [R31]), the authors proposed a comprehensive questionnaire covering motivation, composition, collection process, preprocessing, uses, distribution, and maintenance. Datasheets introduced transparency norms that require dataset creators to disclose intended use cases and known limitations.

Pushkarna et al. expanded this concept with **Data Cards** (ACM FAccT 2022 [R2]), introducing a purpose-driven, visually structured documentation schema tailored for production ML pipelines. Data Cards explicitly formalize dataset boundaries, documenting downstream suitability, upstream collection biases, and benchmark performance across demographic slices.

Concurrently, automated methods for assessing dataset sufficiency have emerged. **GoalCover** (arXiv 2026 [R19]) introduced goal-driven data selection for instruction tuning, selecting training subsets that maximize coverage over a target skill distribution. In a broader evaluation of foundation model blind spots, **Competency Gaps in LLMs and Benchmarks** (arXiv 2025 [R27]) demonstrated that standard aggregate performance metrics conceal severe capability collapses in specialized subdomains.

### 3.2 Limitations of Existing Work
Despite their conceptual influence, existing dataset documentation paradigms suffer from two acute deficiencies:
1. *Manual Bottleneck:* Datasheets for Datasets [R31] and Data Cards [R2] are purely qualitative, manual artifacts. Creating a comprehensive Data Card requires weeks of human authoring, leading to negligible adoption across open-source repositories. A developer downloading a tabular dataset from Hugging Face or Kaggle rarely encounters a completed Data Card.
2. *Task-Specific vs. Demographic Gaps:* Automated frameworks like GoalCover [R19] measure coverage over functional task competencies (e.g., Python coding, mathematical reasoning), entirely bypassing demographic, regional, and cultural representation gaps.

### 3.3 FairLens Differentiation and Hypotheses
FairLens bridges the divide between manual qualitative documentation and automated task-specific selection by providing an **automated, domain-configurable, quantitative representation gap scanner**:
- It accepts arbitrary tabular datasets, user-defined column mappings, and optional target population distributions (such as national census data).
- It calculates transparent, mathematically grounded metrics: Category Coverage, Representation Share, Absolute Representation Deviation, Jensen-Shannon Distribution Divergence, and Missingness Rates.
- It incorporates statistical safeguards, including bootstrap confidence intervals and minimum subgroup sample-size thresholds, preventing false certainty when evaluating sparse demographic slices.
- **Working Hypothesis:** An automated, configurable gap-detection tool can quantify demographic and geographic imbalances in minutes, providing reproducible metrics where manual Data Cards fail due to documentation fatigue.

---

## 4. Fairness Definitions and Counterfactual Testing

### 4.1 State of Prior Research
The algorithmic fairness literature formalizes fairness through two distinct lenses: observational group fairness and causal counterfactual fairness. Observational metrics, comprehensively surveyed by Barocas, Hardt, and Narayanan [R43] and Gallegos et al. (Computational Linguistics 2024 [R15]), include Demographic Parity, Equalized Odds, and Predictive Parity. These metrics evaluate statistical independence between model predictions and protected attributes.

In contrast, **Counterfactual Fairness**, formulated by Kusner et al. (NeurIPS 2017 [R8]), grounds fairness in structural causal models. Formally, a decision $d$ is counterfactually fair with respect to protected attribute $A$ if:
$$P(d_{A \leftarrow a}(U) = y \mid X = x, A = a) = P(d_{A \leftarrow a'}(U) = y \mid X = x, A = a)$$
for all possible values $a, a'$, where $U$ represents background unobserved exogenous variables and $X$ denotes observed features. In natural language processing, this causal principle is operationalized via **Counterfactual Perturbation Testing**: generating pairs or n-tuples of test cases that are identical in semantic, statutory, and factual structure, varying solely in an irrelevant demographic identifier (e.g., swapping a male name for a female name, or a dominant-caste surname for an oppressed-caste surname).

Empirical implementations of counterfactual testing include **BiasAsker** (Wan et al., ACM ESEC/FSE 2023 [R6]), which automatically generates query pairs to interrogate conversational agents for social biases, and **CAFFE** (arXiv 2025 [R23]), which formalizes automated prompt perturbation pipelines with semantic invariance checks. Similarly, **BBQ** (Parrish et al., Findings of ACL 2022 [R33]) evaluates question answering models under ambiguous versus disambiguated contexts across nine protected socio-demographic axes.

### 4.2 Limitations of Existing Work
Existing counterfactual fairness frameworks exhibit critical methodological shortcomings when applied to domain-specific, high-stakes reasoning:
1. *Conflation of Inherent Noise with Demographic Bias:* Foundation models are non-deterministic under standard decoding temperatures. If a model exhibits a 10% baseline output fluctuation across identical prompt repetitions (prompt noise floor), observing a 12% outcome flip under counterfactual name swapping cannot be attributed solely to demographic bias. Most existing audits (e.g., BiasAsker [R6]) omit intrinsic noise calibration.
2. *Failure to Model Legally Relevant Distinctions:* Western fairness frameworks assume that protected attributes should *never* influence outcomes. In Indian jurisprudence, however, specific personal laws legitimately mandate distinct legal outcomes based on religion and gender (e.g., the Hindu Succession Act versus Muslim Personal Law). A naive counterfactual framework that swaps religion in a succession dispute will flag a legally correct statutory ruling as "unfair bias."
3. *Clinical Precedent vs. Legal Reality:* While **EQUITRIAGE** (Young & Matthews, arXiv 2026 [R17]) demonstrated high counterfactual flip rates (43.8%) in *Nemotron-3-Super* within clinical emergency triage, its findings are confined to gender in medical emergency acuity. Clinical triage metrics cannot be conflated with statutory legal or financial reasoning (Section 2.3).

### 4.3 FairLens Differentiation and Hypotheses
FairLens formulates a rigorous counterfactual auditing protocol designed specifically for professional reasoning:
- It explicitly separates **legally relevant statutory controls** (e.g., succession disputes governed by religious personal law) from **impermissible demographic bias** (e.g., criminal liability under the IPC/BNS, where caste and religion are strictly irrelevant).
- It introduces a **model noise floor control**, measuring the model's intrinsic non-deterministic variation on identical prompts and subtracting this baseline from observed demographic flip rates.
- **Working Hypothesis:** Isolating legally relevant controls and subtracting the prompt noise floor will yield a robust, uninflated metric of true demographic disparity in LLM reasoning.

---

## 5. Indian Demographic, Geographic, and Cultural Representation

### 5.1 State of Prior Research
In their landmark paper, **"Re-imagining Algorithmic Fairness in India and Beyond"** (ACM FAccT 2021 [R1]), Sambasivan et al. established that standard machine learning fairness paradigms are heavily West-centric. Drawing upon in-depth interviews with civil society organizations, activists, and technologists across India, the authors demonstrated that algorithmic harms in India are governed by unique, deeply entrenched social structures:
- **Caste (Jati and Varna):** A hierarchical social stratification system that dictates spatial segregation, social capital, and economic opportunity.
- **Religious Majoritarianism and Minoritization:** Complex tensions that influence access to housing, employment, and justice.
- **Linguistic and Regional Hierarchies:** Digital exclusion driven by the dominance of English and Hindi over non-scheduled languages and regional dialects.
- **Digital Infrastructure Skew:** Digital traces in India heavily over-represent urban, upper-caste, technologically connected men, rendering rural and lower-caste populations statistically invisible in open web corpora.

Subsequent empirical studies quantified these disparities in NLP. In **"Casteist but Not Racist? Quantifying Disparities in Large Language Model Bias between India and the West" (Indian-BhED)**, Khandelwal et al. (arXiv 2023 [R20]) evaluated commercial language models on associative sentence completion tasks. Their findings demonstrated that popular LLMs preferred stereotypical completions regarding Indian caste in **63% to 79%** of test cases, and religion in **69% to 72%** of test cases—revealing biases substantially stronger than Western racial biases in the same models.

Further contextualized benchmarks, such as **IndiBias** (Gupta et al., NAACL 2024 [R14]), **DECASTE** (arXiv 2025 [R21]), and **IndiCASA** (arXiv 2025 [R22]), established validated vocabularies of caste names, regional naming conventions, and cultural identifiers across Indian states, providing empirical ground truth on linguistic stereotyping.

### 5.2 Limitations of Existing Work
Despite their value in exposing cultural stereotyping, existing Indian bias benchmarks operate almost entirely at the level of **associative stereotyping and masked token probability**:
- Indian-BhED [R20] and IndiBias [R14] test whether an LLM associates a Brahmin surname with "scholar" or a Dalit surname with "manual scavenger" in open-ended text.
- They do **not** evaluate whether these associations alter deliberative outcomes when the model is tasked with applying a statutory legal test or assessing an investment loan.
- An LLM may exhibit masked-token stereotyping yet maintain statutory invariance when prompted with explicit legal constraints; conversely, a model may suppress overt slurs yet systematically deny bail to marginalized groups in simulated legal judgments.

### 5.3 FairLens Differentiation and Hypotheses
FairLens shifts the evaluation from associative stereotyping to **downstream outcome flips in high-stakes reasoning**:
- By embedding validated Indian demographic signifiers (derived from Sambasivan et al. [R1] and IndiBias [R14]) into multi-step statutory and financial scenarios, FairLens tests whether model judgments flip on allocative decisions.
- In Layer A, FairLens provides direct representation gap metrics for Indian states, districts, linguistic distributions, and demographic categories in tabular data.
- **Working Hypothesis:** Models that suppress overt caste slurs in conversational chat still exhibit statistically significant outcome flip rates when evaluating complex Indian legal and financial scenarios.

---

## 6. Indian Legal Reasoning and Fairness Evaluation

### 6.1 State of Prior Research
Natural language processing for the legal domain has expanded from document retrieval to judicial outcome prediction and statutory reasoning. The foundational corpus for Indian jurisprudence was established by Malik et al. with **ILDC for CJPE** (ACL 2021 [R13]), comprising 35,000 Supreme Court of India judgments annotated with court decisions and explanation rationale. In parallel, domain-adapted transformer models such as **InLegalBERT** (Paul et al., AI & Law 2022 [R34]) demonstrated that pre-training on Indian case law substantially outperforms general-domain BERT in legal classification and named entity recognition. Task benchmarks like **NyayaAnumana** (LREC-COLING 2024 [R35]) introduced multi-task evaluation for Indian court case analysis.

The critical intersection between Indian legal NLP and algorithmic fairness was established by Girhepuje et al. in **"Are Models Trained on Indian Legal Data Fair?"** (SAIL 2023 [R30]), which identified severe geographic and demographic skews in bail prediction models trained on Indian High Court dockets.

Most recently, Gupta et al. published **InSaAF: Incorporating Safety through Accuracy and Fairness | Are LLMs ready for the Indian Legal Domain?** (JURIX 2024 [R7]). As the closest prior work to FairLens, InSaAF established a specialized evaluation framework for Indian criminal law:
1. It formalized a **Binary Statutory Reasoning task** using provisions of the Indian Penal Code (IPC [R52]), testing whether specific legal sections apply to factual scenarios across diverse social identities.
2. It introduced the **$\beta$-weighted Legal Safety Score ($LSS_\beta$)**, harmonizing statutory accuracy and demographic fairness into a unified metric:
   $$LSS_\beta = \frac{(1 + \beta^2) \cdot \text{Accuracy} \cdot \text{Fairness}}{\beta^2 \cdot \text{Accuracy} + \text{Fairness}}$$
3. It demonstrated that instruction fine-tuning on curated legal data mitigated bias in base LLaMA-family models.

Concurrently, legal reliability studies such as **Large Legal Fictions** (Dahl et al., Journal of Legal Analysis 2024 [R16]) and **LegalBench** (Guha et al., NeurIPS 2023 [R11]) proved that LLMs hallucinate false legal citations and fabricated judicial holdings in up to 88% of complex common law queries, emphasizing the necessity of strict statutory grounding.

### 6.2 Limitations of Existing Work and InSaAF
While InSaAF represents a vital milestone, it possesses clear boundaries:
1. *Narrow Legal Scope:* InSaAF evaluates solely criminal statutory reasoning under the IPC. It ignores civil, commercial, and financial regulatory law (such as SEBI and RBI regulations).
2. *Omission of Dataset-Level Auditing:* InSaAF evaluates models on an existing benchmark without auditing the upstream pre-training or fine-tuning datasets that induced the bias.
3. *Model Coverage:* InSaAF tested base LLaMA models; it did not evaluate modern large-scale mixture-of-experts architectures such as NVIDIA Nemotron 3 Ultra.
4. *Absence of Attribution Controls:* InSaAF's fine-tuning experiments did not isolate the effect of demographic counterfactual balancing from domain-specific legal factual grounding.

### 6.3 FairLens Differentiation
FairLens expands upon InSaAF across five distinct dimensions:
- **Two-Layer Integration:** Links upstream dataset gap auditing (Layer A) directly with downstream model testing (Layer B).
- **Dual Domain:** Evaluates both criminal statutory law (IPC/BNS [R52]) and financial regulatory law (SEBI/RBI).
- **Target Model:** Audits NVIDIA Nemotron 3 Ultra (`nvidia/nemotron-3-ultra-550b-a55b`), which has never been audited in this domain.
- **Three-Way Attribution Control:** Implements a rigorous three-way comparative evaluation: Base Student Model versus Debiased Fine-Tuned Model versus Factually Grounded Control Model (trained on identical source data without demographic balancing).

---

## 7. Indian Financial Reasoning and Benchmark Limitations

### 7.1 State of Prior Research
Financial natural language processing has historically focused on Western equity markets and SEC filings (e.g., FinQA, ConvFinQA, FinanceBench). Bias in financial LLMs was highlighted in the position paper **"Evaluating Large Language Models in Finance Requires Explicit Bias Consideration"** (arXiv 2026 [R28]) and an empirical study at **ACM ICAIF 2025** [R5], which proved that LLM investment recommendations exhibit systematic skews based on simulated investor demographic profiles. General financial safety was formalized by **FinTrust** (arXiv 2025 [R29]), establishing compliance and toxicity metrics for financial chatbots.

For the Indian context, the primary landmark is **IndiaFinBench** (arXiv 2026 [R18]). IndiaFinBench established an evaluation benchmark consisting of **406 expert-annotated QA pairs derived from 192 primary regulatory documents** issued by the Securities and Exchange Board of India (SEBI) and the Reserve Bank of India (RBI) from 1992 to 2026. The benchmark evaluates models across regulatory interpretation, numerical reasoning, contradiction detection, and temporal reasoning. A complementary industrial benchmark, **BFSI-Bench** (arXiv 2025 [R36]), evaluates operational banking, retail lending, and insurance comprehension.

### 7.2 Limitations of Existing Work
1. *Accuracy-Only Benchmarking:* Both IndiaFinBench [R18] and BFSI-Bench [R36] measure factual accuracy, regulatory retrieval, and mathematical calculation. **Neither benchmark includes counterfactual fairness testing or demographic perturbation testing.**
2. *Separation from Legal Fairness:* Financial compliance is intrinsically connected to administrative and commercial law. In India, RBI master directions on priority sector lending and microfinance explicitly regulate credit allocation to economically weaker sections. Evaluating financial advice in isolation from legal statutory standards creates an incomplete picture of compliance.
3. *Strict Benchmark Separation (Rule 2.3):* Because IndiaFinBench is an established evaluation-only benchmark, **it must never be used for training or fine-tuning**, preserving its validity as an unbiased evaluation set.

### 7.3 FairLens Differentiation and Hypotheses
FairLens incorporates Indian financial regulatory reasoning into an integrated fairness audit:
- Uses IndiaFinBench [R18] exclusively as an external evaluation holdout.
- Develops novel counterfactual financial test pairs (e.g., retail loan advisory, microfinance compliance, and KYC documentation) where applicant identity (caste, religion, gender, domicile) is perturbed while financial fundamentals remain invariant.
- **Working Hypothesis:** Nemotron 3 Ultra will achieve high nominal regulatory accuracy on IndiaFinBench while exhibiting non-trivial counterfactual flip rates on retail lending and investment advisory queries.

---

## 8. Synthetic Corrective Data and Parameter-Efficient Fine-Tuning

### 8.1 State of Prior Research
When representation gaps and model biases are identified, retraining foundation models from scratch is computationally infeasible for academic institutions. The dominant paradigm relies on **Synthetic Data Generation** paired with **Parameter-Efficient Fine-Tuning (PEFT)**.

The foundation for synthetic instruction generation was established by **Self-Instruct** (Wang et al., ACL 2023 [R38]), which bootstraps diverse instruction-following data from teacher LLMs using iterative seed prompting. In the fairness domain, **Counterfactual Data Augmentation (CDA)** (Lu et al., arXiv 2020 [R39]) balances biased text corpora by perturbing demographic identifiers.

To transfer knowledge into small, locally deployable student models, **Knowledge Distillation** (comprehensively surveyed by Gou et al., IJCV 2021 [R41]) trains compact models to emulate the reasoning traces of high-capacity teacher models. To execute fine-tuning within consumer hardware constraints, **LoRA** (Hu et al., ICLR 2022 [R10]) injects trainable rank decomposition matrices into frozen model layers. **QLoRA** (Dettmers et al., NeurIPS 2023 [R9]) advanced this by quantizing the base model to 4-bit NormalFloat (NF4) with double quantization and paged optimizers, allowing an 8B parameter model to be fine-tuned on a single consumer GPU with 6 GB to 8 GB of VRAM.

### 8.2 Limitations of Existing Work
1. *Unverified Synthetic Data Teaches Confident Errors:* Generating synthetic legal data without human or statutory verification is dangerous. As proven in legal hallucination research [R16], unconstrained LLM generation creates plausible-sounding but fictitious legal precedents.
2. *Reproduction of Teacher Bias:* If Nemotron 3 Ultra harbors subtle demographic skews, standard Self-Instruct distillation will transfer those exact biases into the student model.
3. *Lack of Attribution Controls:* Prior work often attributes fine-tuning improvements to debiasing, without verifying whether gains merely resulted from domain knowledge injection.

### 8.3 FairLens Differentiation
In FairLens Component E and F:
- Synthetic generation is **grounded strictly in verifiable seed corpora**: official bare acts from India Code [R52], Supreme Court judgments, and published SEBI/RBI regulations.
- Generation is **counterfactually balanced by design**, explicitly producing invariant statutory and financial reasoning pairs.
- A **three-way evaluation protocol** is mandated:
  1. Base Student Model (zero fine-tuning).
  2. Debiased Fine-Tuned Student (trained on balanced, source-grounded synthetic corpus).
  3. Factual Control Student (trained on identical factual corpus without demographic balancing).
- **Working Hypothesis:** The debiased student model will match or exceed the factual control model's accuracy on Indian statutory benchmarks while achieving a statistically significant reduction in counterfactual flip rates.

---

## 9. Comparative Synthesis and Research Gaps

The following comparative matrices synthesize the state of the art across relevant literature and position FairLens directly against established precedents.

### Table 1: Comparative Literature Matrix (Discovery, Audit, and Fairness Dimensions)

| Work / Reference | Search Engine | Gap Scan | Indian Context | Legal Domain | Finance Domain | Fairness Audit | Fix & Retest | Target: Nemotron |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **CHORUS [R24], Pneuma [R25], DataChat [R32]** | Yes | No | No | No | No | No | No | No |
| **Google Dataset Search [R3], Aurum [R4]** | Yes | No | Partial | No | No | No | No | No |
| **Datasheets [R31], Data Cards [R2]** | No | Manual | No | No | No | No | No | No |
| **GoalCover [R19], Competency Gaps [R27]** | No | Task-only | No | No | No | No | No | No |
| **Kusner et al. [R8], CAFFE [R23], BiasAsker [R6]** | No | No | No | No | No | Yes | No | No |
| **EQUITRIAGE (Young & Matthews 2026) [R17]** | No | No | No | No | No | Clinical | No | Super (Not Ultra) |
| **Sambasivan et al. [R1], Indian-BhED [R20]** | No | No | Yes | No | No | Stereotype | No | No |
| **IndiBias [R14], DECASTE [R21], IndiCASA [R22]** | No | No | Yes | No | No | Token prob | No | No |
| **InSaAF (Gupta et al. 2024) [R7]** | No | No | Yes | Yes (IPC) | No | Yes | Yes (LLaMA) | No |
| **Girhepuje et al. (SAIL 2023) [R30]** | No | Court skew | Yes | Yes | No | Yes | No | No |
| **ILDC [R13], InLegalBERT [R34], NyayaAnumana [R35]** | No | No | Yes | Yes | No | No | No | No |
| **ICAIF Bias Study [R5], FinTrust [R29]** | No | No | No | No | Yes | Yes | No | No |
| **IndiaFinBench [R18], BFSI-Bench [R36]** | No | No | Yes | No | Yes | Accuracy only| No | No |
| **Large Legal Fictions [R16], LegalBench [R11]** | No | No | No | Yes | No | Reliability| No | No |
| **Self-Instruct [R38], QLoRA [R9], CDA [R39]** | No | No | No | General | General | CDA only | PEFT tools | No |
| **Nemotron 3 Technical Docs [R26, R40]** | No | No | Unmeasured| Corpora | No | None | No | Subject Model |
| **FairLens (Proposed Project)** | **Yes (Plan)**| **Automated**| **Yes** | **Yes** | **Yes** | **Yes** | **3-Way Eval** | **Nemotron 3 Ultra** |

---

## 10. Research Questions and Project Scope

To address the limitations documented above, FairLens is formulated around four core Research Questions (RQs):

- **RQ1 (Dataset Auditing):** How can representation gaps across demographic, geographic, and cultural dimensions in arbitrary tabular datasets be quantified and reported automatically with rigorous uncertainty bounds?
- **RQ2 (Model Fairness Auditing):** To what extent does NVIDIA Nemotron 3 Ultra exhibit counterfactual outcome flips across Indian legal statutory reasoning and financial regulatory compliance when non-legally relevant identity signifiers (caste, religion, gender, region) are perturbed?
- **RQ3 (Corrective Data Synthesis):** Can source-grounded synthetic legal and financial data generated from primary Indian statutes and regulations mitigate counterfactual outcome flips while preserving statutory accuracy?
- **RQ4 (Attribution and Knowledge Transfer):** When a compact student model (3B–4B) is fine-tuned on this corrective data using QLoRA, does it outperform an attribution control model (trained on unperturbed factual data), demonstrating that bias reduction is attributable to demographic balancing rather than domain knowledge injection?

### Project Scope Boundaries (Phase 1–4 Freeze)
1. **In-Scope for Phases 1–4:**
   - Formalization and traceability verification of all literature references (R1–R52).
   - Core infrastructure: centralized configuration, safe logging, cached OpenRouter API client, and live pricing/cost estimation.
   - Modular Dataset Discovery Engine supporting Hugging Face Hub, Kaggle, UCI, data.gov, and Zenodo with normalized metadata and offline fixtures.
   - Domain-configurable Dataset Representation-Gap Detection Engine implementing Category Coverage, Representation Deviation, Jensen-Shannon Divergence, Missingness Rates, bootstrap confidence intervals, explainable scorecards, and JSON/CSV reporting.
   - Fully reproducible, offline end-to-end integration test demonstrating dataset ingestion, gap profiling, mock discovery, and mock API execution.
2. **Out-of-Scope for Phases 1–4 (Deferred to Review-2 and Later Phases):**
   - Full QLoRA fine-tuning execution on local hardware or cloud GPU clusters.
   - Large-scale live paid API sweeps against Nemotron 3 Ultra.
   - Training or fine-tuning on evaluation benchmarks (IndiaFinBench, BFSI-Bench, or InSaAF holdouts).
   - Automatic external API-based demographic inference on unlabelled text columns.

---

## 11. Summary and Expected Contributions

FairLens bridges fundamental divides in current machine learning fairness and discovery research. By integrating general-purpose dataset representation auditing with a high-stakes empirical case study on Indian legal and financial reasoning, FairLens delivers:
1. **A Domain-Configurable Representation Gap Engine:** An open-source, automated tool for profiling demographic, geographic, and cultural coverage in datasets, providing transparent metrics and uncertainty intervals where manual Data Cards fail.
2. **The First Empirical Audit of Nemotron 3 Ultra for Indian Jurisprudence:** Independent, counterfactual evaluation of NVIDIA's 550B flagship model on Indian statutory and regulatory reasoning, establishing its actual flip rates beyond corporate safety disclosures.
3. **A Defensible, Controlled Repair Pipeline:** A methodology for synthesizing source-grounded corrective training data with explicit attribution controls, establishing whether small, fine-tuned models can achieve equitable legal reasoning within academic hardware constraints.

---

## 12. References (IEEE Format)

Please refer to `docs/research/references.bib` for complete machine-readable BibTeX metadata and `docs/research/reference_verification.csv` for the primary source verification ledger.
