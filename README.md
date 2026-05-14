# AA Terminal-Bench Hard

This repository documents the task provenance for Artificial Analysis' "Terminal-Bench Hard" evaluation.

It exists because the naming is easy to confuse:

- It is not the official Terminal-Bench 1.0 / `terminal-bench-core` 0.1.1 release split.
- It is not Terminal-Bench 2.0.
- It is the hard-labeled task pool from a pinned Terminal-Bench repository commit, filtered to the 44 tasks published by Artificial Analysis.

## Short Version

Artificial Analysis says its Terminal-Bench Hard evaluation uses:

- `terminal-bench-core`
- latest dataset version as of 2025-08-14
- commit `74221fb`
- 44 evaluated tasks
- Terminus 2 agent harness
- 3 repeats per task
- pass/fail test-suite scoring

Source: [Artificial Analysis Intelligence Benchmarking Methodology](https://artificialanalysis.ai/methodology/intelligence-benchmarking#terminal-bench-hard)

At the pinned Terminal-Bench commit, there are 48 tasks labeled `difficulty: hard`.
The 44 tasks in Artificial Analysis' published list are those 48 minus 4 tasks.

## Pinned Source

Terminal-Bench repository:

https://github.com/harbor-framework/terminal-bench

Pinned commit:

```text
74221fb0b6b5a7f88e53bed5726edaaf236348c9
```

Commit summary:

```text
2025-08-13 New task: CSP related to vacation scheduling (#551)
```

The task source tree at that commit is:

https://github.com/harbor-framework/terminal-bench/tree/74221fb0b6b5a7f88e53bed5726edaaf236348c9/tasks

## Files

- [`data/aa_terminal_bench_hard_tasks.txt`](data/aa_terminal_bench_hard_tasks.txt): the 44 task IDs published by Artificial Analysis.
- [`data/tbench_hard_at_74221fb.txt`](data/tbench_hard_at_74221fb.txt): all 48 task IDs labeled `difficulty: hard` at the pinned Terminal-Bench commit.
- [`data/not_in_aa_published_list.txt`](data/not_in_aa_published_list.txt): the 4 hard-labeled tasks at the pinned commit that are not in the AA-published 44.
- [`scripts/reproduce.sh`](scripts/reproduce.sh): clones Terminal-Bench, checks out the pinned commit, regenerates the 48-task hard list, and compares it with the AA list in this repository.

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
```

## Excluded By Diff

Artificial Analysis says a small number of tasks are excluded due to external dependency issues in the original dataset. The four hard-labeled tasks at the pinned commit that are not in the published AA 44-task list are:

```text
causal-inference-r
install-windows-3.11
lean4-proof
mcmc-sampling-stan
```

## Notes

`aimo-airline-departures` is a useful example of why the pinned commit matters. It is present at commit `74221fb` and was labeled `difficulty: hard` there, but later repository state and registry views may show different labels or splits.

This repository does not redistribute Terminal-Bench task contents. It only stores task IDs and a small reproduction script. Terminal-Bench belongs to its authors and maintainers. Artificial Analysis' benchmark methodology belongs to Artificial Analysis.
