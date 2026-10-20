"""
Base Discovery Adapter Abstract Class.

Enforces provider-level error isolation, standard query signatures,
and credential requirement declarations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from fairlens.config.logging import get_logger
from fairlens.discovery.schema import DiscoveryQuery, NormalizedDatasetMetadata

logger = get_logger("discovery.base")


class BaseDiscoveryAdapter(ABC):
    """Abstract interface for external dataset repository adapters."""

    def __init__(self, provider_name: str):
        self.provider_name = provider_name

    @abstractmethod
    def search(self, query: DiscoveryQuery) -> List[NormalizedDatasetMetadata]:
        """Query repository and return normalized dataset metadata objects."""
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        """Check if necessary API credentials or libraries are available."""
        pass

    @abstractmethod
    def requires_auth(self) -> bool:
        """Indicate whether the repository mandates API keys for search."""
        pass

    def safe_search(self, query: DiscoveryQuery) -> List[NormalizedDatasetMetadata]:
        """Execute search with complete exception containment to protect aggregator."""
        try:
            logger.info("Executing discovery query on provider '%s': '%s'", self.provider_name, query.keywords)
            results = self.search(query)
            logger.info("Provider '%s' returned %d candidate datasets", self.provider_name, len(results))
            return results
        except Exception as e:
            logger.error("Provider '%s' search failed: %s", self.provider_name, e)
            return []
