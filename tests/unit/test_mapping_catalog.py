from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider
from ru_cloud_portability_advisor.mapping.catalog import load_catalog


def test_catalog_loads_rules():
    rules = load_catalog()
    assert rules
    providers = {rule.source_provider for rule in rules}
    assert CloudProvider.AWS in providers
