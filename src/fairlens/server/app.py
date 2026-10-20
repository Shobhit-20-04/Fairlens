"""
FairLens Backend REST API Server.

Provides typed HTTP endpoints integrating the Python backend engines:
- Settings & Health monitoring
- Federated Dataset Discovery (Phase 3)
- Tabular Data Profiling & Representation-Gap Auditing (Phase 4)
- Research Workspace Telemetry & Pricing (Phase 2 & Layer B)
"""

import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
import flask
from flask import Flask, jsonify, request
from flask_cors import CORS

from fairlens.config.settings import get_settings
from fairlens.config.logging import get_logger
from fairlens.discovery.engine import DatasetDiscoveryEngine
from fairlens.discovery.schema import DiscoveryQuery
from fairlens.auditing.config import AuditConfig, AuditDimension
from fairlens.auditing.loader import TabularDataLoader
from fairlens.auditing.engine import RepresentationAuditEngine, AuditReport
from fairlens.api.pricing import CostEstimator

logger = get_logger("server.app")

# Ensure required output directories exist
os.makedirs("outputs/audit_reports", exist_ok=True)
os.makedirs("outputs/uploads", exist_ok=True)

app = Flask(__name__)
# Enable CORS for local Vite dev server
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Global in-memory cache of recent audit reports for export
_audit_reports_cache: Dict[str, Any] = {}


def get_gpu_info() -> Dict[str, Any]:
    """Inspect GPU availability and VRAM telemetry safely."""
    try:
        import torch
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            vram_gb = round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2)
            return {
                "available": True,
                "device": device_name,
                "vram_gb": vram_gb,
                "cuda_version": torch.version.cuda,
            }
    except Exception as e:
        logger.debug(f"GPU inspection failed or PyTorch not available: {e}")
    return {"available": False, "device": "CPU Only", "vram_gb": 0.0, "cuda_version": None}


# ==============================================================================
# Health & Settings Endpoints
# ==============================================================================

@app.route("/api/health", methods=["GET"])
def health_check():
    """System health check and runtime telemetry."""
    settings = get_settings()
    gpu_info = get_gpu_info()

    return jsonify({
        "status": "healthy",
        "service": "FairLens Research Platform",
        "version": "0.1.0",
        "environment": settings.env,
        "offline_mode": settings.offline_mode,
        "python_version": sys.version.split()[0],
        "gpu": gpu_info,
        "timestamp": time.time(),
    })


@app.route("/api/settings", methods=["GET"])
def get_settings_view():
    """Retrieve masked application settings and budget ceilings."""
    settings = get_settings()

    def mask(val: Optional[str]) -> str:
        if not val:
            return "<not-set>"
        if len(val) <= 8:
            return "***"
        return f"{val[:4]}...{val[-4:]}"

    return jsonify({
        "env": settings.env,
        "log_level": settings.log_level,
        "offline_mode": settings.offline_mode,
        "openrouter_model": settings.openrouter_model,
        "openrouter_api_key_configured": settings.has_openrouter_credentials(),
        "openrouter_api_key_masked": mask(settings.openrouter_api_key),
        "openrouter_timeout_seconds": settings.openrouter_timeout_seconds,
        "openrouter_max_retries": settings.openrouter_max_retries,
        "budget": {
            "max_spend_usd": settings.max_spend_usd,
            "warn_spend_usd": settings.warn_spend_usd,
            "input_price_per_m": settings.input_price_per_m,
            "output_price_per_m": settings.output_price_per_m,
        },
        "providers": {
            "huggingface": bool(settings.huggingface_token),
            "kaggle": bool(settings.kaggle_key),
            "data_gov": bool(settings.data_gov_api_key),
            "zenodo": bool(settings.zenodo_access_token),
        }
    })


# ==============================================================================
# Discovery Endpoints (Phase 3)
# ==============================================================================

