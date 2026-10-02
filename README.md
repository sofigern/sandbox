# sandbox

My exercise repo for learning algorithms, starting with string matching for DNA sequencing.
Each exercise is a small Python module with tests, and several solutions to the same problem are checked against one shared test suite and timed against each other.

## Setup

You need [uv](https://docs.astral.sh/uv/).

```sh
git clone https://github.com/sofigern/sandbox.git
cd sandbox
uv sync
```

`uv sync` installs Python 3.14 if needed and the exact tool versions pinned in `uv.lock`.

## Layout

```
biology/                       exercises, one package per course level
  c1_exact_matching/           chapter: exact matching
    c1_1_naive/naive.py        section: the naive algorithm
      c1_1_1_naive_improvements/naive_improvements.py   a sub-step: an optimised variant
test/                          tests, mirroring the same tree
benchmark/                     timing comparisons, mirroring the same tree
```

Folders are named `c` plus the course number, then the topic: `c1_1_naive` is section 1.1.
A sub-step nests inside its section, so listings always show it right after its parent.

## Running the checks

```sh
uv run pytest                  # tests, plus the examples in docstrings
uv run ruff check .            # lint: likely bugs, import order, outdated syntax
uv run ruff format .           # format the code
```

CI runs the same three checks on every push and pull request.

## Benchmarks

Benchmarks answer "which solution is faster, and on what input".
They time every implementation of a problem on the same named workloads, such as random DNA and a worst case, and print one table per workload with the fastest as `1.0`.
They are slow and their numbers depend on the machine, so plain `uv run pytest` and CI skip them; run them on request:

```sh
uv run pytest benchmark
```

Compare numbers from one machine, run back to back, never across machines.
To focus on one workload, add `-k worst_case`; to keep a run and compare a later one against it, use `--benchmark-autosave` and then `--benchmark-compare`.
Only trust the timing of a solution that passes its tests: a solution that skips work it should not do is fast and wrong.

## Adding a solution

A new solution to an existing problem joins the shared tests and the benchmarks by being added to the `implementations` list in both `test/biology/c1_exact_matching/test_exact_matching.py` and `benchmark/biology/c1_exact_matching/bench_exact_matching.py`.
Every test and every workload then runs against it automatically.

Conventions for naming, tests and docstrings are in [`AGENTS.md`](AGENTS.md).
