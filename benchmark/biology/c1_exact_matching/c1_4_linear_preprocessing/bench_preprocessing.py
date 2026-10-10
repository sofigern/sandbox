import random

import pytest

from biology.c1_exact_matching.c1_4_linear_preprocessing import (
    preprocessing,
    preprocessing_compact,
)

implementations = pytest.mark.parametrize(
    "z_of",
    [preprocessing.z_values, preprocessing_compact.z_values],
    ids=["gusfield", "compact"],
)

# Fixed seed: every run, and every implementation, times the same inputs.
_rng = random.Random(0)
_genome = "".join(_rng.choice("ACGT") for _ in range(100_000))
# Fibonacci word: highly repetitive yet never periodic.
_prev, _fibonacci = "a", "ab"
while len(_fibonacci) < 100_000:
    _prev, _fibonacci = _fibonacci, _fibonacci + _prev

workloads = {
    # Expected case: short Z-boxes everywhere.
    "random_dna": _genome,
    # One Z-box spans the whole string; every position reuses it.
    "all_same": "a" * 100_000,
    # Long boxes that keep hitting their end: the explicit-extension case.
    "periodic": "aab" * 33_333,
    # Many positions inside a box whose reused value stops short.
    "fibonacci": _fibonacci[:100_000],
}


@pytest.mark.parametrize("workload", workloads)
@implementations
def bench_z_values(benchmark, z_of, workload):
    s = workloads[workload]
    benchmark.group = workload
    benchmark(z_of, s)
