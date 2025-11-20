from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider, ServiceKind


@dataclass
class BaseResource:
    name: str
    provider: CloudProvider
    kind: ServiceKind
    region: Optional[str] = None
    raw: Dict | None = None


@dataclass
class StorageBucket(BaseResource):
    versioning: bool = False
    size_gb: Optional[float] = None


@dataclass
class ManagedDatabaseInstance(BaseResource):
    engine: Optional[str] = None
    cpu: Optional[float] = None
    memory_gb: Optional[float] = None
    storage_gb: Optional[float] = None


@dataclass
class ComputeInstance(BaseResource):
    cpu: Optional[float] = None
    memory_gb: Optional[float] = None
    disk_gb: Optional[float] = None


@dataclass
class KubernetesCluster(BaseResource):
    node_count: Optional[int] = None
    version: Optional[str] = None


@dataclass
class LoadBalancer(BaseResource):
    lb_type: Optional[str] = None
    protocol: Optional[str] = None


@dataclass
class Queue(BaseResource):
    fifo: bool = False
    throughput: Optional[int] = None


@dataclass
class Function(BaseResource):
    runtime: Optional[str] = None
    memory_mb: Optional[int] = None
    timeout_sec: Optional[int] = None


@dataclass
class K8sObject(BaseResource):
    api_version: str = ""
    namespace: Optional[str] = None
    annotations: Dict[str, str] = field(default_factory=dict)
    spec: Dict | None = None


def ensure_list(value: BaseResource | List[BaseResource] | None) -> List[BaseResource]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]

