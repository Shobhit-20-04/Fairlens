"""
Unit tests for FairLens RepresentationAuditEngine.
"""

import shutil
import tempfile
import unittest
from pathlib import Path

from fairlens.auditing.config import AuditConfig, AuditDimension
from fairlens.auditing.engine import RepresentationAuditEngine


class TestAuditingEngine(unittest.TestCase):
    """Test suite for representation auditing on diverse synthetic test scenarios."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_balanced_dataset_audit(self):
        """Verify audit on balanced 50/50 dataset achieves high parity score and zero warnings."""
        dim = AuditDimension(
            name="gender",
            column_name="gender",
            expected_distribution={"Male": 0.50, "Female": 0.50},
        )
        config = AuditConfig(dimensions=[dim])
        engine = RepresentationAuditEngine(config)

        report = engine.audit(Path("tests/fixtures/auditing/balanced.csv"))
        res = report.dimensions["gender"]

        self.assertEqual(res.valid_records, 100)
        self.assertEqual(res.missing_records, 0)
        self.assertAlmostEqual(res.max_abs_deviation, 0.0, places=3)
        self.assertEqual(res.scorecard.parity_score, 100.0)
        self.assertEqual(len(res.warnings), 0)

    def test_imbalanced_dataset_triggers_severe_deviation_warning(self):
        """Verify 90/10 imbalanced dataset triggers WARN_SEVERE_DEVIATION."""
        dim = AuditDimension(
            name="gender",
            column_name="gender",
            expected_distribution={"Male": 0.50, "Female": 0.50},
        )
        config = AuditConfig(dimensions=[dim])
        engine = RepresentationAuditEngine(config)

        report = engine.audit(Path("tests/fixtures/auditing/imbalanced.csv"))
        res = report.dimensions["gender"]

        self.assertAlmostEqual(res.max_abs_deviation, 0.40, places=3)
        warning_ids = [w.warning_id for w in res.warnings]
        self.assertIn("WARN_SEVERE_DEVIATION", warning_ids)
        self.assertLess(res.scorecard.parity_score, 70.0)

    def test_missing_category_triggers_zero_obs_warning(self):
        """Verify missing expected category triggers WARN_ZERO_OBSERVATION."""
        dim = AuditDimension(
            name="caste_group",
            column_name="caste_group",
            expected_categories=["Group_A", "Group_B", "Group_C"],
        )
        config = AuditConfig(dimensions=[dim])
        engine = RepresentationAuditEngine(config)

        report = engine.audit(Path("tests/fixtures/auditing/missing_categories.csv"))
        res = report.dimensions["caste_group"]

        self.assertEqual(res.zero_observation_categories, ["Group_C"])
        self.assertAlmostEqual(res.coverage_ratio, 2 / 3, places=2)
        warning_ids = [w.warning_id for w in res.warnings]
        self.assertIn("WARN_ZERO_OBSERVATION", warning_ids)

    def test_high_missingness_triggers_warning(self):
        """Verify dataset with missing/null markers triggers WARN_HIGH_MISSINGNESS."""
        dim = AuditDimension(name="gender", column_name="gender")
        config = AuditConfig(dimensions=[dim])
        engine = RepresentationAuditEngine(config)

        report = engine.audit(Path("tests/fixtures/auditing/with_nulls.csv"))
        res = report.dimensions["gender"]

        self.assertGreater(res.missing_rate, 0.15)
        warning_ids = [w.warning_id for w in res.warnings]
        self.assertIn("WARN_HIGH_MISSINGNESS", warning_ids)

    def test_no_reference_distribution_omits_parity_score(self):
        """Verify descriptive audit without expected distribution leaves parity score None."""
        dim = AuditDimension(name="category", column_name="category")
        config = AuditConfig(dimensions=[dim])
        engine = RepresentationAuditEngine(config)

        report = engine.audit(Path("tests/fixtures/auditing/single_category.csv"))
        res = report.dimensions["category"]

        self.assertIsNone(res.scorecard.parity_score)
        self.assertIsNone(res.scorecard.composite_score)
        self.assertEqual(res.scorecard.completeness_score, 100.0)

    def test_realistic_indian_legal_audit_and_intersectional(self):
        """Audit 1,000-row synthetic Indian legal dataset across multiple dimensions."""
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
        engine = RepresentationAuditEngine(config)

        report = engine.audit(Path("tests/fixtures/auditing/indian_legal_synthetic_audit.csv"))

        self.assertEqual(len(report.dimensions), 3)
        self.assertIn("gender__x__state", report.intersectional_results)
        self.assertGreater(report.execution_time_seconds, 0.0)

        # Test text summary generation
        summary = report.format_text_summary()
        self.assertIn("FAIRLENS DATASET REPRESENTATION AUDIT REPORT", summary)
        self.assertIn("ASSUMPTIONS & LIMITATIONS", summary)

    def test_export_audit_report(self):
        """Test exporting audit report to JSON and CSV formats."""
        dim = AuditDimension(name="gender", column_name="gender")
        config = AuditConfig(dimensions=[dim])
        engine = RepresentationAuditEngine(config)
        report = engine.audit(Path("tests/fixtures/auditing/balanced.csv"))

        json_file = Path(self.temp_dir) / "audit_report.json"
        csv_file = Path(self.temp_dir) / "audit_report.csv"

        engine.export_report(report, json_file, format="json")
        self.assertTrue(json_file.exists())

        engine.export_report(report, csv_file, format="csv")
        self.assertTrue(csv_file.exists())


if __name__ == "__main__":
    unittest.main()
