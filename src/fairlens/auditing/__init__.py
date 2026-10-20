"""FairLens Dataset Representation-Gap Auditing Module."""

from fairlens.auditing.config import AuditConfig, AuditDimension
from fairlens.auditing.engine import AuditReport, DimensionAuditResult, RepresentationAuditEngine
from fairlens.auditing.loader import TabularDataLoader
from fairlens.auditing.metrics import RepresentationMetrics
from fairlens.auditing.scoring import AuditWarning, ExplainableScoringFramework, Scorecard

__all__ = [
    "AuditConfig",
    "AuditDimension",
    "AuditReport",
    "DimensionAuditResult",
    "RepresentationAuditEngine",
    "TabularDataLoader",
    "RepresentationMetrics",
    "AuditWarning",
    "ExplainableScoringFramework",
    "Scorecard",
]
