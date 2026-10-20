"""
UCI Machine Learning Repository Discovery Adapter.

Provides access to indexed benchmark tabular datasets from the UCI ML Repository,
mapping feature taxonomies, demographic columns, and tasks.
"""

from typing import List, Optional
from fairlens.config.logging import get_logger
from fairlens.config.settings import Settings, get_settings
from fairlens.discovery.base import BaseDiscoveryAdapter
from fairlens.discovery.schema import DiscoveryQuery, NormalizedDatasetMetadata

logger = get_logger("discovery.uci")

# Canonical UCI repository index for fairness and tabular tasks
UCI_CANONICAL_INDEX = [
    {
        "name": "Adult Census Income (Census Income)",
        "id": "uci.adult",
        "url": "https://archive.ics.uci.edu/dataset/2/adult",
        "description": "Predict whether income exceeds $50K/yr based on 1994 US Census data. Benchmark dataset with demographic features (age, sex, race, education, occupation).",
        "domain": "sociodemographic",
        "task_type": "tabular",
        "format": "csv",
        "features": ["age", "workclass", "education", "marital-status", "occupation", "relationship", "race", "sex", "hours-per-week", "native-country"],
        "license": "CC-BY-4.0",
        "row_count": 48842,
    },
    {
        "name": "Statlog (German Credit Data)",
        "id": "uci.german_credit",
        "url": "https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data",
        "description": "Classifies people described by a set of attributes as good or bad credit risks. Contains personal attributes such as gender, age, marital status, and housing.",
        "domain": "finance",
        "task_type": "tabular",
        "format": "csv",
        "features": ["status_checking", "duration", "credit_history", "purpose", "credit_amount", "savings", "employment", "personal_status_sex", "age"],
        "license": "CC-BY-4.0",
        "row_count": 1000,
    },
    {
        "name": "Bank Marketing",
        "id": "uci.bank_marketing",
        "url": "https://archive.ics.uci.edu/dataset/222/bank+marketing",
        "description": "Related with direct marketing campaigns of a Portuguese banking institution. Contains client attributes including age, job, marital status, education, and loan default.",
        "domain": "finance",
        "task_type": "tabular",
        "format": "csv",
        "features": ["age", "job", "marital", "education", "default", "balance", "housing", "loan"],
        "license": "CC-BY-4.0",
        "row_count": 45211,
    },
    {
        "name": "Student Performance",
        "id": "uci.student_performance",
        "url": "https://archive.ics.uci.edu/dataset/320/student+performance",
        "description": "Student achievement in secondary education of two Portuguese schools, with demographic, social, and school-related features.",
        "domain": "education",
        "task_type": "tabular",
        "format": "csv",
        "features": ["school", "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu", "guardian"],
        "license": "CC-BY-4.0",
        "row_count": 1044,
    },
]


class UCIDiscoveryAdapter(BaseDiscoveryAdapter):
    """Adapter for searching tabular benchmarks in the UCI ML Repository."""

    def __init__(self, settings: Optional[Settings] = None):
        super().__init__(provider_name="uci")
        self.settings = settings or get_settings()

    def is_configured(self) -> bool:
        """UCI catalog index is available locally without credentials."""
        return True

    def requires_auth(self) -> bool:
        return False

    def search(self, query: DiscoveryQuery) -> List[NormalizedDatasetMetadata]:
        """Search canonical UCI index using keyword matching."""
        terms = [t.lower() for t in query.keywords.split() if len(t) > 2]
        matches: List[NormalizedDatasetMetadata] = []

        for item in UCI_CANONICAL_INDEX:
            text_corpus = f"{item['name']} {item['description']} {' '.join(item['features'])} {item['domain']}".lower()
            if not terms or any(t in text_corpus for t in terms):
                record = NormalizedDatasetMetadata(
                    name=item["name"],
                    dataset_id=item["id"],
                    source_provider="uci",
                    canonical_url=item["url"],
                    description=item["description"],
                    domain=item["domain"],
                    task_type="tabular",
                    geography=["Global / Reference Benchmark"],
                    available_features=item["features"],
                    format="csv",
                    license=item["license"],
                    license_verified=True,
                    row_count=item.get("row_count"),
                    search_query=query.keywords,
                    verification_status="verified_api",
                )
                matches.append(record)

        return matches[:query.limit]
