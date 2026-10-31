from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider


@dataclass
class AdvisorConfig:
    source_provider: CloudProvider
    target_providers: list[CloudProvider]
    region_preference: str | None = None
    pricing_file: Path | None = None
    notes: str | None = None
    raw: dict = field(default_factory=dict)


class ConfigError(Exception):
    """Raised when configuration is invalid or cannot be loaded."""


def _normalize_provider(value: str) -> CloudProvider:
    normalized = value.strip().lower()
    mapping = {
        "aws": CloudProvider.AWS,
        "gcp": CloudProvider.GCP,
        "google": CloudProvider.GCP,
        "hetzner": CloudProvider.HETZNER,
        "yandex": CloudProvider.YANDEX,
        "yc": CloudProvider.YANDEX,
        "vk": CloudProvider.VK,
        "cloud_ru": CloudProvider.CLOUD_RU,
        "selectel": CloudProvider.SELECTEL,
    }
    if normalized not in mapping:
        raise ConfigError(f"Unknown provider in config: {value}")
    return mapping[normalized]


def load_config(path: str | Path) -> AdvisorConfig:
    config_path = Path(path).expanduser()
    if not config_path.exists():
        raise ConfigError(f"Config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}

    try:
        source = _normalize_provider(data["source_provider"])
        targets = [_normalize_provider(item) for item in data.get("target_providers", [])]
    except KeyError as exc:
        raise ConfigError(f"Missing required config key: {exc}") from exc

    if not targets:
        raise ConfigError("Config must include at least one target_providers entry")

    pricing_file = data.get("pricing_file")
    if pricing_file:
        pf = Path(pricing_file)
        pricing_path = pf if pf.is_absolute() else (config_path.parent / pf).resolve()
    else:
        pricing_path = None

    return AdvisorConfig(
        source_provider=source,
        target_providers=targets,
        region_preference=data.get("region_preference"),
        pricing_file=pricing_path,
        notes=data.get("notes"),
        raw=data,
    )
