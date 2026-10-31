# ru-cloud-portability-advisor

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](pyproject.toml)

🇬🇧 English | 🇷🇺 [Русская версия](README.ru.md)

**ru-cloud-portability-advisor** is a CLI tool for analyzing infrastructure-as-code (Terraform) and Kubernetes manifests to plan migrations from foreign cloud providers (AWS, GCP, Hetzner) to Russian cloud platforms (Yandex Cloud, VK Cloud, Cloud.ru, Selectel).

It parses your existing configuration, identifies resources, maps them to their local equivalents, and generates a detailed migration report with compatibility notes and potential issues.

## Key Features

- **Multi-Cloud Analysis**: Parses Terraform (`.tf`, `.hcl`) and Kubernetes (`.yaml`) files to discover compute, storage, database, and networking resources.
- **Intelligent Mapping**: Automatically maps source resources (e.g., `aws_instance`, `google_sql_database`) to target equivalents (e.g., `yandex_compute_instance`, `vk_mdb_postgresql`).
- **Migration Advice**: Highlights feature gaps, version incompatibilities, and required configuration changes.
- **Flexible Reporting**: Generates reports in JSON, Markdown, or HTML formats.
- **Extensible Rules**: Mapping logic is defined in YAML files, allowing users to add custom rules or support new providers.
- **Privacy First**: Runs entirely locally; your infrastructure code is never sent to any external server.

## Architecture / Components

The tool consists of the following modules:

- **Discovery Engine**: Scans directories for Terraform and Kubernetes files using `python-hcl2` and `PyYAML`.
- **Advisor Core**: Matches discovered resources against a library of mapping rules (`src/ru_cloud_portability_advisor/mapping/rules`).
- **Reporting Module**: Converts analysis results into human-readable formats (Markdown, HTML) or machine-readable JSON.
- **CLI Interface**: Built with `typer` for easy interaction.

## Requirements

- **OS**: Linux, macOS, or Windows.
- **Python**: 3.10 or higher.
- **Dependencies**:
  - `terraform` (optional, for accurate HCL parsing context).
  - `kubectl` (optional, for validating manifests).
- **Disk Space**: Minimal (<100 MB).

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ranas-mukminov/ru-cloud-portability-advisor.git
   cd ru-cloud-portability-advisor
   ```

2. **Install the package**:
   ```bash
   pip install .
   ```

3. **Run an analysis**:
   ```bash
   # Analyze a Terraform project and output to JSON
   ru-cloud-advisor analyze-project \
     --tf-path ./examples/terraform \
     --out analysis_result.json
   ```

4. **Generate a readable report**:
   ```bash
   # Convert JSON analysis to a Markdown report
   ru-cloud-advisor generate-report \
     --input analysis_result.json \
     --format markdown \
     --output MIGRATION_PLAN.md
   ```

## Installation

### From Source

Recommended for developers and latest features:

```bash
git clone https://github.com/ranas-mukminov/ru-cloud-portability-advisor.git
cd ru-cloud-portability-advisor
pip install .
```

### Development Setup

To install with testing and linting tools:

```bash
pip install -e ".[dev]"
```

## Configuration

You can customize the analysis using a YAML configuration file. This allows you to specify source/target providers and region preferences.

**Example Config (`config.yaml`):**

```yaml
# Source provider (aws, gcp, hetzner)
source_provider: aws

# Target providers to consider
target_providers:
  - yandex
  - vk
  - selectel

# Preferred target region
region_preference: ru-central1

# Optional: Path to custom pricing data
pricing_file: ./custom_pricing.yaml

# Notes for the report
notes: "Migration project for payment gateway"
```

Pass this config to the analyzer:

```bash
ru-cloud-advisor analyze-project \
  --tf-path ./my-infra \
  --config ./config.yaml \
  --out report.json
```

## Usage & Common Tasks

### Analyze a Hybrid Project

If you have both Terraform and Kubernetes files:

```bash
ru-cloud-advisor analyze-project \
  --tf-path ./terraform \
  --k8s-path ./k8s \
  --out full_analysis.json
```

### View Supported Mappings

To see which resources can be automatically mapped:

```bash
ru-cloud-advisor print-mapping-table
```

### Generate HTML Report

For a report that can be shared with stakeholders:

```bash
ru-cloud-advisor generate-report \
  --input full_analysis.json \
  --format html \
  --output migration_report.html
