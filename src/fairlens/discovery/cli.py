"""
CLI Interface for FairLens Dataset Discovery Engine.
"""

import argparse
import sys
from fairlens.discovery.engine import DatasetDiscoveryEngine
from fairlens.discovery.schema import DiscoveryQuery


def main():
    parser = argparse.ArgumentParser(description="FairLens Multi-Source Dataset Discovery Engine")
    parser.add_argument("keywords", type=str, help="Search keywords (e.g. 'Indian legal statutory reasoning')")
    parser.add_argument("--domain", type=str, default=None, help="Domain filter (legal, finance, sociodemographic)")
    parser.add_argument("--geography", type=str, default=None, help="Geography filter (e.g. 'India')")
    parser.add_argument("--limit", type=int, default=5, help="Maximum results to display")
    parser.add_argument("--export", type=str, default=None, help="Export output path (.json or .csv)")
    parser.add_argument("--offline", action="store_true", help="Force offline fixtures mode")

    args = parser.parse_args()

    engine = DatasetDiscoveryEngine(use_fixtures_only=args.offline)
    query = DiscoveryQuery(
        keywords=args.keywords,
        domain=args.domain,
        geography=args.geography,
        limit=args.limit,
    )

    result = engine.search(query)
    print(engine.format_report(result))

    if args.export:
        fmt = "csv" if args.export.endswith(".csv") else "json"
        engine.export_results(result, args.export, format=fmt)
        print(f"\n[+] Exported results to {args.export}")


if __name__ == "__main__":
    main()
