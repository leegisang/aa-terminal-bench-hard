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
- [`data/current_benchmark_crosswalk.tsv`](data/current_benchmark_crosswalk.tsv): current TB1/TB2 presence and difficulty labels for the AA 44-task list.
- [`scripts/reproduce.sh`](scripts/reproduce.sh): clones Terminal-Bench, checks out the pinned commit, regenerates the 48-task hard list, and compares it with the AA list in this repository.
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

This repository does not redistribute Terminal-Bench task contents. It only stores task IDs and a small reproduction script. Terminal-Bench belongs to its authors and maintainers. Artificial Analysis' benchmark methodology belongs to Artificial Analysis.