```

## Update / Upgrade

To update to the latest version from the repository:

```bash
git pull origin main
pip install . --upgrade
```

If you installed via `pip install -e`, simply pulling the latest code is sufficient.

## Logs & Troubleshooting

- **Parsing Errors**: If the tool fails to parse a `.tf` file, ensure it is valid HCL. The tool uses `python-hcl2` which is robust but may stumble on complex dynamic blocks.
- **Missing Mappings**: If a resource shows as "Unknown" or "No mapping found", check `src/ru_cloud_portability_advisor/mapping/rules`. You can add new rules there.
- **Verbose Output**: Currently, the tool prints errors to stderr.

## Security Notes

- **Local Execution**: This tool analyzes files locally. No code or credentials are uploaded to any cloud.
- **Secrets**: The tool does not extract values from `variable` blocks or `secrets.yaml` files, but always ensure you do not commit actual secrets to your repository.
- **Dependencies**: Regularly update dependencies to patch vulnerabilities:
  ```bash
  pip-audit
  ```

## Project Structure

- `src/ru_cloud_portability_advisor/` — Main package source code.
  - `advisor/` — Analysis logic.
  - `mapping/rules/` — YAML definitions for resource mapping.
  - `cli/` — Command-line interface entry points.
  - `render/` — Report generation logic.
- `examples/` — Sample Terraform and Kubernetes projects for testing.
- `tests/` — Unit and integration tests.

## Dependencies

From `pyproject.toml` (Python 3.10+):

- `typer>=0.12` — CLI framework
- `rich>=13.0` — terminal formatting
- `PyYAML>=6.0` — YAML parsing
- `python-hcl2>=4.3` — Terraform HCL parsing
- `jsonschema>=4.17` — configuration validation
- `jinja2>=3.1` — template rendering
- `pydantic>=2.0` — data validation
- `tabulate>=0.9` — table formatting

Development extras (`pip install -e ".[dev]"`) add `pytest`, `mypy`, `ruff`, `black`, `isort`, `yamllint`, `pip-audit`, and `bandit`.

## What Is Analyzed

- **Infrastructure discovery**: Terraform resources and Kubernetes manifests, with automatic source-provider detection (AWS, GCP, Hetzner).
- **Service mapping**: storage, databases, Kubernetes, load balancers, queues, and serverless functions, mapped to Yandex Cloud, VK Cloud, Cloud.ru, and Selectel equivalents using `src/ru_cloud_portability_advisor/mapping/rules/`.
- **Migration assessment**: 1:1 mappings, mappings that need refactoring, and services with no direct equivalent, plus risk notes.
- **Cost estimation**: current vs. target cost, estimated only from pricing data supplied by the user in a pricing file (see `examples/pricing/`); the tool does not scrape provider tariffs.
- **Generated artifacts**: JSON/Markdown/HTML migration reports. The AI layer (`src/ru_cloud_portability_advisor/ai/`) is an interface with stub implementations only — it returns a "not configured" placeholder until a provider implementation is supplied; it does not generate finished Terraform or Kubernetes files by itself.

## Examples

All three use sample inputs that exist in this repository and the CLI flags in `src/ru_cloud_portability_advisor/cli/commands/` (`--tf-path`, `--k8s-path`, `--config`, `--out`, `--input`, `--format`, `--output`).

### AWS to Yandex Cloud

```bash
ru-cloud-advisor analyze-project \
  --tf-path examples/terraform/aws_sample \
  --config src/ru_cloud_portability_advisor/config/examples/aws_to_yc_simple.yaml \
  --out ./out/aws_to_yc.json

ru-cloud-advisor generate-report \
  --input ./out/aws_to_yc.json \
  --format html \
  --output ./out/aws_to_yc_report.html
```

### GCP to VK Cloud

```bash
ru-cloud-advisor analyze-project \
  --tf-path examples/terraform/gcp_sample \
  --k8s-path examples/k8s \
  --config src/ru_cloud_portability_advisor/config/examples/gcp_to_vk_medium.yaml \
  --out ./out/gcp_to_vk.json
```

### Hetzner to Selectel

```bash
ru-cloud-advisor analyze-project \
  --tf-path examples/terraform/hetzner_sample \
  --config src/ru_cloud_portability_advisor/config/examples/hetzner_to_selectel.yaml \
  --out ./out/hetzner_to_selectel.json
```

## Configuration

Configuration files follow the fields documented in `src/ru_cloud_portability_advisor/config/schema.yaml`:

```yaml
source_provider: aws  # aws | gcp | hetzner
target_providers:
  - yandex  # yandex | vk | cloud_ru | selectel
region_preference: ru-central1  # optional
pricing_file: ./pricing/aws_to_yc_pricing.yaml  # optional, user-supplied prices
notes: "Migration project notes"  # optional
```

See `src/ru_cloud_portability_advisor/config/examples/` and `examples/pricing/` for complete examples. Pricing files use per-unit fields such as `cost_per_vcpu_hour`, `cost_per_gb_ram_hour`, `cost_per_gb_storage_month`, and `cost_per_gb_egress_month` — not a nested per-instance-type price list.

## Troubleshooting

- **No resources detected**: check that `--tf-path` and `--k8s-path` point at directories containing `.tf` or `.yaml`/`.yml` files, and that Terraform resources use a recognised provider syntax (for example `aws_instance`, `google_compute_instance`).
- **Mapping not found**: a resource may show as unknown or with no equivalent. Run `ru-cloud-advisor print-mapping-table` to see the available mappings, check the detected source provider, and review `src/ru_cloud_portability_advisor/mapping/rules/`.
- **Cost estimation shows "N/A" or looks wrong**: cost estimation needs a `pricing_file` in the configuration, in the format used by `examples/pricing/`, covering the resource types in the input.
- **Parsing errors**: validate the input first (`terraform validate` for Terraform, YAML validation for Kubernetes manifests) and check that files are UTF-8 encoded; parser errors include file paths and line numbers.

## Contributing

We welcome contributions!

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/new-mapping`).
3. Add your changes (e.g., new mapping rules in `src/.../mapping/rules`).
4. Run tests: `pytest`.
5. Commit and push: `git push origin feature/new-mapping`.
6. Open a Pull Request.

## License

This project is licensed under the [Apache 2.0 License](LICENSE).

## Author and Commercial Support

**Author**: [Ranas Mukminov](https://github.com/ranas-mukminov)

For production-grade migration planning, infrastructure audits, and DevOps support, visit **[run-as-daemon.ru](https://run-as-daemon.ru)** (Russian) or contact the author via GitHub profile.
