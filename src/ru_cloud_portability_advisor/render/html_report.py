from __future__ import annotations

from typing import Dict


def render_html(report: Dict) -> str:
    rows = ""
    for mapping in report.get("mappings", []):
        targets = ", ".join(f"{t['provider']}:{t['service']}" for t in mapping.get("targets", []))
        rows += f"<tr><td>{mapping['resource']['name']}</td><td>{mapping['resource']['kind']}</td><td>{mapping['status']}</td><td>{targets}</td></tr>"
    html = f"""
    <html>
      <head>
        <meta charset="UTF-8"/>
        <title>ru-cloud-portability-advisor report</title>
        <style>
          body {{ font-family: Arial, sans-serif; padding: 20px; }}
          table {{ width: 100%; border-collapse: collapse; }}
          th, td {{ border: 1px solid #ddd; padding: 8px; }}
          th {{ background: #f2f2f2; }}
        </style>
      </head>
      <body>
        <h1>Отчет по миграции</h1>
        <p>Всего ресурсов: {report['summary']['total_resources']}</p>
        <p>Прямое соответствие: {report['summary']['direct_mappings']}</p>
        <p>Требуется рефакторинг: {report['summary']['needs_refactor']}</p>
        <p>Нет аналога: {report['summary']['no_analogs']}</p>
        <table>
          <thead><tr><th>Ресурс</th><th>Тип</th><th>Статус</th><th>Варианты</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </body>
    </html>
    """
    return html

