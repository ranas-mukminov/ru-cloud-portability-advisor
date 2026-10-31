from __future__ import annotations

from dataclasses import dataclass

from ru_cloud_portability_advisor.advisor import recommendations, report_builder
from ru_cloud_portability_advisor.config.loader import AdvisorConfig, load_config
from ru_cloud_portability_advisor.cost.estimator import estimate_costs
from ru_cloud_portability_advisor.discovery.k8s_parser import parse_k8s_directory
from ru_cloud_portability_advisor.discovery.tf_parser import parse_terraform_directory
from ru_cloud_portability_advisor.domain.cloud_enums import CloudProvider
from ru_cloud_portability_advisor.domain.findings import AnalysisResult, AnalysisSummary, MappingResult, ResourceFinding
from ru_cloud_portability_advisor.domain.models import BaseResource
from ru_cloud_portability_advisor.mapping.mapper import map_resources


@dataclass
class AnalysisInput:
    tf_path: str | None = None
    k8s_path: str | None = None
    config_path: str | None = None


def _load_resources(tf_path: str | None, k8s_path: str | None) -> list[BaseResource]:
    resources: list[BaseResource] = []
    if tf_path:
        resources.extend(parse_terraform_directory(tf_path))
    if k8s_path:
        resources.extend(parse_k8s_directory(k8s_path))
    return resources


def _calculate_summary(mappings: list[MappingResult]) -> AnalysisSummary:
    direct = sum(1 for m in mappings if m.status.value == "direct")
    refactor = sum(1 for m in mappings if m.status.value == "needs_refactor")
    no_analog = sum(1 for m in mappings if m.status.value == "no_analog")
    return AnalysisSummary(
        total_resources=len(mappings),
        direct_mappings=direct,
        refactors=refactor,
        no_analogs=no_analog,
    )


def analyze(input_params: AnalysisInput) -> AnalysisResult:
    config: AdvisorConfig | None = load_config(input_params.config_path) if input_params.config_path else None
    target_providers = config.target_providers if config else []
    source_provider = config.source_provider if config else CloudProvider.UNKNOWN
    resources = _load_resources(input_params.tf_path, input_params.k8s_path)
    mappings = map_resources(resources, target_providers=target_providers)
    summary = _calculate_summary(mappings)
    findings: list[ResourceFinding] = recommendations.generate_findings(mappings)

    cost_result = None
    if config:
        cost_result = estimate_costs(
            resources=resources,
            source_provider=source_provider,
            target_providers=target_providers,
            pricing_file=str(config.pricing_file) if config.pricing_file else None,
        )
    return AnalysisResult(
        resources=resources,
        mappings=mappings,
        findings=findings,
        cost=cost_result,
        summary=summary,
    )


def build_report(result: AnalysisResult) -> dict:
    return report_builder.build_report(result)
