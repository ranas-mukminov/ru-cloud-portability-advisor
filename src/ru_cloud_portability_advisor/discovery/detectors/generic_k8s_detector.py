from __future__ import annotations

from typing import Iterable

from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider, ServiceKind
from ru_cloud_portability_advisor.domain.models import BaseResource


def detect(resources: Iterable[BaseResource]) -> CloudProvider:
    """
    Detect provider hints from Kubernetes manifests based on annotations or storage classes.
    Returns CloudProvider.UNKNOWN when no hints were found.
    """
    provider_counts: dict[CloudProvider, int] = {}
    for resource in resources:
        if resource.kind != ServiceKind.K8S_OBJECT and resource.kind != ServiceKind.LOAD_BALANCER:
            continue
        provider = resource.provider
        provider_counts[provider] = provider_counts.get(provider, 0) + 1
    if not provider_counts:
        return CloudProvider.UNKNOWN
    return max(provider_counts, key=provider_counts.get)

