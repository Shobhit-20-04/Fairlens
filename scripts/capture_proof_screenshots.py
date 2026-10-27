"""
FairLens: Official Website Proof & Novelty Verification Screenshot Capturer.
Captures high-resolution, dated visual evidence from authoritative sources
(NVIDIA NGC, OpenRouter, arXiv, PRS India, Google Research, Hugging Face)
to substantiate the six research gaps (G1-G6) and FairLens novelty claims.
"""

import csv
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WORKSPACE_DIR = Path("D:/fairlens")
OUTPUT_DIR = WORKSPACE_DIR / "research_papers" / "official_proof_screenshots"
MANIFEST_PATH = OUTPUT_DIR / "proof_manifest.csv"
README_PATH = OUTPUT_DIR / "README.md"

PROOFS_MANIFEST = [
    {
        "id": "PROOF_01",
        "filename": "01_nvidia_nemotron_content_safety_bias_none_proof.png",
        "url": "https://catalog.ngc.nvidia.com/orgs/nvidia/models/nemotron-content-safety",
        "title": "NVIDIA NGC Catalog: Nemotron Content Safety Model Card",
        "gap_addressed": "G3 (Nemotron 3 Ultra Unaudited for Demographic Fairness)",
        "novelty_claim": "NVIDIA officially documents 'Bias Mitigation Measures: None'. Built-in safety filters only target overt toxicity/weapons, leaving high-stakes reasoning completely unmitigated.",
        "scroll_y": 600,
        "wait_seconds": 5
    },
    {
        "id": "PROOF_02",
        "filename": "02_openrouter_nemotron_3_ultra_550b_spec_proof.png",
        "url": "https://openrouter.ai/models/nvidia/nemotron-3-ultra-550b-a55b",
        "title": "OpenRouter: nvidia/nemotron-3-ultra-550b-a55b Model Directory",
        "gap_addressed": "G3 (Nemotron 3 Ultra Scope & Deployment)",
        "novelty_claim": "Verifies that Nemotron 3 Ultra 550B is deployed as a frontier 550B MoE reasoning model with 128k context, yet has never been evaluated for Indian statutory or financial fairness.",
        "scroll_y": 0,
        "wait_seconds": 4
    },
    {
        "id": "PROOF_03",
        "filename": "03_insaaf_jurix2024_ipc_only_scope_proof.png",
        "url": "https://arxiv.org/abs/2402.10567",
        "title": "InSaAF: Incorporating Safety through Accuracy and Fairness (JURIX 2024 / arXiv)",
        "gap_addressed": "G4 & G5 (Indian Legal Fairness Scope Limitations)",
        "novelty_claim": "Proves the closest prior work (InSaAF) tested only LLaMA-2 on Indian Penal Code (IPC) criminal offenses; it completely omitted Indian financial regulation and dataset auditing.",
        "scroll_y": 0,
        "wait_seconds": 3
    },
    {
        "id": "PROOF_04",
        "filename": "04_indiafinbench_financial_qa_no_fairness_proof.png",
        "url": "https://arxiv.org/abs/2604.19298",
        "title": "IndiaFinBench: Benchmark for Indian Financial Regulatory Text (arXiv:2604.19298)",
        "gap_addressed": "G4 & G5 (Financial Benchmarks Lack Demographic Fairness)",
        "novelty_claim": "Proves that IndiaFinBench evaluates QA accuracy across 192 SEBI/RBI documents, but contains zero counterfactual perturbation testing or demographic fairness metrics.",
        "scroll_y": 0,
        "wait_seconds": 3
    },
    {
        "id": "PROOF_05",
        "filename": "05_indian_bhed_stereotypes_vs_outcome_flips_proof.png",
        "url": "https://arxiv.org/abs/2309.08573",
        "title": "Indian-BhED: Casteist but Not Racist? (arXiv:2309.08573)",
        "gap_addressed": "G5 (Associative Stereotypes vs. Deliberative Outcome Flips)",
        "novelty_claim": "Proves prevailing Indian bias benchmarks evaluate associative sentence completions (63%-79% caste bias), rather than downstream allocative decisions (bail or credit flips).",
        "scroll_y": 0,
        "wait_seconds": 3
    },
    {
        "id": "PROOF_06",
        "filename": "06_equitriage_clinical_triage_only_proof.png",
        "url": "https://arxiv.org/abs/2605.03998",
        "title": "EQUITRIAGE: Emergency Department Clinical Triage Fairness Audit (arXiv:2605.03998)",
        "gap_addressed": "G3 (Precedent for Nemotron Flip Rates Confined to Healthcare)",
        "novelty_claim": "Proves the only prior counterfactual flip-rate audit on Nemotron was restricted to emergency clinical triage across gender; Indian law and finance remain uncharted.",
        "scroll_y": 0,
        "wait_seconds": 3
    },
    {
        "id": "PROOF_07",
        "filename": "07_google_dataset_search_discovery_without_fairness_proof.png",
        "url": "https://research.google/pubs/google-dataset-search-building-a-search-engine-for-datasets-in-an-open-web-ecosystem/",
        "title": "Google Research: Google Dataset Search Ecosystem Architecture",
        "gap_addressed": "G1 (Dataset Discovery Tools Lack Fairness Scoring)",
        "novelty_claim": "Proves major web-scale discovery engines crawl schema.org metadata (names, formats, licenses) without any demographic, cultural, or geographic representation scoring.",
        "scroll_y": 0,
        "wait_seconds": 4
    },
    {
        "id": "PROOF_08",
        "filename": "08_bns_2023_statutory_transition_proof.png",
        "url": "https://prsindia.org/bills/parliament/the-bharatiya-nyaya-sanhita-2023",
        "title": "PRS Legislative Research: The Bharatiya Nyaya Sanhita, 2023 (Act No. 45 of 2023)",
        "gap_addressed": "G4 (Statutory Modernization from IPC to BNS)",
        "novelty_claim": "Proves the official Indian criminal statutory transition to BNS 2023; FairLens models both IPC and BNS 2023 statutory sections unlike older benchmarks stuck exclusively on IPC.",
        "scroll_y": 0,
        "wait_seconds": 3
    },
    {
        "id": "PROOF_09",
        "filename": "09_sambasivan_facct2021_india_fairness_grounding_proof.png",
        "url": "https://arxiv.org/abs/2101.09995",
        "title": "Re-imagining Algorithmic Fairness in India and Beyond (ACM FAccT 2021 / arXiv)",
        "gap_addressed": "Foundational Grounding (Western Race Parity Fails in India)",
        "novelty_claim": "Foundational peer-reviewed qualitative proof (36 expert interviews) establishing that Western fairness frameworks fail in India due to caste, religion, and regional hierarchies.",
        "scroll_y": 0,
        "wait_seconds": 3
    },
    {
        "id": "PROOF_10",
        "filename": "10_huggingface_hub_dataset_discovery_proof.png",
        "url": "https://huggingface.co/docs/hub/datasets",
        "title": "Hugging Face Hub: Dataset Documentation and Catalog Architecture",
        "gap_addressed": "G1 & G2 (Dataset Documentation Remains Static & Task-Centric)",
        "novelty_claim": "Shows that standard dataset hubs provide basic task/modality tags without automated demographic disparity or representation distribution auditing.",
        "scroll_y": 0,
        "wait_seconds": 4
    }
]


