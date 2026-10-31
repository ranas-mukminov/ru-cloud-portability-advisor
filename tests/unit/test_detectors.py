from ru_cloud_portability_advisor.discovery.detectors import aws_detector, gcp_detector, hetzner_detector
from ru_cloud_portability_advisor.discovery.tf_parser import parse_terraform_directory


def test_aws_detector():
    resources = parse_terraform_directory("examples/terraform/aws_sample")
    assert aws_detector.detect(resources) is True


def test_gcp_detector():
    resources = parse_terraform_directory("examples/terraform/gcp_sample")
    assert gcp_detector.detect(resources) is True


def test_hetzner_detector():
    resources = parse_terraform_directory("examples/terraform/hetzner_sample")
    assert hetzner_detector.detect(resources) is True
