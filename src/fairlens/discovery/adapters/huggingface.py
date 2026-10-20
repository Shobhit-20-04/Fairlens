"""
Hugging Face Hub Dataset Discovery Adapter.

Connects to Hugging Face Datasets via official REST API / huggingface_hub library,
extracting tags, modalities, licenses, and author metadata.
"""

from typing import List, Optional
import requests
from fairlens.config.logging import get_logger
from fairlens.config.settings import Settings, get_settings
from fairlens.discovery.base import BaseDiscoveryAdapter
from fairlens.discovery.schema import DiscoveryQuery, NormalizedDatasetMetadata

logger = get_logger("discovery.huggingface")


class HuggingFaceDiscoveryAdapter(BaseDiscoveryAdapter):
    """Adapter for searching datasets on Hugging Face Hub."""

    API_ENDPOINT = "https://huggingface.co/api/datasets"

    def __init__(self, settings: Optional[Settings] = None):
        super().__init__(provider_name="huggingface")
        self.settings = settings or get_settings()

    def is_configured(self) -> bool:
        """Hugging Face public search does not mandate tokens."""
        return True

    def requires_auth(self) -> bool:
        """Public search is anonymous; auth only needed for gated datasets."""
        return False

    def search(self, query: DiscoveryQuery) -> List[NormalizedDatasetMetadata]:
        """Search Hugging Face Hub for candidate datasets."""
        if self.settings.offline_mode:
            logger.debug("Hugging Face adapter in offline mode; returning empty or relying on fixtures.")
            return []

        params = {
            "search": query.keywords,
            "limit": min(query.limit, 50),
            "full": "true",
        }
        headers = {}
        if self.settings.huggingface_token:
            headers["Authorization"] = f"Bearer {self.settings.huggingface_token}"

        try:
            response = requests.get(self.API_ENDPOINT, params=params, headers=headers, timeout=15)
            if response.status_code != 200:
                logger.warning("Hugging Face API returned status %d", response.status_code)
                return []

            raw_datasets = response.json()
            normalized: List[NormalizedDatasetMetadata] = []

            for item in raw_datasets:
                dataset_id = item.get("id", "")
                tags = item.get("tags", [])
                description = item.get("description", "") or f"Hugging Face dataset {dataset_id}"

                # Extract languages, licenses, and domains from tags
                languages = [t.replace("language:", "") for t in tags if t.startswith("language:")]
                licenses = [t.replace("license:", "") for t in tags if t.startswith("license:")]
                primary_license = licenses[0] if licenses else "unknown"

                # Check for geographic or Indian domain tags
                geography = []
                if any("india" in t.lower() for t in tags) or "india" in dataset_id.lower():
                    geography.append("India")

                domain = "general"
                if any(t in ("legal", "law", "judgments") for t in tags) or "legal" in dataset_id.lower():
                    domain = "legal"
                elif any(t in ("finance", "banking", "financial") for t in tags) or "fin" in dataset_id.lower():
                    domain = "finance"

                # Check format
                format_type = "tabular" if any(t in ("csv", "parquet", "json") for t in tags) else "nlp"

                record = NormalizedDatasetMetadata(
                    name=dataset_id.split("/")[-1] if "/" in dataset_id else dataset_id,
                    dataset_id=dataset_id,
                    source_provider="huggingface",
                    canonical_url=f"https://huggingface.co/datasets/{dataset_id}",
                    description=description[:500],
                    domain=domain,
                    task_type=format_type,
                    geography=geography,
                    languages=languages,
                    format=format_type,
                    license=primary_license,
                    license_verified=primary_license != "unknown",
                    last_updated=item.get("lastModified"),
                    search_query=query.keywords,
                    verification_status="verified_api",
                )
                normalized.append(record)

            return normalized

        except requests.RequestException as e:
            logger.warning("Network connection to Hugging Face API failed: %s", e)
            return []
