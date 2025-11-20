from pathlib import Path

from ru_cloud_portability_advisor.advisor.analysis_engine import AnalysisInput, analyze
from ru_cloud_portability_advisor.domain.cloud_enums import MigrationStatus


def test_aws_to_yandex_flow():
    result = analyze(
        AnalysisInput(
            tf_path=str(Path("examples/terraform/aws_sample")),
            config_path=str(Path("src/ru_cloud_portability_advisor/config/examples/aws_to_yc_simple.yaml")),
        )
    )
    assert any(m.status == MigrationStatus.DIRECT for m in result.mappings)

