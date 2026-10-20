"""
Kaggle Dataset Discovery Adapter.

Supports querying Kaggle API metadata when credentials (KAGGLE_USERNAME and KAGGLE_KEY)
are configured, with safe error containment and clear credential setup guidance.
"""

from typing import List, Optional
from fairlens.config.logging import get_logger
from fairlens.config.settings import Settings, get_settings
from fairlens.discovery.base import BaseDiscoveryAdapter
from fairlens.discovery.schema import DiscoveryQuery, NormalizedDatasetMetadata

logger = get_logger("discovery.kaggle")


class KaggleDiscoveryAdapter(BaseDiscoveryAdapter):
    """Adapter for searching datasets on Kaggle."""

    def __init__(self, settings: Optional[Settings] = None):
        super().__init__(provider_name="kaggle")
        self.settings = settings or get_settings()

    def is_configured(self) -> bool:
        """Check if Kaggle username and key are populated."""
        return bool(self.settings.kaggle_username and self.settings.kaggle_key)

    def requires_auth(self) -> bool:
        """Kaggle mandates authenticated API credentials for programmatic dataset search."""
        return True

    def search(self, query: DiscoveryQuery) -> List[NormalizedDatasetMetadata]:
        """Search Kaggle datasets if credentials exist; otherwise log clear instructions."""
        if not self.is_configured():
            logger.info(
                "Kaggle adapter is not configured. To enable live Kaggle search, "
                "set KAGGLE_USERNAME and KAGGLE_KEY in .env or place kaggle.json in ~/.kaggle."
            )
            return []

        if self.settings.offline_mode:
            logger.debug("Kaggle adapter running in offline mode.")
            return []

        # When credentials are provided, invoke official kaggle API or return structured results
        try:
            import kaggle
            api = kaggle.KaggleApi()
            api.authenticate()
            datasets = api.dataset_list(search=query.keywords, max_size=query.limit)
            normalized: List[NormalizedDatasetMetadata] = []
            for ds in datasets:
                normalized.append(
                    NormalizedDatasetMetadata(
                        name=ds.title or ds.ref,
                        dataset_id=f"kaggle.{ds.ref}",
                        source_provider="kaggle",
                        canonical_url=f"https://www.kaggle.com/datasets/{ds.ref}",
                        description=ds.subtitle or f"Kaggle dataset by {ds.creatorName}",
                        domain="general",
                        task_type="tabular",
                        format="tabular",
                        license=ds.licenseName or "unknown",
                        license_verified=bool(ds.licenseName),
                        size_bytes=ds.totalBytes,
                        search_query=query.keywords,
                        verification_status="verified_api",
                    )
                )
            return normalized
        except ImportError:
            logger.warning("Kaggle Python library is not installed.")
            return []
        except Exception as e:
            logger.error("Kaggle API call failed: %s", e)
            return []
