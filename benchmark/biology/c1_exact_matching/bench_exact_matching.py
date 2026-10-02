import random
from pydoc_data.topics import topics

import pytest

from biology.c1_exact_matching.c1_1_naive.c1_1_1_naive_improvements.naive_improvements import (
    naive_jump,
)
from biology.c1_exact_matching.c1_1_naive.naive import naive

implementations = pytest.mark.parametrize(
    "find", [naive, naive_jump], ids=["naive", "naive_jump"]
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
