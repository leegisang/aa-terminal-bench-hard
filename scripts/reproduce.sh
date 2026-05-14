#!/usr/bin/env bash
set -euo pipefail

COMMIT="${1:-74221fb0b6b5a7f88e53bed5726edaaf236348c9}"
TBENCH_REPO="${TBENCH_REPO:-https://github.com/harbor-framework/terminal-bench.git}"

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
REPO_ROOT="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
WORKDIR="$(mktemp -d)"

cleanup() {
  rm -rf "$WORKDIR"
}
trap cleanup EXIT

git -C "$WORKDIR" init --quiet terminal-bench
git -C "$WORKDIR/terminal-bench" remote add origin "$TBENCH_REPO"
git -C "$WORKDIR/terminal-bench" fetch --quiet --depth 1 origin "$COMMIT"
git -C "$WORKDIR/terminal-bench" checkout --quiet FETCH_HEAD

HARD_LIST="$WORKDIR/tbench_hard_at_commit.txt"
AA_LIST="$REPO_ROOT/artifacts/aa_terminal_bench_hard_tasks.txt"
NOT_IN_AA="$WORKDIR/not_in_aa.txt"
MISSING_FROM_HARD="$WORKDIR/missing_from_hard.txt"
EXTRACTED_TASKS="$WORKDIR/extracted_tasks.txt"

git -C "$WORKDIR/terminal-bench" grep -l '^difficulty: hard$' HEAD -- tasks \
  | sed 's#HEAD:tasks/##; s#/task.yaml##' \
  | sort > "$HARD_LIST"

comm -23 "$HARD_LIST" "$AA_LIST" > "$NOT_IN_AA"
comm -13 "$HARD_LIST" "$AA_LIST" > "$MISSING_FROM_HARD"

printf 'Terminal-Bench hard tasks at %s: %s\n' "$COMMIT" "$(wc -l < "$HARD_LIST" | tr -d ' ')"
printf 'Artificial Analysis published tasks: %s\n' "$(wc -l < "$AA_LIST" | tr -d ' ')"
printf 'Hard tasks not in AA published list: %s\n' "$(wc -l < "$NOT_IN_AA" | tr -d ' ')"
cat "$NOT_IN_AA"
printf 'AA tasks missing from pinned hard list: %s\n' "$(wc -l < "$MISSING_FROM_HARD" | tr -d ' ')"
cat "$MISSING_FROM_HARD"

if [ -d "$REPO_ROOT/tasks" ]; then
  find "$REPO_ROOT/tasks" -mindepth 1 -maxdepth 1 -type d \
    | sed 's#^.*/##' \
    | sort > "$EXTRACTED_TASKS"
  printf 'Task directories in this repository: %s\n' "$(wc -l < "$EXTRACTED_TASKS" | tr -d ' ')"
  diff -u "$AA_LIST" "$EXTRACTED_TASKS"
fi
