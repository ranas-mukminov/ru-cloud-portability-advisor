from __future__ import annotations

from ru_cloud_portability_advisor.ai.base import AIProvider, NoopAIProvider
from ru_cloud_portability_advisor.domain.models import K8sObject


def suggest_annotations(obj: K8sObject, provider: AIProvider | None = None) -> str:
    ai = provider or NoopAIProvider()
    prompt = (
        f"Предложи аннотации/StorageClass для ресурса kind={(obj.raw or {}).get('kind')} "
        f"с именем {obj.name} при переносе в российские облака. "
        "Верни краткий список с указанием TODO для параметров."
    )
    return ai.complete(prompt)
