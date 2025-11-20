from __future__ import annotations

from typing import List

from ru_cloud_portability_advisor.domain.cloud_enums import MigrationStatus, ServiceKind
from ru_cloud_portability_advisor.domain.findings import MappingResult, ResourceFinding


def _generic_recommendations(mapping: MappingResult) -> List[str]:
    if mapping.resource.kind == ServiceKind.KUBERNETES:
        return ["Проверьте версии k8s и совместимость сетевых плагинов на целевой платформе."]
    if mapping.resource.kind == ServiceKind.LOAD_BALANCER:
        return ["Сопоставьте аннотации ingress/service с контроллером целевого облака."]
    if mapping.resource.kind == ServiceKind.DATABASE:
        return ["Согласуйте тип БД, версию и параметры резервного копирования в managed-сервисе."]
    if mapping.resource.kind == ServiceKind.STORAGE:
        return ["Проверьте политику versioning и ACL при переносе бакетов."]
    if mapping.resource.kind == ServiceKind.FUNCTION:
        return ["При отсутствии аналога рассмотрите перенос логики в k8s CronJob/Job."]
    return []


def generate_findings(mappings: List[MappingResult]) -> List[ResourceFinding]:
    findings: List[ResourceFinding] = []
    for mapping in mappings:
        issues: List[str] = []
        recommendations: List[str] = _generic_recommendations(mapping)
        if mapping.status == MigrationStatus.NO_ANALOG:
            issues.append("Нет прямого аналога, требуется архитектурный рефакторинг.")
        elif mapping.status == MigrationStatus.NEEDS_REFACTOR:
            issues.append("Потребуются изменения конфигурации перед миграцией.")
        findings.append(ResourceFinding(resource=mapping.resource, issues=issues, recommendations=recommendations))
    return findings