@app.route("/api/discovery/providers", methods=["GET"])
def discovery_providers():
    """List supported dataset discovery providers and their authentication status."""
    settings = get_settings()
    return jsonify({
        "providers": [
            {
                "id": "huggingface",
                "name": "Hugging Face Hub",
                "authenticated": bool(settings.huggingface_token),
                "public_search": True,
                "rate_limit_authenticated": "Higher rate limits with token",
                "description": "NLP, multimodal, and domain-specific open ML datasets."
            },
            {
                "id": "zenodo",
                "name": "Zenodo (CERN / OpenAIRE)",
                "authenticated": bool(settings.zenodo_access_token),
                "public_search": True,
                "rate_limit_authenticated": "100 req/min with token",
                "description": "Scientific publications, research datasets, and academic artifacts with DOIs."
            },
            {
                "id": "data_gov",
                "name": "Data.gov & Open Government Catalogs",
                "authenticated": bool(settings.data_gov_api_key),
                "public_search": True,
                "rate_limit_authenticated": "1,000 req/hour with DEMO_KEY",
                "description": "US and Indian open government data catalogs (data.gov, data.gov.in)."
            },
            {
                "id": "uci",
                "name": "UCI Machine Learning Repository",
                "authenticated": False,
                "public_search": True,
                "rate_limit_authenticated": "No API key required",
                "description": "Classic benchmark datasets with verified feature types and demographic annotations."
            },
            {
                "id": "kaggle",
                "name": "Kaggle Datasets",
                "authenticated": bool(settings.kaggle_key),
                "public_search": False,
                "rate_limit_authenticated": "Kaggle API key required for live search",
                "description": "Crowdsourced and competition tabular datasets with community feedback."
            }
        ]
    })


@app.route("/api/discovery/search", methods=["POST"])
def discovery_search():
    """Execute federated dataset discovery search across configured adapters."""
    body = request.get_json() or {}
    query_str = body.get("query", "").strip()
    domain = body.get("domain") or None
    geo = body.get("geographic_coverage") or None
    selected_providers = body.get("providers")
    min_quality = float(body.get("min_quality_score", 0.0))
    limit = int(body.get("limit", 20))
    use_mock_offline = bool(body.get("use_mock_offline", False))

    settings = get_settings()
    # In offline mode or if requested, use fixtures
    engine = DatasetDiscoveryEngine(
        settings=settings,
        use_fixtures_only=use_mock_offline or settings.offline_mode
    )

    query = DiscoveryQuery(
        keywords=query_str,
        domain=domain,
        geography=geo,
        providers=selected_providers,
        limit=limit,
    )

    result = engine.search(query)

    return jsonify({
        "query": {
            "keywords": result.query.keywords,
            "domain": result.query.domain,
            "geography": result.query.geography,
            "providers": result.query.providers,
            "limit": result.query.limit,
        },
        "total_found": result.total_found,
        "returned_count": len(result.datasets),
        "execution_time_seconds": round(result.execution_time_seconds, 3),
        "provider_counts": result.provider_counts,
        "provider_errors": result.provider_errors,
        "datasets": [ds.to_dict() for ds in result.datasets],
    })


# ==============================================================================
# Profiling & Sample Datasets Endpoints (Phase 4)
# ==============================================================================

