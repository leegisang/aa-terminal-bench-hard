#!/usr/bin/env python3
"""AA-style pass@1 evaluator wrapper.

This script does not implement an agent or the Terminal-Bench harness itself.
Instead, it applies the Artificial Analysis evaluation policy around a
user-supplied per-task command:

  * read the AA task list from aa_eval.yaml
  * run every task for the configured number of repeats
  * treat command exit code 0 as pass@1 = 1 and non-zero/timeout as pass@1 = 0
  * average all task-repeat attempts into one component score

The command can be provided with --runner-command or AA_RUNNER_COMMAND. It may
use format placeholders such as {task}, {repeat}, {repo}, {task_dir},
{manifest}, and {run_dir}.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "aa_eval.yaml"


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"null", "None", "~"}:
        return None
    if value in {"true", "false"}:
        return value == "true"
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value


def load_simple_yaml(path: Path) -> dict[str, dict[str, Any]]:
    """Parse the small YAML subset used by aa_eval.yaml.

    Keeping this parser local avoids adding PyYAML as a dependency just to read
    a flat, human-auditable config file.
    """
    data: dict[str, dict[str, Any]] = {}
    section: str | None = None
    for raw_line in path.read_text().splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line.startswith(" ") and stripped.endswith(":"):
            section = stripped[:-1]
            data[section] = {}
            continue
        if section is None or not line.startswith("  ") or ":" not in stripped:
            raise ValueError(f"Unsupported config line in {path}: {raw_line}")
        key, value = stripped.split(":", 1)
        data[section][key.strip()] = _parse_scalar(value)
    return data


def read_task_ids(config: dict[str, dict[str, Any]], selected: list[str] | None) -> list[str]:
    task_list_path = ROOT / str(config["benchmark"]["task_list_path"])
    task_ids = [line.strip() for line in task_list_path.read_text().splitlines() if line.strip()]
    if selected:
        selected_set = set(selected)
        missing = sorted(selected_set - set(task_ids))
        if missing:
            raise SystemExit(f"Unknown task id(s): {', '.join(missing)}")
        task_ids = [task for task in task_ids if task in selected_set]
    return task_ids


def build_attempt_env(config: dict[str, dict[str, Any]], task: str, repeat: int, task_dir: Path, manifest: Path, run_dir: Path) -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "AA_TASK_ID": task,
            "AA_REPEAT_INDEX": str(repeat),
            "AA_TASK_DIR": str(task_dir),
            "AA_TASK_MANIFEST": str(manifest),
            "AA_RUN_DIR": str(run_dir),
            "AA_REPEATS": str(config["benchmark"]["repeats"]),
            "AA_SCORING": str(config["benchmark"]["scoring"]),
            "AA_AGGREGATE": str(config["benchmark"]["aggregate"]),
        }
    )
    for key, value in config.get("execution", {}).items():
        if value is not None:
            env[f"AA_{key.upper()}"] = str(value)
    return env


def run_attempt(command_template: str, config: dict[str, dict[str, Any]], task: str, repeat: int, output_dir: Path) -> dict[str, Any]:
    task_root = ROOT / str(config["benchmark"]["task_root"])
    task_dir = task_root / task
    manifest = task_dir / str(config["benchmark"]["task_manifest"])
    attempt_name = f"{task}__repeat-{repeat}"
    run_dir = output_dir / "attempts" / attempt_name
    run_dir.mkdir(parents=True, exist_ok=True)

    if not manifest.exists():
        raise FileNotFoundError(f"Missing task manifest: {manifest}")

    command = command_template.format(
        task=task,
        task_id=task,
        repeat=repeat,
        repeat_index=repeat,
        repo=ROOT,
        task_dir=task_dir,
        manifest=manifest,
        run_dir=run_dir,
    )
    env = build_attempt_env(config, task, repeat, task_dir, manifest, run_dir)
    timeout = config.get("execution", {}).get("global_timeout_sec")

    started = time.time()
    stdout_path = run_dir / "stdout.log"
    stderr_path = run_dir / "stderr.log"
    timed_out = False
    exit_code: int | None = None

    with stdout_path.open("w") as stdout, stderr_path.open("w") as stderr:
        try:
            completed = subprocess.run(
                command,
                cwd=ROOT,
                env=env,
                shell=True,
                stdout=stdout,
                stderr=stderr,
                timeout=float(timeout) if timeout is not None else None,
            )
            exit_code = completed.returncode
        except subprocess.TimeoutExpired:
            timed_out = True

    duration_sec = time.time() - started
    passed = (exit_code == 0) and not timed_out
    return {
        "task_id": task,
        "repeat_index": repeat,
        "pass_at_1": 1 if passed else 0,
        "passed": passed,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "duration_sec": duration_sec,
        "command": command,
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
    }


def write_summary(output_dir: Path, attempts: list[dict[str, Any]], config: dict[str, dict[str, Any]]) -> dict[str, Any]:
    total = len(attempts)
    passed = sum(int(attempt["pass_at_1"]) for attempt in attempts)
    summary = {
        "benchmark": config["benchmark"]["name"],
        "scoring": config["benchmark"]["scoring"],
        "aggregate": config["benchmark"]["aggregate"],
        "total_attempts": total,
        "passed_attempts": passed,
        "failed_attempts": total - passed,
        "pass_at_1": passed / total if total else 0.0,
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run AA-style binary pass@1 evaluation.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--runner-command", default=os.environ.get("AA_RUNNER_COMMAND"))
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--tasks", nargs="*", help="Optional task subset for smoke tests.")
    parser.add_argument("--repeats", type=int, help="Override repeats for smoke tests.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned attempts without executing.")
    args = parser.parse_args()

    config = load_simple_yaml(args.config)
    task_ids = read_task_ids(config, args.tasks)
    repeats = args.repeats if args.repeats is not None else int(config["benchmark"]["repeats"])
    output_dir = args.output_dir or ROOT / "runs" / time.strftime("aa-eval-%Y%m%d-%H%M%S")

    if not args.runner_command and not args.dry_run:
        raise SystemExit("Provide --runner-command or AA_RUNNER_COMMAND, or use --dry-run.")

    planned = [(task, repeat) for task in task_ids for repeat in range(1, repeats + 1)]
    print(f"Benchmark: {config['benchmark']['name']}")
    print(f"Planned attempts: {len(planned)} ({len(task_ids)} tasks * {repeats} repeats)")

    if args.dry_run:
        template = args.runner_command or "<runner-command>"
        for task, repeat in planned:
            task_dir = ROOT / str(config["benchmark"]["task_root"]) / task
            manifest = task_dir / str(config["benchmark"]["task_manifest"])
            print(template.format(task=task, task_id=task, repeat=repeat, repeat_index=repeat, repo=ROOT, task_dir=task_dir, manifest=manifest, run_dir="<run_dir>"))
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    attempts_path = output_dir / "attempts.jsonl"
    attempts: list[dict[str, Any]] = []
    with attempts_path.open("w") as attempt_file:
        for index, (task, repeat) in enumerate(planned, start=1):
            print(f"[{index}/{len(planned)}] {task} repeat {repeat}")
            result = run_attempt(args.runner_command, config, task, repeat, output_dir)
            attempts.append(result)
            attempt_file.write(json.dumps(result, sort_keys=True) + "\n")
            attempt_file.flush()

    summary = write_summary(output_dir, attempts, config)
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"Results written to: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
