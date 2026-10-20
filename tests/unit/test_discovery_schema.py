"""
Unit tests for FairLens dataset discovery metadata schema and suitability scoring.
"""

import unittest
from fairlens.discovery.schema import DiscoveryQuery, NormalizedDatasetMetadata


class TestDiscoverySchema(unittest.TestCase):
    """Test suite for NormalizedDatasetMetadata completeness and suitability logic."""

    def test_completeness_scoring(self):
        """Test metadata completeness score calculation."""
        # Full record
        full_ds = NormalizedDatasetMetadata(
            name="InSaAF Benchmark",
            dataset_id="crai/insaaf",
            source_provider="huggingface",
            canonical_url="https://huggingface.co/datasets/crai/insaaf",
            description="Comprehensive statutory reasoning benchmark evaluating IPC sections across caste and gender.",
            domain="legal",
            task_type="tabular",
            geography=["India"],
            available_features=["scenario", "section", "label"],
            format="csv",
            license="Apache-2.0",
        )
        self.assertGreaterEqual(full_ds.metadata_completeness_score, 0.85)
        self.assertEqual(len(full_ds.missing_fields), 0)
        self.assertEqual(full_ds.audit_suitability, "high")

        # Incomplete record
        sparse_ds = NormalizedDatasetMetadata(
            name="Sparse Data",
            dataset_id="sparse.123",
            source_provider="unknown",
            canonical_url="https://example.com/sparse",
            description="Short desc",
            domain="general",
            format="unknown",
            license="unknown",
        )
        self.assertLess(sparse_ds.metadata_completeness_score, 0.5)
        self.assertIn("format", sparse_ds.missing_fields)
        self.assertIn("license", sparse_ds.missing_fields)
        self.assertEqual(sparse_ds.audit_suitability, "low")

    def test_to_dict_serialization(self):
        """Test serialization to dictionary."""
        ds = NormalizedDatasetMetadata(
            name="Test Dataset",
            dataset_id="test.1",
            source_provider="zenodo",
            canonical_url="https://zenodo.org/record/123",
        )
        d = ds.to_dict()
        self.assertIsInstance(d, dict)
        self.assertEqual(d["name"], "Test Dataset")
        self.assertEqual(d["source_provider"], "zenodo")


if __name__ == "__main__":
    unittest.main()
