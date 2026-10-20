"""
Aggregated Dataset Discovery Engine for FairLens.

Orchestrates multi-source queries across Hugging Face, Zenodo, Data.gov,
Kaggle, and UCI repositories with isolated error handling, deduplication,
offline fixture fallbacks, and export capabilities.
"""

import csv
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from fairlens.config.logging import get_logger
from fairlens.config.settings import Settings, get_settings
from fairlens.discovery.adapters.data_gov import DataGovDiscoveryAdapter
from fairlens.discovery.adapters.huggingface import HuggingFaceDiscoveryAdapter
from fairlens.discovery.adapters.kaggle import KaggleDiscoveryAdapter
from fairlens.discovery.adapters.uci import UCIDiscoveryAdapter
from fairlens.discovery.adapters.zenodo import ZenodoDiscoveryAdapter
from fairlens.discovery.base import BaseDiscoveryAdapter
from fairlens.discovery.schema import DiscoveryQuery, DiscoveryResult, NormalizedDatasetMetadata

logger = get_logger("discovery.engine")


class DatasetDiscoveryEngine:
    """Master discovery engine managing multi-source dataset discovery."""

    def __init__(
        self,
        settings: Optional[Settings] = None,
        use_fixtures_only: bool = False,
        fixtures_path: Optional[Path] = None,
    ):
        self.settings = settings or get_settings()
        self.use_fixtures = use_fixtures_only or self.settings.offline_mode
        self.fixtures_path = fixtures_path or Path("tests/fixtures/discovery/sample_datasets.json")
        self.adapters: Dict[str, BaseDiscoveryAdapter] = {
            "huggingface": HuggingFaceDiscoveryAdapter(self.settings),
            "zenodo": ZenodoDiscoveryAdapter(self.settings),
            "data_gov": DataGovDiscoveryAdapter(self.settings),
            "kaggle": KaggleDiscoveryAdapter(self.settings),
            "uci": UCIDiscoveryAdapter(self.settings),
        }

    def register_adapter(self, name: str, adapter: BaseDiscoveryAdapter) -> None:
        """Register a custom discovery adapter."""
        self.adapters[name] = adapter

    def get_provider_status(self) -> Dict[str, Dict[str, Any]]:
        """Return configuration and authentication status for each provider."""
        status = {}
        for name, adapter in self.adapters.items():
            status[name] = {
                "configured": adapter.is_configured(),
                "requires_auth": adapter.requires_auth(),
                "offline_fallback_supported": True,
            }
        return status

    def search(self, query: DiscoveryQuery) -> DiscoveryResult:
        """Execute federated dataset search across configured repositories."""
        start_time = time.time()
        provider_counts: Dict[str, int] = {}
        provider_errors: Dict[str, str] = {}
        all_datasets: List[NormalizedDatasetMetadata] = []

        # Determine which providers to query
        target_providers = query.providers or list(self.adapters.keys())

        # If offline or fixture mode is enabled, load offline fixtures
        if self.use_fixtures:
            logger.info("Executing search in OFFLINE / FIXTURE mode using %s", self.fixtures_path)
            fixtures = self._load_fixtures()
            filtered_fixtures = self._filter_fixtures(fixtures, query)
            for ds in filtered_fixtures:
                provider_counts[ds.source_provider] = provider_counts.get(ds.source_provider, 0) + 1
            all_datasets.extend(filtered_fixtures)
        else:
            # Query live provider adapters with complete error isolation
            for provider_name in target_providers:
                if provider_name not in self.adapters:
                    provider_errors[provider_name] = f"Unknown provider '{provider_name}'"
                    continue

                adapter = self.adapters[provider_name]
                try:
                    results = adapter.safe_search(query)
                    provider_counts[provider_name] = len(results)
                    all_datasets.extend(results)
                except Exception as e:
                    logger.error("Error from provider %s: %s", provider_name, e)
                    provider_errors[provider_name] = str(e)
                    provider_counts[provider_name] = 0

        # Deduplicate datasets by canonical URL or dataset ID
        deduplicated = self._deduplicate(all_datasets)

        # Apply secondary filters if requested (domain, geography, task_type)
        filtered = self._apply_secondary_filters(deduplicated, query)

        # Sort by metadata completeness descending
        filtered.sort(key=lambda d: d.metadata_completeness_score, reverse=True)

        # Apply pagination (offset & limit)
        paginated = filtered[query.offset : query.offset + query.limit]

        elapsed = time.time() - start_time
        return DiscoveryResult(
            query=query,
            datasets=paginated,
            total_found=len(filtered),
            provider_counts=provider_counts,
            provider_errors=provider_errors,
            execution_time_seconds=elapsed,
        )

    def _deduplicate(
        self, datasets: List[NormalizedDatasetMetadata]
    ) -> List[NormalizedDatasetMetadata]:
        """Eliminate duplicate datasets across providers."""
        seen_keys = set()
        unique = []
        for ds in datasets:
            # Key on canonical URL or normalized name
            key = ds.canonical_url.lower() if ds.canonical_url else ds.name.lower()
            if key not in seen_keys:
                seen_keys.add(key)
                unique.append(ds)
        return unique

    def _apply_secondary_filters(
        self, datasets: List[NormalizedDatasetMetadata], query: DiscoveryQuery
    ) -> List[NormalizedDatasetMetadata]:
        """Filter results based on domain or geography if requested."""
        results = datasets
        if query.domain:
            target_domain = query.domain.lower()
            results = [d for d in results if target_domain in d.domain.lower()]

        if query.geography:
            target_geo = query.geography.lower()
            results = [
                d for d in results
                if any(target_geo in g.lower() for g in d.geography)
                or target_geo in d.description.lower()
            ]

        if query.task_type:
            target_task = query.task_type.lower()
            results = [d for d in results if target_task in d.task_type.lower()]

        return results

    def _load_fixtures(self) -> List[NormalizedDatasetMetadata]:
        """Load deterministic test fixtures from JSON file."""
        if not self.fixtures_path.exists():
            logger.warning("Fixtures file not found at %s", self.fixtures_path)
            return []

        try:
            with open(self.fixtures_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            return [
                NormalizedDatasetMetadata(
                    name=item["name"],
                    dataset_id=item["dataset_id"],
                    source_provider=item["source_provider"],
                    canonical_url=item["canonical_url"],
                    description=item.get("description", ""),
                    domain=item.get("domain", "general"),
                    task_type=item.get("task_type", "tabular"),
                    geography=item.get("geography", []),
                    languages=item.get("languages", ["en"]),
                    documented_demographics=item.get("documented_demographics", []),
                    available_features=item.get("available_features", []),
                    format=item.get("format", "csv"),
                    license=item.get("license", "unknown"),
                    license_verified=item.get("license_verified", False),
                    row_count=item.get("row_count"),
                    verification_status=item.get("verification_status", "fixture"),
                )
                for item in raw_data
            ]
        except Exception as e:
            logger.error("Failed to load discovery fixtures: %s", e)
            return []

    def _filter_fixtures(
        self, fixtures: List[NormalizedDatasetMetadata], query: DiscoveryQuery
    ) -> List[NormalizedDatasetMetadata]:
        """Match query keywords and filters against fixture records."""
        keywords = query.keywords.lower().split()
        matches = []
        for f in fixtures:
            text = f"{f.name} {f.description} {f.domain} {' '.join(f.geography)} {' '.join(f.available_features)}".lower()
            if not keywords or any(k in text for k in keywords):
                f.search_query = query.keywords
                matches.append(f)
        return matches

    def export_results(self, result: DiscoveryResult, output_path: Path, format: str = "json") -> None:
        """Export discovery results to JSON or CSV."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format.lower() == "json":
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
            logger.info("Exported discovery results to %s", output_path)
        elif format.lower() == "csv":
            if not result.datasets:
                return
            keys = [
                "name", "dataset_id", "source_provider", "domain", "task_type",
                "format", "license", "metadata_completeness_score", "audit_suitability",
                "canonical_url",
            ]
            with open(output_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                for ds in result.datasets:
                    d = ds.to_dict()
                    writer.writerow({k: d.get(k, "") for k in keys})
            logger.info("Exported discovery results to CSV at %s", output_path)
        else:
            raise ValueError(f"Unsupported export format '{format}', must be 'json' or 'csv'")

    def format_report(self, result: DiscoveryResult) -> str:
        """Generate human-readable summary of discovery execution."""
        lines = [
            "===========================================================",
            "             FAIRLENS DATASET DISCOVERY REPORT             ",
            "===========================================================",
            f"Search Query: '{result.query.keywords}'",
            f"Total Unique Datasets Found: {result.total_found}",
            f"Execution Time: {result.execution_time_seconds:.3f} seconds",
            "\nProvider Breakdown:",
        ]
        for p, count in result.provider_counts.items():
            lines.append(f"  - {p}: {count} candidates")

        if result.provider_errors:
            lines.append("\nProvider Warnings / Errors:")
            for p, err in result.provider_errors.items():
                lines.append(f"  - {p}: {err}")

        lines.append("\nTop Matching Candidate Datasets:")
        for idx, ds in enumerate(result.datasets, 1):
            lines.append(
                f"\n[{idx}] {ds.name} ({ds.source_provider})"
                f"\n    URL: {ds.canonical_url}"
                f"\n    Domain: {ds.domain} | Format: {ds.format} | License: {ds.license}"
                f"\n    Metadata Completeness: {ds.metadata_completeness_score:.1%} | Audit Suitability: {ds.audit_suitability.upper()}"
                f"\n    Suitability Notes: {', '.join(ds.audit_suitability_reasons)}"
            )
        lines.append("===========================================================")
        return "\n".join(lines)
