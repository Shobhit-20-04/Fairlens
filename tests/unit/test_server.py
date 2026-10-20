"""
Unit tests for FairLens Backend REST API Server.
"""

import json
import unittest
from pathlib import Path
from fairlens.server.app import app


class TestServerEndpoints(unittest.TestCase):
    """Test suite for FairLens REST API endpoints."""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_health_check(self):
        """Test health check endpoint."""
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["version"], "0.1.0")
        self.assertIn("gpu", data)
        self.assertIn("python_version", data)

    def test_settings_view(self):
        """Test settings view with masked secrets."""
        res = self.client.get("/api/settings")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("budget", data)
        self.assertEqual(data["budget"]["max_spend_usd"], 5.0)
        self.assertIn("providers", data)

    def test_discovery_providers(self):
        """Test discovery providers list."""
        res = self.client.get("/api/discovery/providers")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        providers = data["providers"]
        self.assertGreaterEqual(len(providers), 4)
        ids = [p["id"] for p in providers]
        self.assertIn("huggingface", ids)
        self.assertIn("zenodo", ids)
        self.assertIn("uci", ids)

    def test_discovery_search(self):
        """Test discovery search endpoint in mock offline mode."""
        res = self.client.post(
            "/api/discovery/search",
            json={"query": "legal", "use_mock_offline": True, "limit": 5}
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("datasets", data)
        self.assertGreater(len(data["datasets"]), 0)
        self.assertIn("execution_time_seconds", data)

    def test_profiler_samples(self):
        """Test retrieval of pre-loaded sample datasets."""
        res = self.client.get("/api/profiler/samples")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        samples = data["samples"]
        self.assertGreater(len(samples), 0)
        names = [s["file_name"] for s in samples]
        self.assertIn("indian_legal_synthetic_audit.csv", names)

    def test_profiler_profile(self):
        """Test profiling of a tabular dataset."""
        sample_path = "tests/fixtures/auditing/indian_legal_synthetic_audit.csv"
        res = self.client.post(
            "/api/profiler/profile",
            json={"file_path": sample_path}
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["total_rows"], 1000)
        self.assertGreaterEqual(data["total_columns"], 5)
        self.assertGreaterEqual(len(data["columns"]), 5)
        self.assertGreater(len(data["preview_rows"]), 0)

    def test_audit_run_and_export(self):
        """Test running an audit via REST and exporting the report."""
        sample_path = "tests/fixtures/auditing/indian_legal_synthetic_audit.csv"
        payload = {
            "file_path": sample_path,
            "dimensions": [
                {
                    "name": "gender",
                    "column_name": "gender",
                    "dimension_type": "demographic",
                    "expected_distribution": {"Male": 0.48, "Female": 0.48, "Non-Binary": 0.04},
                    "expected_categories": ["Male", "Female", "Non-Binary"]
                }
            ]
        }
        res = self.client.post("/api/audit/run", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("report", data)
        self.assertIn("gender", data["report"]["dimensions"])
        report_id = data["report_id"]

        # Test JSON export
        res_exp = self.client.post("/api/audit/export", json={"report_id": report_id, "format": "json"})
        self.assertEqual(res_exp.status_code, 200)
        exp_data = res_exp.get_json()
        self.assertEqual(exp_data["format"], "json")
        self.assertTrue(Path(exp_data["file_path"]).exists())

        # Test CSV export
        res_csv = self.client.post("/api/audit/export", json={"report_id": report_id, "format": "csv"})
        self.assertEqual(res_csv.status_code, 200)
        csv_data = res_csv.get_json()
        self.assertEqual(csv_data["format"], "csv")
        self.assertTrue(Path(csv_data["file_path"]).exists())

    def test_research_status(self):
        """Test research status endpoint."""
        res = self.client.get("/api/research/status")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("layer_b_case_study", data)
        self.assertIn("nvidia/nemotron-3-ultra-550b-a55b", data["layer_b_case_study"]["openrouter_model_id"])
        self.assertIn("disclaimer", data["layer_b_case_study"]["methodology"])

    def test_cost_estimator(self):
        """Test cost calculation endpoint."""
        res = self.client.post("/api/research/estimate-cost", json={"input_tokens": 10000, "output_tokens": 2000, "runs": 3})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["input_tokens_total"], 30000)
        self.assertEqual(data["output_tokens_total"], 6000)
        self.assertGreater(data["total_cost_usd"], 0)
        self.assertTrue(data["is_within_budget"])


if __name__ == "__main__":
    unittest.main()
