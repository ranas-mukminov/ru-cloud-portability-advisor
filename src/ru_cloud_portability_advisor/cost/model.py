from __future__ import annotations

from dataclasses import dataclass, field

from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider


@dataclass
class Pricing:
    cost_per_vcpu_hour: float = 0.0
    cost_per_gb_ram_hour: float = 0.0
    cost_per_gb_storage_month: float = 0.0
    cost_per_gb_egress_month: float = 0.0


@dataclass
class CostModel:
    provider: CloudProvider
    region: str | None = None
    pricing: Pricing = field(default_factory=Pricing)


@dataclass
class CostEstimate:
    monthly_cost: float
    breakdown: dict[str, float] = field(default_factory=dict)
