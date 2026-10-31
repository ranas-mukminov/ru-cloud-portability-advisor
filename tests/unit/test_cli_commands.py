from typer.testing import CliRunner

from ru_cloud_portability_advisor.cli.main import app

runner = CliRunner()


def test_print_mapping_table_command():
    result = runner.invoke(app, ["print-mapping-table"])
    assert result.exit_code == 0
    assert "source_provider" in result.stdout