@app.route("/api/profiler/samples", methods=["GET"])
def get_sample_datasets():
    """List available pre-loaded sample datasets for instant demonstration."""
    sample_dir = Path("tests/fixtures/auditing")
    samples = []

    descriptions = {
        "indian_legal_synthetic_audit.csv": {
            "name": "Indian Legal Case Synthetic Audit (Layer B)",
            "description": "50 synthetic case filings with gender, religion, and state dimensions modeled after Indian legal domains.",
            "recommended_dimensions": [
                {
                    "name": "gender",
                    "column_name": "gender",
                    "dimension_type": "demographic",
                    "expected_distribution": {"Male": 0.48, "Female": 0.48, "Non-Binary": 0.04},
                    "expected_categories": ["Male", "Female", "Non-Binary"]
                },
                {
                    "name": "religion",
                    "column_name": "religion",
                    "dimension_type": "cultural",
                    "expected_distribution": {"Hindu": 0.798, "Muslim": 0.142, "Christian": 0.023, "Sikh": 0.017, "Other": 0.020},
                    "expected_categories": ["Hindu", "Muslim", "Christian", "Sikh", "Other"]
                },
                {
                    "name": "state",
                    "column_name": "state",
                    "dimension_type": "geographic",
                    "expected_categories": ["Maharashtra", "Karnataka", "Tamil Nadu", "Delhi", "Uttar Pradesh", "West Bengal", "Gujarat"]
                }
            ]
        },
        "balanced.csv": {
            "name": "Balanced Demographic Sample",
            "description": "A benchmark dataset with balanced gender and region distributions for testing parity scorecards.",
            "recommended_dimensions": [
                {
                    "name": "gender",
                    "column_name": "gender",
                    "dimension_type": "demographic",
                    "expected_distribution": {"M": 0.5, "F": 0.5},
                    "expected_categories": ["M", "F"]
                }
            ]
        },
        "imbalanced.csv": {
            "name": "Imbalanced Distribution Benchmark",
            "description": "Heavily skewed distribution with 90% majority group to test representation gap alerts.",
            "recommended_dimensions": [
                {
                    "name": "category",
                    "column_name": "category",
                    "dimension_type": "demographic",
                    "expected_distribution": {"Group_A": 0.5, "Group_B": 0.5},
                    "expected_categories": ["Group_A", "Group_B"]
                }
            ]
        },
        "with_nulls.csv": {
            "name": "Missing Values & Null Benchmark",
            "description": "Contains varied missingness markers (NA, unknown, null, ?) to test data hygiene and Wilson CIs.",
            "recommended_dimensions": [
                {
                    "name": "gender",
                    "column_name": "gender",
                    "dimension_type": "demographic",
                    "expected_categories": ["Male", "Female"]
                }
            ]
        },
        "missing_categories.csv": {
            "name": "Zero-Observation Underrepresented Categories",
            "description": "Omits expected categories to trigger zero-observation severity warnings.",
            "recommended_dimensions": [
                {
                    "name": "tier",
                    "column_name": "tier",
                    "dimension_type": "cultural",
                    "expected_categories": ["Tier1", "Tier2", "Tier3", "Rural"]
                }
            ]
        }
    }

    if sample_dir.exists():
        for f in sample_dir.glob("*.csv"):
            meta = descriptions.get(f.name, {
                "name": f.stem.replace("_", " ").title(),
                "description": f"Auditing fixture dataset ({f.name})",
                "recommended_dimensions": []
            })
            samples.append({
                "file_name": f.name,
                "file_path": str(f).replace("\\", "/"),
                "size_bytes": f.stat().st_size,
                "title": meta["name"],
                "description": meta["description"],
                "recommended_dimensions": meta.get("recommended_dimensions", [])
            })

    return jsonify({"samples": samples})


@app.route("/api/profiler/profile", methods=["POST"])
def profile_dataset():
    """Profile tabular dataset: schema, column types, null counts, duplicates, and preview rows."""
    file_path: Optional[str] = None

    if "file" in request.files:
        uploaded_file = request.files["file"]
        if not uploaded_file.filename:
            return jsonify({"error": "No file uploaded"}), 400
        safe_filename = Path(uploaded_file.filename).name
        target_path = Path("outputs/uploads") / safe_filename
        uploaded_file.save(str(target_path))
        file_path = str(target_path)
    else:
        body = request.get_json() or {}
        file_path = body.get("file_path")

    if not file_path:
        return jsonify({"error": "No file path or file provided"}), 400

    path_obj = Path(file_path)
    if not path_obj.exists():
        return jsonify({"error": f"File does not exist: {file_path}"}), 404

    try:
        df, profile = TabularDataLoader.load(path_obj)

        # Generate preview rows (first 20 rows, sanitized for JSON)
        preview_df = df.head(20).fillna("<NULL>")
        preview_rows = preview_df.to_dict(orient="records")

        # Column detailed metadata
        columns_meta = []
        for col in df.columns:
            s = df[col]
            null_count = int(s.isna().sum())
            unique_count = int(s.nunique(dropna=True))
            dtype_str = profile.get("column_types", {}).get(col, str(s.dtype))
            sample_unique = [str(x) for x in s.dropna().unique()[:8]]

            columns_meta.append({
                "name": col,
                "dtype": dtype_str,
                "null_count": null_count,
                "null_rate": round(null_count / len(df), 4) if len(df) > 0 else 0.0,
                "unique_count": unique_count,
                "sample_values": sample_unique,
            })

        return jsonify({
            "status": "success",
            "file_path": str(path_obj).replace("\\", "/"),
            "file_name": path_obj.name,
            "total_rows": profile["total_rows"],
            "total_columns": profile["total_columns"],
            "duplicate_rows": profile["duplicate_rows"],
            "duplicate_rate": profile["duplicate_rate"],
            "memory_usage_bytes": profile.get("memory_usage_bytes", 0),
            "columns": columns_meta,
            "preview_rows": preview_rows,
        })
    except Exception as e:
        logger.error(f"Error profiling dataset {file_path}: {e}")
        return jsonify({"error": str(e)}), 500


