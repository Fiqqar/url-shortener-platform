#!/usr/bin/env python3
"""Validate the repository monitoring configuration without starting the stack.

Catches, before runtime:

- monitoring/prometheus/prometheus.yml parses and still scrapes the backend
- monitoring/grafana/provisioning/ datasources and dashboard providers parse
- monitoring/grafana/dashboards/*.json parse, reference provisioned datasource
  uids, and expose their PromQL expressions for promtool validation

Use --promql-out to dump the dashboard expressions, then feed them to promtool:

    promtool --experimental promql format "<expression>"

Exit status is 1 when any problem is found; every problem is reported, not just
the first one.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml  # type: ignore[import-untyped]

BACKEND_JOB = "url-shortener-backend"
BACKEND_TARGET = "backend:8000"


class Validation:
    """Collects every problem found in the monitoring configuration."""

    def __init__(self) -> None:
        self.errors: list[str] = []

    def fail(self, path: Path, message: str) -> None:
        self.errors.append(f"{path}: {message}")

    def load_yaml(self, path: Path):
        try:
            with path.open(encoding="utf-8") as handle:
                return yaml.safe_load(handle)
        except FileNotFoundError:
            self.fail(path, "file not found")
        except yaml.YAMLError as exc:
            self.fail(path, f"invalid YAML: {exc}")
        return None

    def load_json(self, path: Path):
        try:
            with path.open(encoding="utf-8") as handle:
                return json.load(handle)
        except FileNotFoundError:
            self.fail(path, "file not found")
        except json.JSONDecodeError as exc:
            self.fail(path, f"invalid JSON: {exc}")
        return None


def datasource_uid(value) -> str | None:
    if isinstance(value, dict):
        return value.get("uid")
    if isinstance(value, str):
        return value
    return None


def check_prometheus(check: Validation, monitoring_dir: Path) -> None:
    config_path = monitoring_dir / "prometheus" / "prometheus.yml"
    config = check.load_yaml(config_path)
    if config is None:
        return
    if not isinstance(config, dict):
        check.fail(config_path, "top level must be a mapping")
        return

    scrape_configs = config.get("scrape_configs")
    if not isinstance(scrape_configs, list) or not scrape_configs:
        check.fail(config_path, "scrape_configs must be a non-empty list")
    else:
        jobs = {
            job.get("job_name"): job for job in scrape_configs if isinstance(job, dict)
        }
        job = jobs.get(BACKEND_JOB)
        if job is None:
            check.fail(config_path, f"missing scrape job '{BACKEND_JOB}'")
        else:
            if job.get("metrics_path") != "/metrics":
                check.fail(config_path, f"job '{BACKEND_JOB}' must use metrics_path /metrics")
            targets: list = []
            static_configs = job.get("static_configs")
            if isinstance(static_configs, list):
                for entry in static_configs:
                    if isinstance(entry, dict) and isinstance(entry.get("targets"), list):
                        targets.extend(entry["targets"])
            if BACKEND_TARGET not in targets:
                check.fail(config_path, f"job '{BACKEND_JOB}' must scrape {BACKEND_TARGET}")

    if not config.get("rule_files"):
        check.fail(config_path, "rule_files must reference the mounted rules directory")


def check_datasources(check: Validation, monitoring_dir: Path) -> set[str]:
    datasource_dir = monitoring_dir / "grafana" / "provisioning" / "datasources"
    files = sorted(datasource_dir.glob("*.yml"))
    if not files:
        check.fail(datasource_dir, "no datasource provisioning files found")
        return set()

    uids: set[str] = set()
    has_default = False
    for path in files:
        doc = check.load_yaml(path)
        if doc is None:
            continue
        entries = doc.get("datasources") if isinstance(doc, dict) else None
        if not isinstance(entries, list) or not entries:
            check.fail(path, "expected a non-empty 'datasources' list")
            continue
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict):
                check.fail(path, f"datasources[{index}] must be a mapping")
                continue
            for field in ("name", "type", "uid", "url"):
                if not entry.get(field):
                    check.fail(path, f"datasources[{index}] is missing '{field}'")
            uid = entry.get("uid")
            if uid:
                uids.add(uid)
            if entry.get("isDefault"):
                has_default = True

    if uids and not has_default:
        check.fail(datasource_dir, "no datasource is marked as default")
    return uids


def check_dashboard_providers(check: Validation, monitoring_dir: Path) -> None:
    provider_dir = monitoring_dir / "grafana" / "provisioning" / "dashboards"
    files = sorted(provider_dir.glob("*.yml"))
    if not files:
        check.fail(provider_dir, "no dashboard provider files found")
        return

    for path in files:
        doc = check.load_yaml(path)
        if doc is None:
            continue
        providers = doc.get("providers") if isinstance(doc, dict) else None
        if not isinstance(providers, list) or not providers:
            check.fail(path, "expected a non-empty 'providers' list")
            continue
        for index, provider in enumerate(providers):
            if not isinstance(provider, dict):
                check.fail(path, f"providers[{index}] must be a mapping")
                continue
            if not provider.get("name"):
                check.fail(path, f"providers[{index}] is missing 'name'")
            if provider.get("type") != "file":
                check.fail(path, f"providers[{index}] must use type 'file'")
            options = provider.get("options")
            if not isinstance(options, dict) or not options.get("path"):
                check.fail(path, f"providers[{index}] is missing options.path")


def check_dashboards(
    check: Validation, monitoring_dir: Path, datasource_uids: set[str]
) -> list[str]:
    dashboard_dir = monitoring_dir / "grafana" / "dashboards"
    files = sorted(dashboard_dir.glob("*.json"))
    if not files:
        check.fail(dashboard_dir, "no dashboard files found")
        return []

    expressions: list[str] = []
    for path in files:
        doc = check.load_json(path)
        if doc is None:
            continue
        if not isinstance(doc, dict):
            check.fail(path, "top level must be an object")
            continue
        if not doc.get("uid"):
            check.fail(path, "dashboard is missing 'uid'")
        if not doc.get("title"):
            check.fail(path, "dashboard is missing 'title'")

        panels = doc.get("panels")
        if not isinstance(panels, list) or not panels:
            check.fail(path, "expected a non-empty 'panels' list")
            continue

        for index, panel in enumerate(panels):
            if not isinstance(panel, dict):
                check.fail(path, f"panels[{index}] must be an object")
                continue
            label = f"panels[{index}] ('{panel.get('title')}')"
            if not panel.get("title"):
                check.fail(path, f"{label} is missing a title")

            targets = panel.get("targets")
            if not isinstance(targets, list) or not targets:
                check.fail(path, f"{label} has no targets")
                continue

            panel_uid = datasource_uid(panel.get("datasource"))
            for target_index, target in enumerate(targets):
                if not isinstance(target, dict):
                    check.fail(path, f"{label} targets[{target_index}] must be an object")
                    continue
                expression = target.get("expr")
                if not isinstance(expression, str) or not expression.strip():
                    check.fail(path, f"{label} targets[{target_index}] is missing an expr")
                    continue
                expressions.append(expression.strip())

                uid = datasource_uid(target.get("datasource")) or panel_uid
                if not uid:
                    check.fail(path, f"{label} targets[{target_index}] has no datasource uid")
                elif datasource_uids and uid not in datasource_uids:
                    check.fail(
                        path,
                        f"{label} targets[{target_index}] references unknown datasource uid '{uid}'",
                    )

    return sorted(set(expressions))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--monitoring-dir", default="monitoring", type=Path)
    parser.add_argument(
        "--promql-out",
        type=Path,
        help="write the unique dashboard PromQL expressions to this file, one per line",
    )
    args = parser.parse_args()

    check = Validation()
    check_prometheus(check, args.monitoring_dir)
    datasource_uids = check_datasources(check, args.monitoring_dir)
    check_dashboard_providers(check, args.monitoring_dir)
    expressions = check_dashboards(check, args.monitoring_dir, datasource_uids)

    if check.errors:
        for error in check.errors:
            print(f"ERROR: {error}")
        print(f"monitoring configuration INVALID ({len(check.errors)} problem(s))")
        return 1

    if args.promql_out:
        # newline="\n" keeps the file LF-only so the promtool container
        # never sees a stray carriage return when this runs on Windows.
        args.promql_out.write_text(
            "\n".join(expressions) + "\n", encoding="utf-8", newline="\n"
        )

    print(
        "monitoring configuration OK "
        f"({len(expressions)} unique dashboard PromQL expression(s))"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
