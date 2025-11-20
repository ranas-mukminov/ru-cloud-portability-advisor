from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from ru_cloud_portability_advisor.advisor.analysis_engine import AnalysisInput, analyze, build_report

console = Console()


def analyze_project(
    tf_path: Optional[Path] = typer.Option(None, help="Path to Terraform configuration directory"),
    k8s_path: Optional[Path] = typer.Option(None, help="Path to Kubernetes manifests directory"),
    config: Optional[Path] = typer.Option(None, help="Path to advisor configuration YAML"),
    out: Optional[Path] = typer.Option(None, help="Output path for JSON report"),
) -> None:
    try:
        result = analyze(
            AnalysisInput(
                tf_path=str(tf_path) if tf_path else None,
                k8s_path=str(k8s_path) if k8s_path else None,
                config_path=str(config) if config else None,
            )
        )
    except Exception as exc:
        console.print(f"[red]Ошибка анализа:[/red] {exc}")
        raise typer.Exit(code=1)

    report = build_report(result)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        console.print(f"[green]Отчет сохранен:[/green] {out}")
    else:
        console.print_json(data=report)
