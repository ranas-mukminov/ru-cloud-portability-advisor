from __future__ import annotations

from collections.abc import Iterable, Sequence

from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider, MigrationStatus
from ru_cloud_portability_advisor.domain.findings import MappingOption, MappingResult
from ru_cloud_portability_advisor.domain.models import BaseResource
from ru_cloud_portability_advisor.mapping.catalog import MappingRule, load_catalog


def _match_rule(resource: BaseResource, rules: Iterable[MappingRule]) -> MappingRule | None:
    resource_type = ""
    if isinstance(resource.raw, dict):
        resource_type = resource.raw.get("type", "")
    for rule in rules:
        if rule.source_type == resource_type:
            return rule
        if resource.kind == rule.kind and resource.provider == rule.source_provider:
            return rule
    return None


def _overall_status(targets: list[MappingOption]) -> MigrationStatus:
    statuses = {t.status or MigrationStatus.DIRECT for t in targets}
    if MigrationStatus.DIRECT in statuses:
        return MigrationStatus.DIRECT
    if MigrationStatus.NEEDS_REFACTOR in statuses:
        return MigrationStatus.NEEDS_REFACTOR
    return MigrationStatus.NO_ANALOG


def map_resources(
    resources: list[BaseResource],
    target_providers: Sequence[CloudProvider] | None = None,
    rules: Iterable[MappingRule] | None = None,
) -> list[MappingResult]:
    mapping_rules = list(rules) if rules is not None else load_catalog()
    results: list[MappingResult] = []
    for resource in resources:
        rule = _match_rule(resource, mapping_rules)
        if rule is None:
            results.append(
                MappingResult(
                    resource=resource,
                    status=MigrationStatus.NO_ANALOG,
                    target_options=[],
                    notes="Нет прямого соответствия в каталоге маппингов.",
                )
            )
            continue

        filtered_targets = [t for t in rule.targets if not target_providers or t.target_provider in target_providers]
        status = _overall_status(filtered_targets) if filtered_targets else MigrationStatus.NO_ANALOG
        results.append(
            MappingResult(resource=resource, status=status, target_options=filtered_targets, notes=rule.notes)
        )
    return results
