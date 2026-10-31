from __future__ import annotations

import json
from pathlib import Path

import yaml

from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider, ServiceKind
from ru_cloud_portability_advisor.domain.models import BaseResource, K8sObject


class K8sParseError(Exception):
    """Raised when Kubernetes manifests cannot be parsed."""


def _infer_provider(annotations: dict[str, str], spec: dict | None) -> CloudProvider:
    text = " ".join(annotations.values()).lower()
    if "alb" in text or "aws" in text:
        return CloudProvider.AWS
    if "gce" in text or "gke" in text or "googleapis" in text:
        return CloudProvider.GCP
    if "hcloud" in text or "hetzner" in text:
        return CloudProvider.HETZNER
    if "yandex" in text or "yc" in text:
        return CloudProvider.YANDEX
    if "vkcloud" in text or "vk cloud" in text:
        return CloudProvider.VK
    if "selectel" in text:
        return CloudProvider.SELECTEL
    storage_class_name = None
    if isinstance(spec, dict):
        storage_class_name = spec.get("storageClassName") or spec.get("storage_class_name")
    if storage_class_name:
        lowered = str(storage_class_name).lower()
        if lowered.startswith("yc-"):
            return CloudProvider.YANDEX
        if lowered.startswith("hcloud"):
            return CloudProvider.HETZNER
    return CloudProvider.UNKNOWN


def _classify_kind(kind: str, spec: dict | None) -> ServiceKind:
    if kind in {"Ingress", "IngressRoute"}:
        return ServiceKind.LOAD_BALANCER
    if kind == "Service":
        service_type = (spec or {}).get("type")
        if service_type in {"LoadBalancer", "NodePort"}:
            return ServiceKind.LOAD_BALANCER
    if kind in {"PersistentVolumeClaim", "StorageClass", "PersistentVolume"}:
        return ServiceKind.STORAGE
    if kind in {"Deployment", "StatefulSet", "DaemonSet"}:
        return ServiceKind.K8S_OBJECT
    return ServiceKind.K8S_OBJECT


def _parse_document(doc: dict, source: Path) -> BaseResource | None:
    if not isinstance(doc, dict):
        return None
    kind = doc.get("kind")
    api_version = doc.get("apiVersion", "")
    metadata = doc.get("metadata") or {}
    name = metadata.get("name") or f"unnamed-{source.name}"
    namespace = metadata.get("namespace")
    annotations = metadata.get("annotations") or {}
    spec = doc.get("spec")
    provider = _infer_provider(annotations, spec)
    service_kind = _classify_kind(kind if isinstance(kind, str) else "", spec)
    return K8sObject(
        name=name,
        provider=provider,
        kind=service_kind,
        api_version=api_version,
        namespace=namespace,
        annotations=annotations,
        spec=spec,
        raw={"kind": kind, "source": str(source)},
    )


def parse_k8s_directory(path: str | Path) -> list[BaseResource]:
    root = Path(path)
    if not root.exists():
        raise K8sParseError(f"Kubernetes path does not exist: {path}")

    manifests: list[BaseResource] = []
    for file_path in root.rglob("*"):
        if file_path.suffix.lower() not in {".yaml", ".yml", ".json"}:
            continue
        try:
            content = file_path.read_text(encoding="utf-8")
            if file_path.suffix.lower() == ".json":
                docs = [json.loads(content)]
            else:
                docs = list(yaml.safe_load_all(content))
            for doc in docs:
                parsed = _parse_document(doc, file_path)
                if parsed:
                    manifests.append(parsed)
        except Exception as exc:  # pragma: no cover - passthrough logging responsibility
            raise K8sParseError(f"Failed to parse {file_path}: {exc}") from exc
    return manifests
