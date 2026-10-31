from __future__ import annotations

from dataclasses import dataclass, field

from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider, ServiceKind


@dataclass
class BaseResource:
    name: str
    provider: CloudProvider
    kind: ServiceKind
    region: str | None = None
    raw: dict | None = None


@dataclass
class StorageBucket(BaseResource):
    versioning: bool = False
    size_gb: float | None = None


@dataclass
class ManagedDatabaseInstance(BaseResource):
    engine: str | None = None
    cpu: float | None = None
    memory_gb: float | None = None
    storage_gb: float | None = None


@dataclass
class ComputeInstance(BaseResource):
    cpu: float | None = None
    memory_gb: float | None = None
    disk_gb: float | None = None


@dataclass
class KubernetesCluster(BaseResource):
    node_count: int | None = None
    version: str | None = None


@dataclass
class LoadBalancer(BaseResource):
    lb_type: str | None = None
    protocol: str | None = None


@dataclass
class Queue(BaseResource):
    fifo: bool = False
    throughput: int | None = None


@dataclass
class Function(BaseResource):
    runtime: str | None = None
    memory_mb: int | None = None
    timeout_sec: int | None = None


@dataclass
class K8sObject(BaseResource):
    api_version: str = ""
    namespace: str | None = None
    annotations: dict[str, str] = field(default_factory=dict)
    spec: dict | None = None


def ensure_list(value: BaseResource | list[BaseResource] | None) -> list[BaseResource]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]
