from pathlib import Path

import pytest

from ru_cloud_portability_advisor.discovery.tf_parser import TerraformParseError, parse_terraform_directory
from ru_cloud_portability_advisor.domain.cloud_enums import ServiceKind
from ru_cloud_portability_advisor.domain.models import StorageBucket


def test_parse_tf_directory_samples():
    resources = parse_terraform_directory(Path("examples/terraform/aws_sample"))
    assert resources, "expected resources to be discovered"
    bucket = next((r for r in resources if isinstance(r, StorageBucket)), None)
    assert bucket is not None
    assert bucket.kind == ServiceKind.STORAGE


def test_parse_tf_directory_not_found():
    with pytest.raises(TerraformParseError):
        parse_terraform_directory(Path("non-existent-path"))

