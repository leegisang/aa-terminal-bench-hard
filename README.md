# AA Terminal-Bench Hard

This repository packages the 44 tasks used by Artificial Analysis for its "Terminal-Bench Hard" evaluation.

The important distinction:

- `tasks/` contains the runnable legacy Terminal-Bench task directories for the AA 44-task set.
- `artifacts/` contains generated provenance lists and crosswalks.
- This is not the official Terminal-Bench 1.0 split, and it is not Terminal-Bench 2.0.
- Terminal-Bench 2.0 lives here: https://github.com/harbor-framework/terminal-bench-2

## Artificial Analysis Naming

Artificial Analysis currently refers to two different Terminal-Bench-based evaluations:

| Artificial Analysis surface | Terminal-Bench eval | Task source | Tasks | Format | Applies to this repo |
|---|---|---|---:|---|---|
| Intelligence Index / Coding Index | Terminal-Bench Hard | `terminal-bench-core` hard subset at commit `74221fb`, with exclusions | 44 | legacy `task.yaml` Terminal-Bench tasks | yes |
| Coding Agent Index | Terminal-Bench v2 | Terminal-Bench 2.0, with five environment-compatibility exclusions | 84 of 89 | Harbor/TB2 `task.toml` tasks | no |

The AA Intelligence Index methodology page documents Terminal-Bench Hard, not Terminal-Bench v2.
The AA Coding Agent Index methodology page documents Terminal-Bench v2.

This repository tracks the first row only: the 44-task Terminal-Bench Hard evaluation used in the Intelligence/Coding Index.

## Task Set

Artificial Analysis describes Terminal-Bench Hard as:

- `terminal-bench-core`
- latest dataset version as of 2025-08-14
- commit `74221fb`
- 44 evaluated tasks
- Terminus 2 agent harness
- 3 repeats per task
- pass/fail test-suite scoring
- pass@1 reported as the average over all task repeats

