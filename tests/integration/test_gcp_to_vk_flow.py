from pathlib import Path

from ru_cloud_portability_advisor.advisor.analysis_engine import AnalysisInput, analyze
from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider


def test_gcp_to_vk_flow():
    result = analyze(
        AnalysisInput(
            tf_path=str(Path("examples/terraform/gcp_sample")),
            config_path=str(Path("src/ru_cloud_portability_advisor/config/examples/gcp_to_vk_medium.yaml")),
        )
    )
    assert any(
        target.target_provider == CloudProvider.VK for mapping in result.mappings for target in mapping.target_options
    )
