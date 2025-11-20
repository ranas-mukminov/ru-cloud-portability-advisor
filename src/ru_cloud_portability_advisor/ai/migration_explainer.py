from __future__ import annotations

from ru_cloud_portability_advisor.ai.base import AIProvider, NoopAIProvider
from ru_cloud_portability_advisor.domain.findings import MappingResult


def explain(mapping: MappingResult, provider: AIProvider | None = None) -> str:
    ai = provider or NoopAIProvider()
    prompt = (
        "Сформулируй краткое пояснение того, что изменится при миграции ресурса "
        f"{mapping.resource.name} с провайдера {mapping.resource.provider.value}. "
        f"Текущий статус: {mapping.status.value}. "
        "Ответ должен быть лаконичным и пригодным для отчета."
    )
    return ai.complete(prompt)