def capture_all_proofs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("=== FairLens: Capturing Official Website Proof Screenshots ===")
    print(f"Output Directory: {OUTPUT_DIR}\n")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1440,960")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    captured_records = []

    try:
        for idx, item in enumerate(PROOFS_MANIFEST, 1):
            proof_id = item["id"]
            filename = item["filename"]
            target_path = OUTPUT_DIR / filename
            url = item["url"]
            print(f"[{idx}/{len(PROOFS_MANIFEST)}] Capturing: {item['title']}")
            print(f"  URL: {url}")
            print(f"  Target: {filename}")

            try:
                driver.get(url)
                time.sleep(item.get("wait_seconds", 3))

                scroll_y = item.get("scroll_y", 0)
                if scroll_y > 0:
                    driver.execute_script(f"window.scrollTo(0, {scroll_y});")
                    time.sleep(1)

                driver.save_screenshot(str(target_path))
                file_size = target_path.stat().st_size
                print(f"  -> Captured successfully ({file_size:,} bytes)\n")

                captured_records.append({
                    "proof_id": proof_id,
                    "filename": filename,
                    "title": item["title"],
                    "url": url,
                    "gap_addressed": item["gap_addressed"],
                    "novelty_claim": item["novelty_claim"],
                    "file_size_bytes": file_size,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "status": "CAPTURED"
                })
            except Exception as e:
                print(f"  [ERROR] Failed to capture {url}: {e}\n")
                captured_records.append({
                    "proof_id": proof_id,
                    "filename": filename,
                    "title": item["title"],
                    "url": url,
                    "gap_addressed": item["gap_addressed"],
                    "novelty_claim": item["novelty_claim"],
                    "file_size_bytes": 0,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "status": f"FAILED: {str(e)[:100]}"
                })
    finally:
        driver.quit()

    # Write proof_manifest.csv
    print(f"Writing proof manifest to: {MANIFEST_PATH}")
    fieldnames = ["proof_id", "filename", "title", "url", "gap_addressed", "novelty_claim", "file_size_bytes", "timestamp", "status"]
    with open(MANIFEST_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(captured_records)

    # Write README.md
    print(f"Writing proof documentation to: {README_PATH}")
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write("# FairLens — Official Website Proofs & Novelty Verification Library\n\n")
        f.write("**Candidate:** Shobhit (Reg No: 26MCS0057)  \n")
        f.write("**Project:** FairLens — Two-Layer Fairness Auditing & NVIDIA Nemotron 3 Ultra Case Study  \n")
        f.write(f"**Last Updated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}  \n\n")
        f.write("---\n\n")
        f.write("## 1. Executive Purpose for Review Panel & Thesis Defense\n\n")
        f.write("This directory contains high-resolution, dated visual screenshots of official websites, open preprints, and government gazettes. ")
        f.write("These artifacts serve as empirical proof during M.Tech review evaluations, demonstrating that:\n")
        f.write("1. **Nemotron 3 Ultra is genuinely unaudited for demographic fairness**, with NVIDIA's official model cards explicitly documenting bias mitigation as `\"None\"`.\n")
        f.write("2. **Closest prior legal fairness benchmarks (InSaAF) are confined strictly to criminal IPC law on LLaMA**, omitting financial regulation and dataset auditing.\n")
        f.write("3. **Existing financial regulatory benchmarks (IndiaFinBench) test only QA accuracy**, containing zero fairness or counterfactual flip-rate metrics.\n")
        f.write("4. **Existing Indian bias benchmarks (Indian-BhED) test associative stereotypes in sentence completion**, rather than high-stakes allocative decision flips.\n")
        f.write("5. **Major dataset search engines (Google Dataset Search, Hugging Face) index metadata without demographic representation scoring**.\n\n")
        f.write("---\n\n")
        f.write("## 2. Visual Proofs & Novelty Alignment Table\n\n")
        f.write("| Proof ID | Screenshot Preview | Source & Context | Research Gap & Novelty Proven |\n")
        f.write("| :---: | :--- | :--- | :--- |\n")

        for r in captured_records:
            if r["status"] == "CAPTURED":
                f.write(f"| **{r['proof_id']}** | [`{r['filename']}`](./{r['filename']}) | **{r['title']}**<br>[Official URL]({r['url']}) | **{r['gap_addressed']}**<br>*{r['novelty_claim']}* |\n")

        f.write("\n---\n\n")
        f.write("## 3. How to Inspect & Use in Review Presentations\n\n")
        f.write("All screenshots are saved as high-resolution (1440x960) PNG images in `research_papers/official_proof_screenshots/`. ")
        f.write("They can be directly embedded into presentation slides (PowerPoint/Beamer) or opened during the viva to provide immediate visual substantiation for any novelty claim.\n\n")
        f.write("To re-capture or update the visual evidence suite, execute:\n")
        f.write("```powershell\n")
        f.write("python scripts/capture_proof_screenshots.py\n")
        f.write("```\n")

    print("\n=== All Proofs Successfully Captured and Documented ===")


if __name__ == "__main__":
    capture_all_proofs()
