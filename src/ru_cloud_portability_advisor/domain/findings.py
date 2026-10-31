from __future__ import annotations

from dataclasses import dataclass, field

from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider, MigrationStatus
from ru_cloud_portability_advisor.domain.models import BaseResource


@dataclass
class MappingOption:
    target_provider: CloudProvider
    target_service: str
    status: MigrationStatus | None = None
    notes: str | None = None


@dataclass
class MappingResult:
    resource: BaseResource
    status: MigrationStatus
    target_options: list[MappingOption] = field(default_factory=list)
    notes: str | None = None


@dataclass
class ResourceFinding:
    resource: BaseResource
    issues: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


@dataclass
class CostBreakdown:
    estimated_monthly: float
    details: dict[str, float] = field(default_factory=dict)


@dataclass
class CostComparison:
    current: CostBreakdown
    target: dict[CloudProvider, CostBreakdown]


@dataclass
class AnalysisSummary:
    total_resources: int
    direct_mappings: int
    refactors: int
    no_analogs: int


@dataclass
class AnalysisResult:
    resources: list[BaseResource]
    mappings: list[MappingResult]
    findings: list[ResourceFinding]
    cost: CostComparison | None = None
    summary: AnalysisSummary | None = None
