from ru_cloud_portability_advisor.cost.estimator import estimate_costs
from ru_cloud_portability_advisor.discovery.tf_parser import parse_terraform_directory
from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider


def test_cost_estimation_with_zero_pricing():
    resources = parse_terraform_directory("examples/terraform/aws_sample")
    costs = estimate_costs(resources, CloudProvider.AWS, [CloudProvider.YANDEX], pricing_file=None)
    assert costs.current.estimated_monthly == 0
    assert CloudProvider.YANDEX in costs.target

