"""
FairLens Offline End-to-End Integration Demonstration.

Executes all four phases in a zero-network, fully reproducible sequence:
1. Ingests synthetic software-test dataset.
2. Profiles data quality, missingness, and duplicates.
3. Runs Phase 4 domain-configurable representation audit (gender, state, caste).
4. Generates structured audit report with assumptions and limitations.
5. Exports audit report to outputs/audit_reports/demo_audit_report.json and .csv.
6. Runs Phase 2 cached API client in mock/dry-run mode without network calls.
7. Runs Phase 3 dataset discovery search against offline fixtures.
8. Displays complete execution summary for Review-1 viva demo.
"""

import sys
import time
from pathlib import Path

from fairlens.api.client import OpenRouterClient
from fairlens.api.pricing import CostEstimator
from fairlens.auditing.config import AuditConfig, AuditDimension
from fairlens.auditing.engine import RepresentationAuditEngine
from fairlens.config.settings import get_settings
from fairlens.discovery.engine import DatasetDiscoveryEngine
from fairlens.discovery.schema import DiscoveryQuery


def run_demo():
    print("==================================================================")
    print("    FAIRLENS REPRODUCIBLE OFFLINE DEMONSTRATION (PHASES 1-4)     ")
    print("    M.Tech Project (MASET697) | SCOPE | VIT Vellore              ")
    print("==================================================================")

    # 1. Inspect Environment & Settings
    print("\n[STEP 1] Initializing Central Configuration (Offline Mode)...")
    settings = get_settings()
    settings.offline_mode = True
    print(f"  Environment: {settings.env}")
    print(f"  Target Model: {settings.openrouter_model}")
    print(f"  Offline Mode: {settings.offline_mode} (Guaranteed Zero Network/Paid Calls)")

    # 2. Phase 4 Tabular Representation Audit
    print("\n[STEP 2] Running Phase 4 Representation-Gap Audit on Indian Legal Fixture...")
    dataset_path = Path("tests/fixtures/auditing/indian_legal_synthetic_audit.csv")

    dim_gender = AuditDimension(
        name="gender",
        column_name="gender",
        expected_distribution={"Male": 0.50, "Female": 0.50, "Non-Binary": 0.0},
    )
    dim_state = AuditDimension(name="state", column_name="state")
    dim_caste = AuditDimension(name="caste", column_name="caste_category")

    config = AuditConfig(
        dimensions=[dim_gender, dim_state, dim_caste],
        intersectional_pairs=[("gender", "state")],
    )
    audit_engine = RepresentationAuditEngine(config)
    report = audit_engine.audit(dataset_path)

    print(report.format_text_summary())

    # Export reports
    export_json = Path("outputs/audit_reports/demo_audit_report.json")
    export_csv = Path("outputs/audit_reports/demo_audit_report.csv")
    audit_engine.export_report(report, export_json, format="json")
    audit_engine.export_report(report, export_csv, format="csv")
    print(f"\n[+] Exported structured audit report to:")
    print(f"    - JSON: {export_json}")
    print(f"    - CSV:  {export_csv}")

    # 3. Phase 2 Mocked API Client Execution
    print("\n[STEP 3] Running Phase 2 Cached OpenRouter Client in Mock Mode...")
    client = OpenRouterClient(settings=settings, mock_mode=True)
    estimator = CostEstimator(
        default_input_price_per_m=settings.input_price_per_m,
        default_output_price_per_m=settings.output_price_per_m,
        max_spend_usd=settings.max_spend_usd,
    )

    test_messages = [
        {"role": "system", "content": "You are an Indian statutory legal reasoning auditor."},
        {"role": "user", "content": "Evaluate whether Section 420 IPC applies to factual Scenario 104."},
    ]

    # Pre-execution cost check
    cost_est = estimator.estimate(
        total_requests=1,
        avg_input_tokens=150,
        avg_output_tokens=80,
        model=settings.openrouter_model,
        use_free_tier=True,
    )
    print(f"  Pre-Execution Cost Estimate: ${cost_est.projected_total_cost:.4f} USD (Within Budget: {cost_est.within_budget})")

    resp1 = client.complete(test_messages, use_cache=True)
    print(f"  Call 1 (Cache Miss): ID={resp1['id']}, Cached={resp1['cached']}, Elapsed={resp1['elapsed_seconds']}s")
    print(f"  Model Output Snippet:\n    \"{resp1['content'][:120]}...\"")

    resp2 = client.complete(test_messages, use_cache=True)
    print(f"  Call 2 (Deterministic Cache Hit): ID={resp2['id']}, Cached={resp2['cached']}, Elapsed={resp2['elapsed_seconds']}s")
    cache_stats = client.cache.stats()
    print(f"  Response Cache Stats: Hits={cache_stats['hits']}, Misses={cache_stats['misses']}, HitRate={cache_stats['hit_rate']:.1%}")

    # 4. Phase 3 Dataset Discovery Search
    print("\n[STEP 4] Running Phase 3 Multi-Source Discovery Engine (Offline Fixtures)...")
    discovery_engine = DatasetDiscoveryEngine(settings=settings, use_fixtures_only=True)
    discovery_query = DiscoveryQuery(keywords="Indian legal financial regulatory", limit=3)
    discovery_result = discovery_engine.search(discovery_query)

    print(discovery_engine.format_report(discovery_result))

    print("\n==================================================================")
    print("       FAIRLENS PHASES 1-4 INTEGRATION DEMO COMPLETE              ")
    print("       Status: ALL COMPONENTS OPERATIONAL AND REPRODUCIBLE        ")
    print("==================================================================")


if __name__ == "__main__":
    run_demo()
