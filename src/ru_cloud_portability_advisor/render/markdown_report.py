from __future__ import annotations


def render_markdown(report: dict) -> str:
    lines = [
        "# Отчет по миграции",
        "",
        f"- Всего ресурсов: {report['summary']['total_resources']}",
        f"- Прямое соответствие: {report['summary']['direct_mappings']}",
        f"- Требуется рефакторинг: {report['summary']['needs_refactor']}",
        f"- Нет аналога: {report['summary']['no_analogs']}",
        "",
        "## Ресурсы",
    ]
    for mapping in report.get("mappings", []):
        lines.append(f"- **{mapping['resource']['name']}** ({mapping['resource']['kind']}): {mapping['status']}")
        for target in mapping.get("targets", []):
            lines.append(f"  - ➡️ {target['provider']} / {target['service']} (status={target.get('status')})")
    if report.get("findings"):
        lines.append("\n## Замечания и рекомендации")
        for finding in report["findings"]:
            lines.append(f"- {finding['resource']['name']}")
            if finding["issues"]:
                lines.append(f"  - Issues: {', '.join(finding['issues'])}")
            if finding["recommendations"]:
                lines.append(f"  - Recommendations: {', '.join(finding['recommendations'])}")
    if report.get("cost"):
        lines.append("\n## Стоимость")
        lines.append(f"- Текущая: {report['cost']['current'].get('estimated_monthly')}")
        for provider, breakdown in (report["cost"]["target"]).items():
            lines.append(f"  - {provider}: {breakdown.get('estimated_monthly')}")
    return "\n".join(lines)
