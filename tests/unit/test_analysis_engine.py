from pathlib import Path

from ru_cloud_portability_advisor.advisor.analysis_engine import AnalysisInput, analyze
from ru_cloud_portability_advisor.domain.findings import AnalysisResult


def test_full_analysis_pipeline():
    result = analyze(
        AnalysisInput(
            tf_path=str(Path("examples/terraform/aws_sample")),
            k8s_path=str(Path("examples/k8s/ingress_aws_lb")),
            config_path=str(Path("src/ru_cloud_portability_advisor/config/examples/aws_to_yc_simple.yaml")),
        )
    )
    assert isinstance(result, AnalysisResult)
    assert result.mappings
    assert result.summary is not None
