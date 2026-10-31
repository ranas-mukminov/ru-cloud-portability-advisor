from pathlib import Path

import pytest

from ru_cloud_portability_advisor.discovery.k8s_parser import K8sParseError, parse_k8s_directory
from ru_cloud_portability_advisor.domain.cloud_enums import ServiceKind


def test_parse_k8s_directory_samples():
    resources = parse_k8s_directory(Path("examples/k8s/ingress_aws_lb"))
    assert resources
    assert any(r.kind == ServiceKind.LOAD_BALANCER for r in resources)


def test_parse_k8s_directory_not_found():
    with pytest.raises(K8sParseError):
        parse_k8s_directory(Path("non-existent-k8s"))
