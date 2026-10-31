from __future__ import annotations

import json
from pathlib import Path

import yaml

from ru_cloud_portability_advisor.cost.model import CostModel, Pricing
from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider


class PricingLoadError(Exception):
    """Raised when pricing configuration cannot be loaded."""


def _parse_file(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        if path.suffix.lower() in {".yaml", ".yml"}:
            return yaml.safe_load(fh) or {}
        return json.load(fh)


def load_pricing(path: str | Path) -> dict[CloudProvider, CostModel]:
    pricing_path = Path(path)
    if not pricing_path.exists():
        raise PricingLoadError(f"Pricing file not found: {path}")

    data = _parse_file(pricing_path)
    models: dict[CloudProvider, CostModel] = {}
    for provider_str, values in data.items():
        provider = CloudProvider(provider_str)
        pricing = Pricing(
            cost_per_vcpu_hour=float(values.get("cost_per_vcpu_hour", 0.0)),
            cost_per_gb_ram_hour=float(values.get("cost_per_gb_ram_hour", 0.0)),
            cost_per_gb_storage_month=float(values.get("cost_per_gb_storage_month", 0.0)),
            cost_per_gb_egress_month=float(values.get("cost_per_gb_egress_month", 0.0)),
        )
        models[provider] = CostModel(provider=provider, region=values.get("region"), pricing=pricing)
    return models


def empty_pricing(providers: list[CloudProvider]) -> dict[CloudProvider, CostModel]:
    return {provider: CostModel(provider=provider) for provider in providers}
