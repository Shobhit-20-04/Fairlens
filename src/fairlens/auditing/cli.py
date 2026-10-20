"""
CLI Entry Point for FairLens Dataset Representation Audit.
"""

import argparse
import sys
from pathlib import Path
from fairlens.auditing.config import AuditConfig, AuditDimension
from fairlens.auditing.engine import RepresentationAuditEngine


def main():
    parser = argparse.ArgumentParser(description="FairLens Tabular Dataset Representation Audit Engine")
    parser.add_argument("dataset", type=str, help="Path to tabular dataset (CSV, Parquet, or Excel)")
    parser.add_argument("--dimension", action="append", nargs=2, metavar=("NAME", "COLUMN"), required=True,
                        help="Specify audit dimension as: --dimension <name> <column>")
    parser.add_argument("--export", type=str, default=None, help="Path to export structured report (.json or .csv)")
    parser.add_argument("--confidence", type=float, default=0.95, help="Confidence level for Wilson intervals")

    args = parser.parse_args()

    dimensions = [
        AuditDimension(name=name, column_name=col)
        for name, col in args.dimension
    ]
    config = AuditConfig(dimensions=dimensions, confidence_level=args.confidence)
    engine = RepresentationAuditEngine(config)

    report = engine.audit(args.dataset)
    print(report.format_text_summary())

    if args.export:
        fmt = "csv" if args.export.endswith(".csv") else "json"
        engine.export_report(report, args.export, format=fmt)
        print(f"\n[+] Exported audit report to {args.export}")


if __name__ == "__main__":
    main()
