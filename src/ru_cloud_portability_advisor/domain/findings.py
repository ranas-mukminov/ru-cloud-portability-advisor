from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider, MigrationStatus
from ru_cloud_portability_advisor.domain.models import BaseResource


@dataclass
class MappingOption:
    target_provider: CloudProvider
    target_service: str
    status: MigrationStatus | None = None
    notes: Optional[str] = None


@dataclass
class MappingResult:
    resource: BaseResource
    status: MigrationStatus
    target_options: List[MappingOption] = field(default_factory=list)
    notes: Optional[str] = None


@dataclass
class ResourceFinding:
    resource: BaseResource
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class CostBreakdown:
    estimated_monthly: float
    details: Dict[str, float] = field(default_factory=dict)


@dataclass
class CostComparison:
    current: CostBreakdown
    target: Dict[CloudProvider, CostBreakdown]


@dataclass
class AnalysisSummary:
    total_resources: int
    direct_mappings: int
    refactors: int
    no_analogs: int


@dataclass
class AnalysisResult:
    resources: List[BaseResource]
    mappings: List[MappingResult]
    findings: List[ResourceFinding]
    cost: Optional[CostComparison] = None
    summary: Optional[AnalysisSummary] = None
