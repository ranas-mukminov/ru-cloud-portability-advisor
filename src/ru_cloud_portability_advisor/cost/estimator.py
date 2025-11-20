from __future__ import annotations

from typing import Dict, Iterable, List

from ru_cloud_portability_advisor.cost.adapters import empty_pricing, load_pricing
from ru_cloud_portability_advisor.cost.model import CostEstimate, CostModel
from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider
from ru_cloud_portability_advisor.domain.findings import CostBreakdown, CostComparison
from ru_cloud_portability_advisor.domain.models import BaseResource, ComputeInstance, ManagedDatabaseInstance, StorageBucket


HOURS_IN_MONTH = 730


def _resource_profile(resource: BaseResource) -> dict:
    # Crude approximations when explicit sizing is missing.
    if isinstance(resource, ComputeInstance):
        return {
            "vcpu": resource.cpu or 2,
            "ram_gb": resource.memory_gb or 4,
            "storage_gb": resource.disk_gb or 50,
        }
    if isinstance(resource, ManagedDatabaseInstance):
        return {
            "vcpu": resource.cpu or 2,
            "ram_gb": resource.memory_gb or 8,
            "storage_gb": resource.storage_gb or 100,
        }
    if isinstance(resource, StorageBucket):
        return {"storage_gb": resource.size_gb or 50}
    return {"vcpu": 0, "ram_gb": 0, "storage_gb": 0}


def _estimate_for_provider(resources: Iterable[BaseResource], pricing: CostModel) -> CostEstimate:
    total = 0.0
    breakdown: Dict[str, float] = {}
    for resource in resources:
        profile = _resource_profile(resource)
        cpu_cost = profile.get("vcpu", 0) * pricing.pricing.cost_per_vcpu_hour * HOURS_IN_MONTH
        ram_cost = profile.get("ram_gb", 0) * pricing.pricing.cost_per_gb_ram_hour * HOURS_IN_MONTH
        storage_cost = profile.get("storage_gb", 0) * pricing.pricing.cost_per_gb_storage_month
        subtotal = cpu_cost + ram_cost + storage_cost
        breakdown[resource.name] = subtotal
        total += subtotal
    return CostEstimate(monthly_cost=total, breakdown=breakdown)


def estimate_costs(
    resources: List[BaseResource],
    source_provider: CloudProvider,
    target_providers: List[CloudProvider],
    pricing_file: str | None = None,
) -> CostComparison:
    pricing: Dict[CloudProvider, CostModel]
    if pricing_file:
        pricing = load_pricing(pricing_file)
    else:
        pricing = empty_pricing([source_provider, *target_providers])

    current_model = pricing.get(source_provider, CostModel(provider=source_provider))
    target_models = {provider: pricing.get(provider, CostModel(provider=provider)) for provider in target_providers}

    current = _estimate_for_provider(resources, current_model)
    target_breakdowns = {
        provider: _estimate_for_provider(resources, model) for provider, model in target_models.items()
    }
    return CostComparison(current=CostBreakdown(current.monthly_cost, current.breakdown), target=target_breakdowns)

