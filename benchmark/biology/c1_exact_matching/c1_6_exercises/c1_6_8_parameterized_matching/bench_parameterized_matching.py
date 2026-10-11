import random

import pytest

from biology.c1_exact_matching.c1_6_exercises.c1_6_8_parameterized_matching import (
    parameterized_matching,
    parameterized_matching_numba,
    parameterized_matching_numpy,
    parameterized_matching_re,
)

# numba compiles on first use; keep that out of the timings.
list(parameterized_matching_numba.p_find("Xa", "XaXb"))


def naive_p_find(p, t):
    """Every window through p_match: the O(nm) baseline."""
    m = len(p)
    return (
        i
        for i in range(len(t) - m + 1)
        if parameterized_matching.p_match(p, t[i : i + m])
    )


implementations = pytest.mark.parametrize(
    "p_find",
    [
        naive_p_find,
        parameterized_matching.p_find,
        parameterized_matching_re.p_find,
        parameterized_matching_numba.p_find,
        parameterized_matching_numpy.p_find,
    ],
    ids=["naive", "z_values", "regex", "numba", "numpy"],
)

# Fixed seed: every run, and every implementation, times the same inputs.
_rng = random.Random(0)
# Code-like text: a few token kinds (upper case) among single-letter variables.
_code = "".join(_rng.choice("ABCDEabcdefgh") for _ in range(100_000))

# Each workload is (pattern, text).
workloads = {
    # Expected case: a 12-character fragment sampled from the text.
    "code_like": (_code[50_000:50_012], _code),
    # Worst case: every window agrees until the last character demands a new parameter.
    "worst_case": ("a" * 9 + "b", "a" * 20_000),
    # Every window p-matches: all parameters, pattern of distinct ones.
    "all_hits": ("abcd", "efgh" * 25_000),
}


@pytest.mark.parametrize("workload", workloads)
@implementations
def bench_p_find(benchmark, p_find, workload):
    p, t = workloads[workload]
    benchmark.group = workload
    benchmark(lambda: list(p_find(p, t)))
