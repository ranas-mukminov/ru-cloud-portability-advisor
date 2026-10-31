from __future__ import annotations

import typer
from rich.console import Console
from tabulate import tabulate

from ru_cloud_portability_advisor.mapping.catalog import load_catalog

console = Console()


def print_mapping_table(provider: str | None = typer.Option(None, help="Filter by source provider")) -> None:
    rules = load_catalog()
    rows = []
    for rule in rules:
        if provider and rule.source_provider.value != provider:
            continue
        target_services = ", ".join(f"{t.target_provider.value}:{t.target_service}" for t in rule.targets)
        rows.append([rule.source_provider.value, rule.source_type, rule.kind.value, target_services])
    console.print(tabulate(rows, headers=["source_provider", "source_type", "kind", "targets"]))
