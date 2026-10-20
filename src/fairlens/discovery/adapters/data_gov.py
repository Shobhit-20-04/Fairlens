"""
Data.gov CKAN API Dataset Discovery Adapter.

Connects to open government data catalogues via the standard CKAN REST API,
retrieving government tabular datasets, department metadata, and public licenses.
"""

from typing import List, Optional
import requests
from fairlens.config.logging import get_logger
from fairlens.config.settings import Settings, get_settings
from fairlens.discovery.base import BaseDiscoveryAdapter
from fairlens.discovery.schema import DiscoveryQuery, NormalizedDatasetMetadata

logger = get_logger("discovery.data_gov")


class DataGovDiscoveryAdapter(BaseDiscoveryAdapter):
    """Adapter for searching open government catalogues."""

    API_ENDPOINT = "https://catalog.data.gov/api/3/action/package_search"

    def __init__(self, settings: Optional[Settings] = None):
        super().__init__(provider_name="data_gov")
        self.settings = settings or get_settings()

    def is_configured(self) -> bool:
        """CKAN package search is publicly queryable without mandatory token."""
        return True

    def requires_auth(self) -> bool:
        return False

    def search(self, query: DiscoveryQuery) -> List[NormalizedDatasetMetadata]:
        """Search Data.gov CKAN catalogue."""
        if self.settings.offline_mode:
            logger.debug("Data.gov adapter running in offline mode.")
            return []

        params = {
            "q": query.keywords,
            "rows": min(query.limit, 20),
        }
        headers = {}
        if self.settings.data_gov_api_key:
            headers["X-API-KEY"] = self.settings.data_gov_api_key

        try:
            response = requests.get(self.API_ENDPOINT, params=params, headers=headers, timeout=15)
            if response.status_code != 200:
                logger.warning("Data.gov CKAN API returned status %d", response.status_code)
                return []

            data = response.json()
            if not data.get("success", False):
                return []

            results = data.get("result", {}).get("results", [])
            normalized: List[NormalizedDatasetMetadata] = []

            for item in results:
                package_id = item.get("id", "")
                title = item.get("title", f"Data.gov Package {package_id}")
                notes = item.get("notes", "")
                license_title = item.get("license_title", "Public Domain / Open Data")

                # Detect resources and formats
                resources = item.get("resources", [])
                formats = list({r.get("format", "").lower() for r in resources if r.get("format")})
                primary_format = formats[0] if formats else "tabular"

                record = NormalizedDatasetMetadata(
                    name=title,
                    dataset_id=f"datagov.{package_id}",
                    source_provider="data_gov",
                    canonical_url=f"https://catalog.data.gov/dataset/{item.get('name', package_id)}",
                    description=notes[:500],
                    domain="governance",
                    task_type="tabular" if any(f in ("csv", "json", "xls", "xlsx") for f in formats) else "general",
                    geography=["US / Public Data"],
                    format=primary_format,
                    license=license_title,
                    license_verified=True,
                    publication_date=item.get("metadata_created"),
                    last_updated=item.get("metadata_modified"),
                    search_query=query.keywords,
                    verification_status="verified_api",
                )
                normalized.append(record)

            return normalized

        except requests.RequestException as e:
            logger.warning("Network connection to Data.gov API failed: %s", e)
            return []
