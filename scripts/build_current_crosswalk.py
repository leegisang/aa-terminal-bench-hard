#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


TB1_URL = "https://www.tbench.ai/benchmarks/terminal-bench-1"
TB2_URL = "https://www.tbench.ai/benchmarks/terminal-bench-2"


class BenchmarkPageParser(HTMLParser):
    def __init__(self, registry_prefix: str) -> None:
        super().__init__()
        self.registry_prefix = registry_prefix
        self.tasks: dict[str, str] = {}
        self.current_task: str | None = None
        self.current_badges: list[str] = []
        self.in_badge = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        href = attr.get("href")
        if tag == "a" and href and href.startswith(self.registry_prefix):
            self.current_task = href.rstrip("/").split("/")[-1]
            self.current_badges = []
            return

        if self.current_task and tag == "span":
            self.in_badge = True

    def handle_endtag(self, tag: str) -> None:
        if self.current_task and tag == "span":
            self.in_badge = False
            return

        if self.current_task and tag == "a":
            difficulty = next(
                (
                    badge
                    for badge in reversed(self.current_badges)
                    if badge in {"easy", "medium", "hard"}
                ),
                "",
            )
            if difficulty:
                self.tasks[self.current_task] = difficulty
            self.current_task = None
            self.current_badges = []
            self.in_badge = False

    def handle_data(self, data: str) -> None:
        if self.current_task and self.in_badge:
            text = data.strip()
            if text:
                self.current_badges.append(text)


def fetch_tasks(url: str, registry_prefix: str) -> dict[str, str]:
    with urllib.request.urlopen(url, timeout=30) as response:
        html = response.read().decode("utf-8")
    parser = BenchmarkPageParser(registry_prefix)
    parser.feed(html)
    return parser.tasks


def load_task_ids(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


def render_markdown_table(rows: list[dict[str, str]]) -> str:
    lines = [
        "| Task | TB1 current | TB1 difficulty | TB2 current | TB2 difficulty |",
        "|---|---:|---|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {task} | {tb1_present} | {tb1_difficulty} | {tb2_present} | {tb2_difficulty} |".format(
                **row
            )
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the current TB1/TB2 crosswalk for AA Terminal-Bench Hard tasks."
    )
    parser.add_argument(
        "--aa-list",
        type=Path,
        default=Path("artifacts/aa_terminal_bench_hard_tasks.txt"),
    )
    parser.add_argument(
        "--tsv",
        type=Path,
        default=Path("artifacts/current_benchmark_crosswalk.tsv"),
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Print a Markdown table to stdout instead of writing TSV.",
    )
    args = parser.parse_args()

    aa_tasks = load_task_ids(args.aa_list)
    tb1 = fetch_tasks(TB1_URL, "/registry/terminal-bench-core/0.1.1/")
    tb2 = fetch_tasks(TB2_URL, "/registry/terminal-bench/2.0/")

    rows = []
    for task in aa_tasks:
        tb1_difficulty = tb1.get(task, "")
        tb2_difficulty = tb2.get(task, "")
        rows.append(
            {
                "task": task,
                "tb1_present": "yes" if tb1_difficulty else "no",
                "tb1_difficulty": tb1_difficulty or "-",
                "tb2_present": "yes" if tb2_difficulty else "no",
                "tb2_difficulty": tb2_difficulty or "-",
            }
        )

    if args.markdown:
        print(render_markdown_table(rows))
        return 0

    with args.tsv.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "task",
                "tb1_present",
                "tb1_difficulty",
                "tb2_present",
                "tb2_difficulty",
            ],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {args.tsv}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
