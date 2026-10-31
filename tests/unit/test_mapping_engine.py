from ru_cloud_portability_advisor.discovery.tf_parser import parse_terraform_directory
from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider, MigrationStatus
from ru_cloud_portability_advisor.mapping.mapper import map_resources


def test_mapping_engine_direct_and_refactor():
    resources = parse_terraform_directory("examples/terraform/aws_sample")
    results = map_resources(resources, target_providers=[CloudProvider.YANDEX, CloudProvider.VK])
    assert results
    assert any(res.status == MigrationStatus.DIRECT for res in results)
