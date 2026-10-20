"""
Unit tests for FairLens tabular data loader.
"""

import tempfile
import unittest
from pathlib import Path
import pandas as pd
from fairlens.auditing.loader import TabularDataLoader


class TestDataLoader(unittest.TestCase):
    """Test suite for tabular data ingestion, profiling, and error checks."""

    def test_load_valid_csv(self):
        """Verify loading CSV with profiling metadata."""
        path = Path("tests/fixtures/auditing/balanced.csv")
        df, profile = TabularDataLoader.load(path)

        self.assertEqual(len(df), 100)
        self.assertEqual(profile["total_rows"], 100)
        self.assertIn("gender", df.columns)
        self.assertEqual(profile["format"], "csv")

    def test_load_empty_file_raises_value_error(self):
        """Ensure empty dataset raises descriptive ValueError."""
        path = Path("tests/fixtures/auditing/empty.csv")
        with self.assertRaises(ValueError):
            TabularDataLoader.load(path)

    def test_nonexistent_file_raises_error(self):
        """Ensure missing file raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            TabularDataLoader.load(Path("nonexistent_path_12345.csv"))

    def test_unsupported_extension_raises_error(self):
        """Ensure non-tabular extension raises ValueError."""
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            with self.assertRaises(ValueError):
                TabularDataLoader.load(Path(tmp.name))


if __name__ == "__main__":
    unittest.main()
