"""
Standardized Metadata Schema and Query Models for FairLens Dataset Discovery.

Enforces uniform representation of dataset metadata across disparate providers
(Hugging Face, Kaggle, UCI, Data.gov, Zenodo) with explicit tracking of missing
fields and potential suitability for demographic representation auditing.
"""

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class NormalizedDatasetMetadata:
    """Standardized schema for discovered datasets across all repositories."""

    # Identity and Source
    name: str
    dataset_id: str
    source_provider: str  # huggingface, kaggle, uci, data_gov, zenodo
    canonical_url: str

    # Context and Content
    description: str = ""
    domain: str = "general"  # legal, finance, healthcare, general, etc.
    task_type: str = "tabular"  # tabular, nlp, classification, etc.
    geography: List[str] = field(default_factory=list)  # e.g. ["India", "Global"]
    languages: List[str] = field(default_factory=list)  # e.g. ["en", "hi"]

    # Demographic and Cultural Documentation (Self-Reported by Source)
    documented_demographics: List[str] = field(default_factory=list)
    available_features: List[str] = field(default_factory=list)
    target_labels: List[str] = field(default_factory=list)

    # Technical Format and Lineage
    format: str = "unknown"  # csv, parquet, json, tabular, etc.
    size_bytes: Optional[int] = None
    row_count: Optional[int] = None
    license: str = "unknown"
    license_verified: bool = False
    publication_date: Optional[str] = None
    last_updated: Optional[str] = None

    # Metadata Quality and Audit Suitability
    verification_status: str = "unverified"  # unverified, verified_api, fixture
    metadata_completeness_score: float = 0.0  # 0.0 to 1.0
    missing_fields: List[str] = field(default_factory=list)
    audit_suitability: str = "unknown"  # high, medium, low, unsupported
    audit_suitability_reasons: List[str] = field(default_factory=list)

    # Provenance
    search_query: str = ""
    retrieved_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def __post_init__(self):
        """Calculate metadata completeness and audit suitability."""
        self._calculate_completeness()
        self._assess_audit_suitability()

    def _calculate_completeness(self) -> None:
        """Evaluate presence of critical documentation fields."""
        critical_fields = {
            "name": bool(self.name),
            "description": bool(self.description and len(self.description) > 20),
            "canonical_url": bool(self.canonical_url),
            "license": bool(self.license and self.license.lower() not in ("unknown", "other", "none")),
            "format": bool(self.format and self.format.lower() != "unknown"),
            "domain": bool(self.domain and self.domain.lower() != "general"),
            "geography": bool(len(self.geography) > 0),
            "features": bool(len(self.available_features) > 0),
        }
        missing = [f for f, present in critical_fields.items() if not present]
        self.missing_fields = missing
        score = (len(critical_fields) - len(missing)) / len(critical_fields)
        self.metadata_completeness_score = round(score, 4)

    def _assess_audit_suitability(self) -> None:
        """Estimate whether dataset is suitable for Phase 4 representation auditing."""
        reasons = []
        is_tabular = self.format.lower() in ("csv", "parquet", "tsv", "excel", "tabular")
        has_geo = any("india" in g.lower() for g in self.geography) or "india" in self.description.lower()

        if is_tabular:
            reasons.append("Tabular structured format directly supported by Phase 4 engine.")
        else:
            reasons.append(f"Format '{self.format}' may require preprocessing before tabular auditing.")

        if has_geo:
            reasons.append("India-centric geography detected in metadata or description.")

        if self.metadata_completeness_score >= 0.75 and is_tabular:
            self.audit_suitability = "high"
        elif is_tabular or self.metadata_completeness_score >= 0.5:
            self.audit_suitability = "medium"
        else:
            self.audit_suitability = "low"

        self.audit_suitability_reasons = reasons

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        return asdict(self)


@dataclass
class DiscoveryQuery:
    """Standardized search parameters passed to discovery providers."""

    keywords: str
    domain: Optional[str] = None
    task_type: Optional[str] = None
    geography: Optional[str] = None
    language: Optional[str] = None
    license: Optional[str] = None
    limit: int = 10
    offset: int = 0
    providers: Optional[List[str]] = None  # None queries all active providers


@dataclass
class DiscoveryResult:
    """Aggregated, deduplicated search results from all queried providers."""

    query: DiscoveryQuery
    datasets: List[NormalizedDatasetMetadata]
    total_found: int
    provider_counts: Dict[str, int]
    provider_errors: Dict[str, str]
    execution_time_seconds: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": asdict(self.query),
            "total_found": self.total_found,
            "provider_counts": self.provider_counts,
            "provider_errors": self.provider_errors,
            "execution_time_seconds": round(self.execution_time_seconds, 4),
            "datasets": [d.to_dict() for d in self.datasets],
        }
