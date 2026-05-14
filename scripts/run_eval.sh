#!/usr/bin/env bash
set -euo pipefail

# AA-style evaluation entrypoint.
#
# This wrapper keeps the shell interface stable and delegates the scoring logic
# to scripts/eval.py. The actual agent/harness command is intentionally
# supplied by the caller because AA's Terminus 2 harness is not part of this
# repository.
#
# Example smoke test:
#   ./scripts/run_eval.sh --dry-run --tasks aimo-airline-departures --repeats 1
#
# Example real run with a command that returns 0 on pass and non-zero on fail:
#   AA_RUNNER_COMMAND='tb run --dataset-path {repo}/tasks --task-id {task} --agent my-agent' \
#     ./scripts/run_eval.sh

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT/scripts/eval.py" --config "$ROOT/aa_eval.yaml" "$@"
