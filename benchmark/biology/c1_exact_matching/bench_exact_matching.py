import random
from pydoc_data.topics import topics

import pytest

from biology.c1_exact_matching import builtin
from biology.c1_exact_matching.c1_1_naive.c1_1_1_naive_improvements.naive_improvements import (
    naive_jump,
)
from biology.c1_exact_matching.c1_1_naive.naive import naive
from biology.c1_exact_matching.c1_5_linear_simple import (
    linear_compact,
    linear_optimized,
    linear_quick,
    linear_simple,
)

implementations = pytest.mark.parametrize(
    "find",
    [
        builtin.match,
        naive,
        naive_jump,
        linear_simple.match,
        linear_optimized.match,
        linear_compact.match,
        linear_quick.match,
    ],
    ids=[
        "builtin",
        "naive",
        "naive_jump",
        "linear_simple",
        "linear_optimized",
        "linear_compact",
        "linear_quick",
    ],
)
# Matchers whose docstrings claim O(1) or Θ(m) space. Checked in bench_constant_space,
# never on the timed function: a `limit_memory` mark makes pytest-memray trace the
# test even without `--memray`, which slows the traced code 2-4x.
constant_space = pytest.mark.parametrize(
    "find",
    [
        builtin.match,
        naive,
        naive_jump,
        linear_optimized.match,
        linear_compact.match,
        linear_quick.match,
    ],
    ids=[
        "builtin",
        "naive",
        "naive_jump",
        "linear_optimized",
        "linear_compact",
        "linear_quick",
    ],
)

# Fixed seed: every run, and every implementation, times the same inputs.
_rng = random.Random(0)
_genome = "".join(_rng.choice("ACGT") for _ in range(100_000))
# Ships with Python, so it needs no download; fixed for a given Python version.
_english = " ".join(topics[k] for k in sorted(topics))[:100_000]

# Each workload is (pattern, text).
workloads = {
    # Expected case: a short read sampled from a random genome.
    "random_dna": (_genome[50_000:50_010], _genome),
    # Average English prose: Python's own help() text, first 100,000 characters.
    "english_text": ("the object", _english),
    # Worst case for naive: every alignment matches until its last character.
    "worst_case": ("a" * 9 + "b", "a" * 20_000),
}


@pytest.mark.parametrize("workload", workloads)
@implementations
def bench_exact_matching(benchmark, find, workload):
    p, t = workloads[workload]
    benchmark.group = workload
    benchmark(lambda: list(find(p, t)))


# 16 KB is a few frames and the result list, and ten times below the Θ(n)
# matchers' 176 KB on the smallest workload, so only a change of shape trips it.
@pytest.mark.limit_memory("16 KB")
@pytest.mark.parametrize("workload", workloads)
@constant_space
def bench_constant_space(find, workload):
    p, t = workloads[workload]
    list(find(p, t))