# ==============================================================================
# Audit Execution & Export Endpoints (Phase 4)
# ==============================================================================

@app.route("/api/audit/run", methods=["POST"])
def run_audit():
    """Execute representation-gap audit on a tabular dataset."""
    body = request.get_json() or {}
    file_path = body.get("file_path")
    dimensions_spec = body.get("dimensions", [])
    intersectional_pairs = body.get("intersectional_pairs") or None
    confidence_level = float(body.get("confidence_level", 0.95))

    if not file_path:
        return jsonify({"error": "Missing 'file_path'"}), 400
    if not dimensions_spec:
        return jsonify({"error": "At least one audit dimension must be configured"}), 400

    path_obj = Path(file_path)
    if not path_obj.exists():
        return jsonify({"error": f"File not found: {file_path}"}), 404

    try:
        audit_dimensions = []
        for d in dimensions_spec:
            dim = AuditDimension(
                name=d["name"],
                column_name=d["column_name"],
                dimension_type=d.get("dimension_type", "demographic"),
                expected_distribution=d.get("expected_distribution"),
                expected_categories=d.get("expected_categories"),
                min_sample_size=int(d.get("min_sample_size", 30)),
            )
            audit_dimensions.append(dim)

        parsed_pairs = None
        if intersectional_pairs:
            parsed_pairs = [tuple(p) for p in intersectional_pairs]

        config = AuditConfig(
            dimensions=audit_dimensions,
            intersectional_pairs=parsed_pairs,
            confidence_level=confidence_level,
        )

        engine = RepresentationAuditEngine(config=config)
        report = engine.audit(path_obj)
        report_dict = report.to_dict()

        # Cache report in-memory with unique ID for export
        report_id = f"report_{int(time.time())}_{path_obj.stem}"
        _audit_reports_cache[report_id] = report
        report_dict["report_id"] = report_id

        return jsonify({
            "status": "success",
            "report_id": report_id,
            "report": report_dict,
            "summary_text": report.format_text_summary(),
        })

    except Exception as e:
        logger.error(f"Failed to run audit: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/audit/export", methods=["POST"])
def export_audit():
    """Export an audit report to disk in JSON or CSV format."""
    import csv
    body = request.get_json() or {}
    report_id = body.get("report_id")
    export_format = body.get("format", "json").lower()

    if not report_id or report_id not in _audit_reports_cache:
        return jsonify({"error": f"Report ID '{report_id}' not found in session cache"}), 404

    report: AuditReport = _audit_reports_cache[report_id]

    try:
        if export_format == "csv":
            target_path = Path("outputs/audit_reports") / f"{report_id}.csv"
            rows = []
            for dim_name, dim_data in report.dimensions.items():
                for cat, p in dim_data.proportions.items():
                    rows.append({
                        "dimension": dim_name,
                        "category": cat,
                        "count": p["count"],
                        "share": p["share"],
                        "ci_lower": p["ci_lower"],
                        "ci_upper": p["ci_upper"],
                        "sparse": p["sample_size_sparse"],
                        "dim_missing_rate": dim_data.missing_rate,
                        "dim_coverage_ratio": dim_data.coverage_ratio,
                        "dim_max_abs_deviation": dim_data.max_abs_deviation,
                    })
            if rows:
                with open(target_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                    writer.writeheader()
                    writer.writerows(rows)
            else:
                target_path.write_text("dimension,category,count,share\n", encoding="utf-8")
        else:
            target_path = Path("outputs/audit_reports") / f"{report_id}.json"
            with open(target_path, "w", encoding="utf-8") as f:
                import json
                json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)

        return jsonify({
            "status": "success",
            "format": export_format,
            "file_path": str(target_path).replace("\\", "/"),
            "file_name": target_path.name,
            "size_bytes": target_path.stat().st_size,
        })
    except Exception as e:
        logger.error(f"Export failed: {e}")
        return jsonify({"error": str(e)}), 500


