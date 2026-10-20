"""
Unit tests for FairLens DatasetDiscoveryEngine.
"""

import shutil
import tempfile
import unittest
from pathlib import Path

from fairlens.discovery.base import BaseDiscoveryAdapter
from fairlens.discovery.engine import DatasetDiscoveryEngine
from fairlens.discovery.schema import DiscoveryQuery, NormalizedDatasetMetadata


class FailingMockAdapter(BaseDiscoveryAdapter):
    """Adapter intentionally raising exceptions to test provider error isolation."""

    def __init__(self):
        super().__init__(provider_name="failing_mock")

    def is_configured(self) -> bool:
        return True

    def requires_auth(self) -> bool:
        return False

    def search(self, query: DiscoveryQuery):
        raise ConnectionResetError("Simulated remote network reset")


class TestDiscoveryEngine(unittest.TestCase):
    """Test suite for multi-source discovery, filtering, and error isolation."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.fixtures_path = Path("tests/fixtures/discovery/sample_datasets.json")
        self.engine = DatasetDiscoveryEngine(
            use_fixtures_only=True,
            fixtures_path=self.fixtures_path,
        )

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_fixture_search_and_keyword_match(self):
        """Verify keyword matching across offline fixtures."""
        query = DiscoveryQuery(keywords="legal IPC reasoning")
        result = self.engine.search(query)

        self.assertGreaterEqual(result.total_found, 1)
        found_names = [d.name for d in result.datasets]
        self.assertTrue(any("InSaAF" in n for n in found_names))

    def test_domain_and_geography_filtering(self):
        """Verify secondary domain and geography filtering."""
        query = DiscoveryQuery(keywords="India", domain="finance")
        result = self.engine.search(query)

        for ds in result.datasets:
            self.assertEqual(ds.domain, "finance")

    def test_deduplication(self):
        """Test deduplication removes duplicate records with identical canonical URL."""
        ds1 = NormalizedDatasetMetadata(name="A", dataset_id="1", source_provider="hf", canonical_url="https://a.org")
        ds2 = NormalizedDatasetMetadata(name="A duplicate", dataset_id="2", source_provider="zenodo", canonical_url="https://a.org")
        ds3 = NormalizedDatasetMetadata(name="B", dataset_id="3", source_provider="uci", canonical_url="https://b.org")

        deduped = self.engine._deduplicate([ds1, ds2, ds3])
        self.assertEqual(len(deduped), 2)
        self.assertEqual(deduped[0].canonical_url, "https://a.org")
        self.assertEqual(deduped[1].canonical_url, "https://b.org")

    def test_pagination(self):
        """Test offset and limit pagination."""
        q_all = DiscoveryQuery(keywords="", limit=10)
        res_all = self.engine.search(q_all)
        total = res_all.total_found

        if total >= 2:
            q_page = DiscoveryQuery(keywords="", limit=1, offset=1)
            res_page = self.engine.search(q_page)
            self.assertEqual(len(res_page.datasets), 1)
            self.assertEqual(res_page.datasets[0].name, res_all.datasets[1].name)

    def test_provider_error_isolation(self):
        """Verify a failing provider does not crash the discovery engine."""
        self.engine.register_adapter("failing_mock", FailingMockAdapter())
        query = DiscoveryQuery(keywords="credit", providers=["failing_mock", "uci"])

        # When running live adapters (temporarily disable fixture mode for this test)
        self.engine.use_fixtures = False
        result = self.engine.search(query)

        self.assertIn("failing_mock", result.provider_counts)
        self.assertEqual(result.provider_counts["failing_mock"], 0)
        self.assertIn("uci", result.provider_counts)
        self.assertGreaterEqual(result.provider_counts["uci"], 1)

    def test_export_json_and_csv(self):
        """Test exporting discovery results to JSON and CSV formats."""
        query = DiscoveryQuery(keywords="credit")
        result = self.engine.search(query)

        json_out = Path(self.temp_dir) / "discovery_out.json"
        csv_out = Path(self.temp_dir) / "discovery_out.csv"

        self.engine.export_results(result, json_out, format="json")
        self.assertTrue(json_out.exists())

        self.engine.export_results(result, csv_out, format="csv")
        self.assertTrue(csv_out.exists())


if __name__ == "__main__":
    unittest.main()
