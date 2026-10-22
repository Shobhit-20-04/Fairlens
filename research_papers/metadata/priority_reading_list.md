# FairLens — Priority Research Reading List

**Candidate:** Shobhit (Reg No: 26MCS0057)  
**Project:** FairLens — Two-Layer Fairness Auditing (Review-1 Milestone)  
**Generated:** 2026-10-22 14:39:06 UTC  

---

## Ranked Priority Reading Papers

### Priority 1: InSaAF: Incorporating Safety through Accuracy and Fairness | Are LLMs ready for the Indian Legal Domain?
- **Authors:** Naman Gupta, Aman Agrawal, et al. (CRAI IIT Madras / IIIT-H / AmEx)
- **Publication / Venue:** 2024 (Legal Knowledge and Information Systems (JURIX))
- **Official Publication URL:** [https://arxiv.org/abs/2402.10567](https://arxiv.org/abs/2402.10567)
- **Local PDF Path:** `research_papers/02_Indian_Legal_NLP/InSaAF_Incorporating_Safety_through_Accuracy_and_Fairness_Are_LLMs_ready_for_the_Indian_Legal_Domain.pdf`
- **Relevance to FairLens:** Closest prior work in Indian legal fairness; evaluates LLMs on Indian Penal Code binary statutory reasoning; proposes Legal Safety Score LSS_beta and fine-tuning baseline.
- **Specific Project Phase / Gap:** Key benchmark comparison target; informs statutory criminal law evaluation.

### Priority 2: Casteist but Not Racist? Quantifying Disparities in Large Language Model Bias between India and the West
- **Authors:** Khyati Khandelwal, Manuel Tonneau, Andrew M. Bean, Hannah Rose Kirk, Scott A. Hale
- **Publication / Venue:** 2023 (arXiv preprint (Indian-BhED Benchmark))
- **Official Publication URL:** [https://arxiv.org/abs/2309.08573](https://arxiv.org/abs/2309.08573)
- **Local PDF Path:** `research_papers/01_Indian_Fairness_and_Bias/Casteist_but_Not_Racist_Quantifying_Disparities_in_Large_Language_Model_Bias_between_India_and_the_West.pdf`
- **Relevance to FairLens:** Empirical benchmark (Indian-BhED) demonstrating that commercial LLMs show severe caste (63%-79%) and religious (69%-72%) stereotypical preference in sentence completion tasks.
- **Specific Project Phase / Gap:** Direct empirical justification for testing caste and religion dimensions in FairLens Layer B.

### Priority 3: IndiaFinBench: An Evaluation Benchmark for Large Language Model Performance on Indian Financial Regulatory Text
- **Authors:** Rajveer Singh Pall
- **Publication / Venue:** 2026 (arXiv preprint)
- **Official Publication URL:** [https://arxiv.org/abs/2604.19298](https://arxiv.org/abs/2604.19298)
- **Local PDF Path:** `research_papers/03_Financial_Fairness_and_Benchmarks/IndiaFinBench_An_Evaluation_Benchmark_for_Large_Language_Model_Performance_on_Indian_Financial_Regulatory_Text.pdf`
- **Relevance to FairLens:** 406 expert-annotated QA pairs from 192 SEBI and RBI regulatory documents spanning 1992-2026; evaluation-only benchmark for Indian financial reasoning in FairLens Layer B.
- **Specific Project Phase / Gap:** Core financial evaluation benchmark for FairLens Layer B; strictly evaluation-only.

### Priority 4: EQUITRIAGE: A Fairness Audit of Gender Bias in LLM-Based Emergency Department Triage
- **Authors:** R. J. Young, A. M. Matthews
- **Publication / Venue:** 2026 (Preprint (arXiv))
- **Official Publication URL:** [https://arxiv.org/abs/2605.03998](https://arxiv.org/abs/2605.03998)
- **Local PDF Path:** `research_papers/09_Clinical_Triage_and_Related_Work/EQUITRIAGE_A_Fairness_Audit_of_Gender_Bias_in_LLM-Based_Emergency_Department_Triage.pdf`
- **Relevance to FairLens:** Audits five LLMs on 18k clinical vignettes; finds Nemotron-3-Super has 43.8% counterfactual flip rate; methodological precedent for counterfactual flip-rate testing on Nemotron family.
- **Specific Project Phase / Gap:** Methodological precedent for counterfactual flip-rate testing on Nemotron models.

### Priority 5: Counterfactual Fairness
- **Authors:** Matt J. Kusner, Joshua Loftus, Chris Russell, Ricardo Silva
- **Publication / Venue:** 2017 (Advances in Neural Information Processing Systems (NeurIPS 30))
- **Official Publication URL:** [https://arxiv.org/abs/1703.06856](https://arxiv.org/abs/1703.06856)
- **Local PDF Path:** `research_papers/04_Counterfactual_Fairness/Counterfactual_Fairness.pdf`
- **Relevance to FairLens:** Foundational causal definition: a decision is fair if it is invariant across counterfactual worlds with swapped protected attributes; core theoretical foundation for FairLens flip-rate analysis.
- **Specific Project Phase / Gap:** Theoretical anchor for counterfactual flip-rate metric and causal attribution controls.

### Priority 6: Data Cards: Purpose-Driven Visual Summaries for Data Documentation
- **Authors:** Mahima Pushkarna, Andrew Zaldivar, Oddur Kjartansson
- **Publication / Venue:** 2022 (Proceedings of the 2022 ACM Conference on Fairness, Accountability, and Transparency (FAccT))
- **Official Publication URL:** [https://arxiv.org/abs/2204.01075](https://arxiv.org/abs/2204.01075)
- **Local PDF Path:** `research_papers/05_Dataset_Discovery_and_Documentation/Data_Cards_Purpose-Driven_Visual_Summaries_for_Data_Documentation.pdf`
- **Relevance to FairLens:** Structured schema for dataset documentation focusing on upstream sources and downstream usage boundaries; provides documentation standards for FairLens metadata schema and audit reporting.
- **Specific Project Phase / Gap:** Standards reference for FairLens normalized 20+ field dataset metadata schema.

### Priority 6: Datasheets for Datasets
- **Authors:** Timnit Gebru, Jamie Morgenstern, Briana Vecchione, Jennifer Wortman Vaughan, Hanna Wallach, Hal Daume III, Kate Crawford
- **Publication / Venue:** 2021 (Communications of the ACM (CACM))
- **Official Publication URL:** [https://arxiv.org/abs/1803.09010](https://arxiv.org/abs/1803.09010)
- **Local PDF Path:** `research_papers/05_Dataset_Discovery_and_Documentation/Datasheets_for_Datasets.pdf`
- **Relevance to FairLens:** Foundational framework proposing standardized documentation questions for dataset creation, composition, collection, and maintenance; informs FairLens metadata schema and data dictionary.
- **Specific Project Phase / Gap:** Foundational citation for dataset documentation transparency.

### Priority 7: QLoRA: Efficient Finetuning of Quantized LLMs
- **Authors:** Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, Luke Zettlemoyer
- **Publication / Venue:** 2023 (Advances in Neural Information Processing Systems (NeurIPS 36))
- **Official Publication URL:** [https://arxiv.org/abs/2305.14314](https://arxiv.org/abs/2305.14314)
- **Local PDF Path:** `research_papers/06_Fine_Tuning_and_Synthetic_Data/QLoRA_Efficient_Finetuning_of_Quantized_LLMs.pdf`
- **Relevance to FairLens:** Enables 4-bit NormalFloat quantization with double quantization and paged optimizers for parameter-efficient fine-tuning; hardware feasibility foundation for student model training on RTX 3050 (6GB VRAM).
- **Specific Project Phase / Gap:** Hardware feasibility foundation for 3B-4B parameter student fine-tuning.

### Priority 7: LoRA: Low-Rank Adaptation of Large Language Models
- **Authors:** Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen
- **Publication / Venue:** 2021 (International Conference on Learning Representations (ICLR))
- **Official Publication URL:** [https://arxiv.org/abs/2106.09685](https://arxiv.org/abs/2106.09685)
- **Local PDF Path:** `research_papers/06_Fine_Tuning_and_Synthetic_Data/LoRA_Low-Rank_Adaptation_of_Large_Language_Models.pdf`
- **Relevance to FairLens:** Parameter-efficient adapter tuning freezing base weights and injecting trainable rank decomposition matrices; core efficiency mechanism for fine-tuning in student model correction.
- **Specific Project Phase / Gap:** Baseline PEFT technique for student fine-tuning.

### Priority 8: ILDC for CJPE: Indian Legal Documents Corpus for Court Judgment Prediction and Explanation
- **Authors:** Vijit Malik, Rishabh Sanjay, Shubham Kumar Nigam, Kripabandhu Ghosh, Shouvik Kumar Guha, Arnab Bhattacharya, Ashutosh Modi
- **Publication / Venue:** 2021 (Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics (ACL))
- **Official Publication URL:** [https://aclanthology.org/2021.acl-long.313/](https://aclanthology.org/2021.acl-long.313/)
- **Local PDF Path:** `research_papers/02_Indian_Legal_NLP/ILDC_for_CJPE_Indian_Legal_Documents_Corpus_for_Court_Judgment_Prediction_and_Explanation.pdf`
- **Relevance to FairLens:** Corpus of 35k Supreme Court of India judgments annotated with court decisions; foundational ground-truth source for Indian legal precedence and judicial outcomes.
- **Specific Project Phase / Gap:** Ground-truth dataset source for Indian judicial prediction.

### Priority 8: LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models
- **Authors:** Neel Guha, Julian Nyarko, Daniel E. Ho, Christopher Re, et al.
- **Publication / Venue:** 2023 (Advances in Neural Information Processing Systems (NeurIPS Datasets & Benchmarks))
- **Official Publication URL:** [https://arxiv.org/abs/2308.11462](https://arxiv.org/abs/2308.11462)
- **Local PDF Path:** `research_papers/07_Legal_Reasoning_and_Evaluation/LegalBench_A_Collaboratively_Built_Benchmark_for_Measuring_Legal_Reasoning_in_Large_Language_Models.pdf`
- **Relevance to FairLens:** 162 legal reasoning tasks across US legal subdomains (statutory, contract, common law); standardizes legal reasoning task taxonomies and issue-spotting structures.
- **Specific Project Phase / Gap:** Taxonomy reference for legal issue spotting and statutory tasks.

### Priority 9: Re-imagining Algorithmic Fairness in India and Beyond
- **Authors:** Nithya Sambasivan, Erin Arnesen, Ben Hutchinson, Tulsee Doshi, Vinodkumar Prabhakaran
- **Publication / Venue:** 2021 (ACM Conference on Fairness, Accountability, and Transparency (FAccT))
- **Official Publication URL:** [https://doi.org/10.1145/3442188.3445896](https://doi.org/10.1145/3442188.3445896)
- **Local PDF Path:** `research_papers/01_Indian_Fairness_and_Bias/Re-imagining_Algorithmic_Fairness_in_India_and_Beyond.pdf`
- **Relevance to FairLens:** Foundational motivation for Indian demographic and cultural gap detection (Layer A and B); establishes that Western racial fairness definitions fail in India due to caste, religious personal laws, and regional hierarchies.
- **Specific Project Phase / Gap:** Primary evidence cited in Review-1 presentation and Section 2.1 problem relevance.

### Priority 10: Self-Instruct: Aligning Language Models with Self-Generated Instructions
- **Authors:** Yizhong Wang, Yeganeh Kordi, Swaroop Mishra, Alisa Liu, Noah A. Smith, Daniel Khashabi, Hannaneh Hajishirzi
- **Publication / Venue:** 2023 (Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (ACL))
- **Official Publication URL:** [https://arxiv.org/abs/2212.10560](https://arxiv.org/abs/2212.10560)
- **Local PDF Path:** `research_papers/06_Fine_Tuning_and_Synthetic_Data/Self-Instruct_Aligning_Language_Models_with_Self-Generated_Instructions.pdf`
- **Relevance to FairLens:** Pipeline for bootstrapping instruction-following data from teacher models starting from small seed tasks; foundation for Component E synthetic corrective data generation.
- **Specific Project Phase / Gap:** Pipeline model for bootstrapping corrective instructional datasets.

### Priority 10: BiasAsker: Measuring the Bias in Conversational AI via Automated Question Asking
- **Authors:** Yuxuan Wan, Guanhong Pu, Jinhao Sun, Aparna Garimella, Kai-Wei Wan, Sheng Zheng, Tong Xiao
- **Publication / Venue:** 2023 (Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE))
- **Official Publication URL:** [https://arxiv.org/abs/2305.12434](https://arxiv.org/abs/2305.12434)
- **Local PDF Path:** `research_papers/07_Legal_Reasoning_and_Evaluation/BiasAsker_Measuring_the_Bias_in_Conversational_AI_via_Automated_Question_Asking.pdf`
- **Relevance to FairLens:** Automated framework generating counterfactual query pairs to detect social bias in conversational AI; provides methodological basis for counterfactual question generation.
- **Specific Project Phase / Gap:** Framework for automated paired question generation.

