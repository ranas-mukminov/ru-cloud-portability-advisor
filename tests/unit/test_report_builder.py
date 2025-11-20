from ru_cloud_portability_advisor.advisor.analysis_engine import AnalysisInput, analyze
from ru_cloud_portability_advisor.advisor.report_builder import build_report


def test_report_builder_contains_sections():
    result = analyze(
        AnalysisInput(
            tf_path="examples/terraform/aws_sample",
            config_path="src/ru_cloud_portability_advisor/config/examples/aws_to_yc_simple.yaml",
        )
    )
    report = build_report(result)
    assert "summary" in report
    assert "mappings" in report
    assert "findings" in report

