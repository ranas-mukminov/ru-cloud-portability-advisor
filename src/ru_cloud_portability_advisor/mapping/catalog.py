from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml

from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider, MigrationStatus, ServiceKind
from ru_cloud_portability_advisor.domain.findings import MappingOption


@dataclass
class MappingRule:
    source_type: str
    source_provider: CloudProvider
    kind: ServiceKind
    targets: List[MappingOption]
    notes: str | None = None


def _load_rule_file(path: Path) -> List[MappingRule]:
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or []

    rules: List[MappingRule] = []
    for rule in data:
        targets = [
            MappingOption(
                target_provider=CloudProvider(target["provider"]),
                target_service=target["service"],
                status=MigrationStatus(target.get("status", MigrationStatus.DIRECT.value)),
                notes=target.get("notes"),
            )
            for target in rule.get("targets", [])
        ]
        rules.append(
            MappingRule(
                source_type=rule["source_type"],
                source_provider=CloudProvider(rule["source_provider"]),
                kind=ServiceKind(rule["kind"]),
                targets=targets,
                notes=rule.get("notes"),
            )
        )
    return rules


def load_catalog(directory: str | Path | None = None) -> List[MappingRule]:
    base_dir = Path(directory) if directory else Path(__file__).parent / "rules"
    rules: List[MappingRule] = []
    for path in sorted(base_dir.glob("*.yaml")):
        rules.extend(_load_rule_file(path))
    return rules