Source: [Artificial Analysis Intelligence Benchmarking Methodology](https://artificialanalysis.ai/methodology/intelligence-benchmarking#terminal-bench-hard)

At the pinned Terminal-Bench commit, there are 48 tasks labeled `difficulty: hard`.
The 44 tasks in Artificial Analysis' published list are those 48 minus 4 tasks excluded by AA.

## AA Evaluation Policy

The Artificial Analysis Intelligence Index v4.0.4 methodology lists Terminal-Bench Hard under the Coding category:

- Category: Coding
- Field: Agentic Workflows
- Workload: 44 tasks, 3 repeats
- Response type: terminal-based task execution
- Scoring: test-suite pass/fail, pass@1
- Intelligence Index weight: 16.7%

For the agent execution policy, Artificial Analysis states that:

- Each task is successful only if its task-specific test suite fully passes.
- The Terminus 2 harness is used for consistency across models.
- Agent episodes are capped at 100 per task repeat.
- Task-level timeouts are overridden by a global 24-hour timeout.
- Each task repeat has a maximum cumulative input budget of 1 million tokens.
- Artificial Analysis reports that these constraints mostly affect models stuck in unsuccessful loops, with no consistent observed performance differences caused by the constraints.

## Runnable Layout

The tasks are copied from:

```text
https://github.com/harbor-framework/terminal-bench
commit 74221fb0b6b5a7f88e53bed5726edaaf236348c9
path   tasks/<task-id>/
```

Each task directory preserves the legacy Terminal-Bench format:

```text
tasks/<task-id>/
  Dockerfile
  docker-compose.yaml
  task.yaml
  run-tests.sh
  solution.sh
  tests/
```

Run with the legacy Terminal-Bench CLI from the repository root:

```bash
tb run --dataset-path tasks --agent oracle --task-id aimo-airline-departures
```

For agent runs, use the normal Terminal-Bench CLI flags with `--dataset-path tasks`.

## Artifacts

- [`artifacts/aa_terminal_bench_hard_tasks.txt`](artifacts/aa_terminal_bench_hard_tasks.txt): the 44 task IDs published by Artificial Analysis.
- [`artifacts/tbench_hard_at_74221fb.txt`](artifacts/tbench_hard_at_74221fb.txt): all 48 task IDs labeled `difficulty: hard` at the pinned Terminal-Bench commit.
- [`artifacts/not_in_aa_published_list.txt`](artifacts/not_in_aa_published_list.txt): the 4 hard-labeled tasks at the pinned commit that are not in the AA-published 44.
- [`artifacts/current_benchmark_crosswalk.tsv`](artifacts/current_benchmark_crosswalk.tsv): current TB1/TB2 presence and difficulty labels for the AA 44-task list.
- [`scripts/reproduce.sh`](scripts/reproduce.sh): clones Terminal-Bench, checks out the pinned commit, regenerates the 48-task hard list, and compares it with the AA list and local `tasks/`.
- [`scripts/build_current_crosswalk.py`](scripts/build_current_crosswalk.py): fetches the current TB1/TB2 benchmark pages and rebuilds the crosswalk.

## Reproduce

```bash
./scripts/reproduce.sh
```

Expected summary:

```text
Terminal-Bench hard tasks at 74221fb0b6b5a7f88e53bed5726edaaf236348c9: 48
Artificial Analysis published tasks: 44
Hard tasks not in AA published list: 4
AA tasks missing from pinned hard list: 0
Task directories in this repository: 44
```

## Excluded By Diff

Artificial Analysis says a small number of tasks are excluded due to external dependency issues in the original dataset. The four hard-labeled tasks at the pinned commit that are not in the published AA 44-task list are:

```text
causal-inference-r
install-windows-3.11
lean4-proof
mcmc-sampling-stan
```

## Current TB1/TB2 Crosswalk

This table compares the AA 44-task list against the current Terminal-Bench benchmark pages as of 2026-05-14:

- TB1 source: https://www.tbench.ai/benchmarks/terminal-bench-1
- TB2 source: https://www.tbench.ai/benchmarks/terminal-bench-2

Regenerate the TSV with:

```bash
./scripts/build_current_crosswalk.py
```

Print the Markdown table with:

```bash
./scripts/build_current_crosswalk.py --markdown
```

Summary:

- Present in current TB1: 21 / 44
- Present in current TB2: 19 / 44
- Present in neither current TB1 nor current TB2: 16 / 44

| Task | TB1 current | TB1 difficulty | TB2 current | TB2 difficulty |
|---|---:|---|---:|---|
| aimo-airline-departures | no | - | no | - |
| blind-maze-explorer-5x5 | yes | hard | no | - |
| cartpole-rl-training | yes | hard | no | - |
| chem-property-targeting | no | - | no | - |
| chem-rf | no | - | no | - |
| circuit-fibsqrt | no | - | yes | hard |
| cobol-modernization | no | - | yes | easy |
| configure-git-webserver | yes | hard | yes | hard |
| cross-entropy-method | no | - | no | - |
| extract-moves-from-video | yes | hard | yes | hard |
| feal-differential-cryptanalysis | no | - | yes | hard |
| feal-linear-cryptanalysis | no | - | yes | hard |
| form-filling | no | - | no | - |
| git-multibranch | yes | hard | yes | medium |
| gpt2-codegolf | yes | hard | yes | hard |
| install-windows-xp | no | - | no | - |
| make-doom-for-mips | no | - | yes | hard |
| make-mips-interpreter | no | - | yes | hard |
| model-extraction-relu-logits | no | - | yes | hard |
| movie-helper | no | - | no | - |
| neuron-to-jaxley-conversion | no | - | no | - |
| oom | yes | hard | no | - |
| organization-json-generator | yes | hard | no | - |
| parallel-particle-simulator | no | - | no | - |
| parallelize-graph | no | - | no | - |
| password-recovery | yes | hard | yes | hard |
| path-tracing | yes | hard | yes | hard |
| path-tracing-reverse | yes | hard | yes | hard |
| play-zork | yes | hard | no | - |
| play-zork-easy | no | - | no | - |
| polyglot-rust-c | yes | hard | yes | hard |
| prove-plus-comm | yes | hard | yes | easy |
| pytorch-model-cli | yes | hard | yes | medium |
| rare-mineral-allocation | no | - | no | - |
| recover-obfuscated-files | no | - | no | - |
| reverse-engineering | no | - | no | - |
| run-pdp11-code | yes | hard | no | - |
| stable-parallel-kmeans | no | - | no | - |
| super-benchmark-upet | yes | hard | no | - |
| swe-bench-astropy-1 | yes | hard | no | - |
| swe-bench-astropy-2 | yes | hard | no | - |
| train-fasttext | yes | hard | yes | hard |
| word2vec-from-scratch | no | - | no | - |
| write-compressor | yes | hard | yes | hard |

## Notes

`aimo-airline-departures` is a useful example of why the pinned commit matters. It is present at commit `74221fb` and was labeled `difficulty: hard` there, but later repository state and registry views may show different labels or splits.

The task files are copied from Terminal-Bench and retain the upstream Apache-2.0 license.