# ==============================================================================
# Research Workspace & Nemotron Telemetry (Phase 2 & Layer B)
# ==============================================================================

@app.route("/api/research/status", methods=["GET"])
def research_status():
    """Telemetry and research roadmap for Layer B (Nemotron 3 Ultra Indian Legal & Financial Case Study)."""
    settings = get_settings()

    return jsonify({
        "layer_b_case_study": {
            "target_model": settings.openrouter_model,
            "model_architecture": "550B total parameter Mixture-of-Experts (MoE) with ~55B active parameters per forward pass",
            "openrouter_model_id": "nvidia/nemotron-3-ultra-550b-a55b",
            "free_tier_variant": "nvidia/nemotron-3-ultra-550b-a55b:free",
            "pricing": {
                "free_tier": "$0.00 / 1M tokens (subject to provider prompt logging)",
                "paid_tier_estimate": "$0.60 / 1M input tokens, $3.60 / 1M output tokens",
                "max_spend_ceiling": f"${settings.max_spend_usd:.2f} USD",
                "warn_threshold": f"${settings.warn_spend_usd:.2f} USD"
            },
            "status": "PLANNED (Future Phase - Review 2 / Final Thesis)",
            "safety_card_findings": {
                "source": "NVIDIA Official Nemotron-3 Safety Documentation",
                "bias_mitigation_claim": "None (relies on external classifier guardrails, not regex filtering)",
                "demographic_parities": "Unverified on Indian jurisdictional and statutory reasoning"
            },
            "methodology": {
                "domains": [
                    "Indian Penal Code (IPC) / Bharatiya Nyaya Sanhita (BNS) Statutory Offenses",
                    "SEBI / RBI Financial Regulations and Dispute Adjudication"
                ],
                "evaluation_protocol": [
                    "Step 1: Construct 200 paired counterfactual legal vignettes (varying demographic identifiers).",
                    "Step 2: Measure prompt noise floor by evaluating identical prompts across temperature seeds.",
                    "Step 3: Measure statutory flip rate (decision change solely due to religion/gender/state change).",
                    "Step 4: Ground corrective prompts in Supreme Court of India precedents and verified statutes.",
                    "Step 5: QLoRA fine-tuning of an open 3B-4B parameter model using verified Indian legal corpora."
                ],
                "disclaimer": "CRITICAL: No experimental Nemotron benchmark numbers or flip rates have been measured yet. All numbers in this section represent verified architectural specifications and planned experimental methodology only."
            }
        }
    })


@app.route("/api/research/estimate-cost", methods=["POST"])
def estimate_cost():
    """Calculate exact token cost estimates against FairLens budget ceilings."""
    body = request.get_json() or {}
    runs = int(body.get("runs", 1))
    input_tokens = int(body.get("input_tokens", 1000))
    output_tokens = int(body.get("output_tokens", 500))
    use_free_tier = bool(body.get("use_free_tier", False))

    estimator = CostEstimator()
    estimate = estimator.estimate(
        total_requests=runs,
        avg_input_tokens=input_tokens,
        avg_output_tokens=output_tokens,
        use_free_tier=use_free_tier,
        enforce_budget=False,
    )

    return jsonify({
        "runs": estimate.total_requests,
        "input_tokens_total": estimate.estimated_input_tokens,
        "output_tokens_total": estimate.estimated_output_tokens,
        "input_cost_usd": round(estimate.base_input_cost, 6),
        "output_cost_usd": round(estimate.base_output_cost, 6),
        "base_total_usd": round(estimate.base_total_cost, 6),
        "total_cost_usd": round(estimate.projected_total_cost, 6),
        "safety_margin": estimate.safety_margin,
        "is_within_budget": estimate.within_budget,
        "budget_limit_usd": estimate.budget_limit,
    })


def create_app() -> Flask:
    """Application factory for WSGI / ASGI runners."""
    return app


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "127.0.0.1")
    logger.info(f"Starting FairLens REST API server on http://{host}:{port}")
    app.run(host=host, port=port, debug=False)
