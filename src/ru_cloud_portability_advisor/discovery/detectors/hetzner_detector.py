from __future__ import annotations

from typing import Iterable

from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider
from ru_cloud_portability_advisor.domain.models import BaseResource


def detect(resources: Iterable[BaseResource]) -> bool:
    return any(resource.provider == CloudProvider.HETZNER for resource in resources)

