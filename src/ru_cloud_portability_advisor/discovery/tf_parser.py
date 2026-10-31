from __future__ import annotations

import json
from pathlib import Path

try:
    import hcl2
except ImportError:  # pragma: no cover
    hcl2 = None  # type: ignore[assignment]

from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider, ServiceKind
from ru_cloud_portability_advisor.domain.models import (
    BaseResource,
    ComputeInstance,
    Function,
    KubernetesCluster,
    LoadBalancer,
    ManagedDatabaseInstance,
    Queue,
    StorageBucket,
)


class TerraformParseError(Exception):
    """Raised when Terraform configuration cannot be parsed."""


def _provider_from_type(resource_type: str) -> CloudProvider:
    if resource_type.startswith("aws_"):
        return CloudProvider.AWS
    if resource_type.startswith("google_"):
        return CloudProvider.GCP
    if resource_type.startswith("hcloud_"):
        return CloudProvider.HETZNER
    return CloudProvider.UNKNOWN


def _base_kwargs(resource_type: str, name: str, attributes: dict) -> dict:
    region = attributes.get("region") or attributes.get("location")
    return {
        "name": name,
        "provider": _provider_from_type(resource_type),
        "region": region,
        "raw": {"type": resource_type, "attributes": attributes},
    }


def _storage_bucket(resource_type: str, name: str, attributes: dict) -> StorageBucket:
    return StorageBucket(
        kind=ServiceKind.STORAGE,
        versioning=bool(attributes.get("versioning", False)),
        size_gb=attributes.get("size"),
        **_base_kwargs(resource_type, name, attributes),
    )


def _database_instance(resource_type: str, name: str, attributes: dict) -> ManagedDatabaseInstance:
    return ManagedDatabaseInstance(
        kind=ServiceKind.DATABASE,
        engine=attributes.get("engine"),
        cpu=attributes.get("allocated_storage"),
        memory_gb=attributes.get("instance_class"),
        storage_gb=attributes.get("storage_gb"),
        **_base_kwargs(resource_type, name, attributes),
    )


def _compute_instance(resource_type: str, name: str, attributes: dict) -> ComputeInstance:
    return ComputeInstance(
        kind=ServiceKind.COMPUTE,
        cpu=attributes.get("vcpu") or attributes.get("cores"),
        memory_gb=attributes.get("memory") or attributes.get("memory_gb"),
        disk_gb=attributes.get("disk") or attributes.get("disk_gb"),
        **_base_kwargs(resource_type, name, attributes),
    )


def _k8s_cluster(resource_type: str, name: str, attributes: dict) -> KubernetesCluster:
    return KubernetesCluster(
        kind=ServiceKind.KUBERNETES,
        node_count=attributes.get("node_count"),
        version=attributes.get("version"),
        **_base_kwargs(resource_type, name, attributes),
    )


def _load_balancer(resource_type: str, name: str, attributes: dict) -> LoadBalancer:
    return LoadBalancer(
        kind=ServiceKind.LOAD_BALANCER,
        lb_type=attributes.get("load_balancer_type"),
        protocol=attributes.get("protocol"),
        **_base_kwargs(resource_type, name, attributes),
    )


def _queue(resource_type: str, name: str, attributes: dict) -> Queue:
    return Queue(
        kind=ServiceKind.QUEUE,
        fifo=bool(attributes.get("fifo_queue", False)),
        throughput=attributes.get("receive_wait_time_seconds"),
        **_base_kwargs(resource_type, name, attributes),
    )


def _function(resource_type: str, name: str, attributes: dict) -> Function:
    return Function(
        kind=ServiceKind.FUNCTION,
        runtime=attributes.get("runtime"),
        memory_mb=attributes.get("memory_size"),
        timeout_sec=attributes.get("timeout"),
        **_base_kwargs(resource_type, name, attributes),
    )


def _classify_resource(resource_type: str, name: str, attributes: dict) -> BaseResource:
    if resource_type in {"aws_s3_bucket", "google_storage_bucket"}:
        return _storage_bucket(resource_type, name, attributes)
    if resource_type in {"aws_db_instance", "google_sql_database_instance"}:
        return _database_instance(resource_type, name, attributes)
    if resource_type in {"aws_instance", "google_compute_instance", "hcloud_server"}:
        return _compute_instance(resource_type, name, attributes)
    if resource_type in {"aws_eks_cluster", "google_container_cluster"}:
        return _k8s_cluster(resource_type, name, attributes)
    if resource_type in {"aws_lb", "aws_alb", "aws_elb", "google_compute_forwarding_rule", "hcloud_load_balancer"}:
        return _load_balancer(resource_type, name, attributes)
    if resource_type in {"aws_sqs_queue", "google_pubsub_subscription"}:
        return _queue(resource_type, name, attributes)
    if resource_type in {"aws_lambda_function", "google_cloudfunctions_function"}:
        return _function(resource_type, name, attributes)
    return BaseResource(
        name=name,
        provider=_provider_from_type(resource_type),
        kind=ServiceKind.NETWORK,
        region=attributes.get("region"),
        raw={"type": resource_type, "attributes": attributes},
    )


def _parse_resource_block(resource_type: str, block: dict) -> list[BaseResource]:
    resources: list[BaseResource] = []
    for name, attributes in block.items():
        resources.append(_classify_resource(resource_type, name, attributes))
    return resources


def _parse_hcl_doc(doc: dict) -> list[BaseResource]:
    resources: list[BaseResource] = []
    for resource in doc.get("resource", []):
        if not isinstance(resource, dict):
            continue
        for resource_type, block in resource.items():
            if isinstance(block, list):
                for item in block:
                    resources.extend(_parse_resource_block(resource_type, item))
            elif isinstance(block, dict):
                resources.extend(_parse_resource_block(resource_type, block))
    return resources


def _parse_tf_file(path: Path) -> list[BaseResource]:
    if path.suffix == ".json":
        with path.open("r", encoding="utf-8") as fh:
            doc = json.load(fh)
    else:
        if hcl2 is None:
            raise TerraformParseError("python-hcl2 is not installed; install dependency or use .tf.json.")
        with path.open("r", encoding="utf-8") as fh:
            doc = hcl2.load(fh)
    return _parse_hcl_doc(doc)


def parse_terraform_directory(path: str | Path) -> list[BaseResource]:
    root = Path(path)
    if not root.exists():
        raise TerraformParseError(f"Terraform path does not exist: {path}")

    resources: list[BaseResource] = []
    for file_path in root.rglob("*"):
        if file_path.suffix not in {".tf", ".json"}:
            continue
        try:
            resources.extend(_parse_tf_file(file_path))
        except Exception as exc:  # pragma: no cover - passthrough logging responsibility
            raise TerraformParseError(f"Failed to parse {file_path}: {exc}") from exc
    return resources
