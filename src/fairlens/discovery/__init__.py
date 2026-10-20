"""FairLens Multi-Source Dataset Discovery Engine."""

from fairlens.discovery.engine import DatasetDiscoveryEngine
from fairlens.discovery.schema import (
    DiscoveryQuery,
    DiscoveryResult,
    NormalizedDatasetMetadata,
)

__all__ = [
    "DatasetDiscoveryEngine",
    "DiscoveryQuery",
    "DiscoveryResult",
    "NormalizedDatasetMetadata",
]
