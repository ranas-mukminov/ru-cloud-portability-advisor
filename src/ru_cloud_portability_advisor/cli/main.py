from __future__ import annotations

import typer

from ru_cloud_portability_advisor.cli.commands.analyze_project import analyze_project
from ru_cloud_portability_advisor.cli.commands.generate_report import generate_report
from ru_cloud_portability_advisor.cli.commands.print_mapping_table import print_mapping_table

app = typer.Typer(help="ru-cloud-portability-advisor CLI")


app.command("analyze-project")(analyze_project)
app.command("generate-report")(generate_report)
app.command("print-mapping-table")(print_mapping_table)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
