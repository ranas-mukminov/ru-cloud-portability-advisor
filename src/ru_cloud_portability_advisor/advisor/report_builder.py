from __future__ import annotations

from ru_cloud_portability_advisor.domain.findings import AnalysisResult


def _serialize_resource(resource) -> dict:
    return {
        "name": resource.name,
        "provider": resource.provider.value,
        "kind": resource.kind.value,
        "region": resource.region,
        "raw": resource.raw,
    }


def build_report(result: AnalysisResult) -> dict:
    return {
        "summary": {
            "total_resources": result.summary.total_resources if result.summary else len(result.resources),
            "direct_mappings": result.summary.direct_mappings if result.summary else 0,
            "needs_refactor": result.summary.refactors if result.summary else 0,
            "no_analogs": result.summary.no_analogs if result.summary else 0,
        },
        "resources": [_serialize_resource(r) for r in result.resources],
        "mappings": [
            {
                "resource": _serialize_resource(mapping.resource),
                "status": mapping.status.value,
                "targets": [
                    {
                        "provider": option.target_provider.value,
                        "service": option.target_service,
                        "status": option.status.value if option.status else None,
                        "notes": option.notes,
                    }
                    for option in mapping.target_options
                ],
                "notes": mapping.notes,
            }
            for mapping in result.mappings
        ],
        "findings": [
            {
                "resource": _serialize_resource(finding.resource),
                "issues": finding.issues,
                "recommendations": finding.recommendations,
            }
            for finding in result.findings
        ],
        "cost": result.cost.__dict__ if result.cost else None,
    }

