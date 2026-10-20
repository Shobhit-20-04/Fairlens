"""
Tabular Data Loader and Ingestion Profiler for FairLens.

Supports CSV, Parquet, TSV, and Excel formats with format validation,
duplicate detection, and data-type profiling without modifying source files.
"""

from pathlib import Path
from typing import Any, Dict, List, Tuple
import pandas as pd
from fairlens.config.logging import get_logger

logger = get_logger("auditing.loader")


class TabularDataLoader:
    """Safe, read-only data loader for tabular audit datasets."""

    SUPPORTED_EXTENSIONS = {".csv", ".parquet", ".pq", ".tsv", ".xlsx", ".xls"}

    @classmethod
    def load(cls, file_path: Path) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Load tabular dataset from disk and return (DataFrame, profiling_metadata).

        Raises ValueError or FileNotFoundError if file is missing, empty, or unsupported.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Dataset file not found: {path.resolve()}")

        suffix = path.suffix.lower()
        if suffix not in cls.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file format '{suffix}'. Supported formats: {', '.join(sorted(cls.SUPPORTED_EXTENSIONS))}"
            )

        logger.info("Loading tabular dataset: %s", path.name)

        try:
            if suffix in (".csv", ".tsv"):
                sep = "\t" if suffix == ".tsv" else ","
                df = pd.read_csv(path, sep=sep, low_memory=False)
            elif suffix in (".parquet", ".pq"):
                df = pd.read_parquet(path)
            elif suffix in (".xlsx", ".xls"):
                df = pd.read_excel(path)
            else:
                raise ValueError(f"Unhandled file extension: {suffix}")
        except Exception as e:
            raise ValueError(f"Failed to parse tabular file '{path.name}': {e}")

        if df.empty:
            raise ValueError(f"Dataset '{path.name}' is empty (0 rows)")

        # Profiling summary
        initial_rows = len(df)
        duplicates = int(df.duplicated().sum())
        column_types: Dict[str, str] = {}
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                column_types[col] = "numeric"
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                column_types[col] = "datetime"
            elif pd.api.types.is_bool_dtype(df[col]):
                column_types[col] = "boolean"
            else:
                column_types[col] = "categorical"

        profile: Dict[str, Any] = {
            "file_name": path.name,
            "file_path": str(path.resolve()),
            "format": suffix.replace(".", ""),
            "total_rows": initial_rows,
            "total_columns": len(df.columns),
            "duplicate_rows": duplicates,
            "duplicate_rate": round(duplicates / initial_rows, 4) if initial_rows > 0 else 0.0,
            "memory_usage_bytes": int(df.memory_usage(deep=True).sum()),
            "columns": list(df.columns),
            "column_types": column_types,
        }

        logger.info(
            "Dataset loaded successfully: %d rows, %d columns, %d duplicate rows",
            initial_rows,
            len(df.columns),
            duplicates,
        )
        return df, profile
