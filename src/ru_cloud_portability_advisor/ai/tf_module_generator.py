from __future__ import annotations

from ru_cloud_portability_advisor.ai.base import AIProvider, NoopAIProvider
from ru_cloud_portability_advisor.domain.findings import MappingResult


def generate_tf_stub(mapping: MappingResult, provider: AIProvider | None = None) -> str:
    ai = provider or NoopAIProvider()
    targets = ", ".join({t.target_provider.value for t in mapping.target_options}) or "целевой облако"
    prompt = (
        f"Сгенерируй черновик Terraform-ресурса для {targets} на основе {mapping.resource.name}. "
        "Оставь TODO для полей, требующих ручного ввода. Используй упрощенный пример."
    )
    return ai.complete(prompt)

