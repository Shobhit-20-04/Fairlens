"""
Zenodo REST API Dataset Discovery Adapter.

Connects to CERN / Zenodo Open Science Repository, querying open scientific
datasets and harvesting verified DOI and licensing metadata.
"""

from typing import List, Optional
import requests
from fairlens.config.logging import get_logger
from fairlens.config.settings import Settings, get_settings
from fairlens.discovery.base import BaseDiscoveryAdapter
from fairlens.discovery.schema import DiscoveryQuery, NormalizedDatasetMetadata

logger = get_logger("discovery.zenodo")


class ZenodoDiscoveryAdapter(BaseDiscoveryAdapter):
    """Adapter for searching open scientific datasets on Zenodo."""

    API_ENDPOINT = "https://zenodo.org/api/records"

    def __init__(self, settings: Optional[Settings] = None):
        super().__init__(provider_name="zenodo")
        self.settings = settings or get_settings()

    def is_configured(self) -> bool:
        """Zenodo public records API is open without mandatory authentication."""
        return True

    def requires_auth(self) -> bool:
        return False

    def search(self, query: DiscoveryQuery) -> List[NormalizedDatasetMetadata]:
        """Search Zenodo records for matching research datasets."""
        if self.settings.offline_mode:
            logger.debug("Zenodo adapter running in offline mode.")
            return []

        params = {
            "q": query.keywords,
            "type": "dataset",
            "size": min(query.limit, 20),
            "sort": "bestmatch",
        }
        headers = {}
        if self.settings.zenodo_access_token:
            headers["Authorization"] = f"Bearer {self.settings.zenodo_access_token}"

        try:
            response = requests.get(self.API_ENDPOINT, params=params, headers=headers, timeout=15)
            if response.status_code != 200:
                logger.warning("Zenodo API returned status %d", response.status_code)
                return []

            data = response.json()
            hits = data.get("hits", {}).get("hits", [])
            normalized: List[NormalizedDatasetMetadata] = []

            for item in hits:
                metadata = item.get("metadata", {})
                record_id = str(item.get("id", ""))
                title = metadata.get("title", f"Zenodo Record {record_id}")
                description = metadata.get("description", "")
                doi = item.get("doi", f"10.5281/zenodo.{record_id}")
                license_info = metadata.get("license", {}).get("id", "open-access")

                geography = []
                if "india" in title.lower() or "india" in description.lower():
                    geography.append("India")

                domain = "general"
                if any(w in title.lower() or w in description.lower() for w in ("legal", "court", "law")):
                    domain = "legal"
                elif any(w in title.lower() or w in description.lower() for w in ("finance", "economic", "bank")):
                    domain = "finance"

                record = NormalizedDatasetMetadata(
                    name=title,
                    dataset_id=f"zenodo.{record_id}",
                    source_provider="zenodo",
                    canonical_url=item.get("links", {}).get("html", f"https://zenodo.org/record/{record_id}"),
                    description=description[:500],
                    domain=domain,
                    task_type="scientific-data",
                    geography=geography,
                    format="archive/data",
                    license=license_info,
                    license_verified=True,
                    publication_date=metadata.get("publication_date"),
                    search_query=query.keywords,
                    verification_status="verified_api",
                )
                normalized.append(record)

            return normalized

        except requests.RequestException as e:
            logger.warning("Network connection to Zenodo API failed: %s", e)
            return []
