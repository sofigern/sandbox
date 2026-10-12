import random

import pytest

from biology.c1_exact_matching.c1_6_exercises.c1_6_12_rectangular_composition import (
    rectangular_composition,
    rectangular_composition_numpy,
    rectangular_composition_sliding,
)

implementations = pytest.mark.parametrize(
    "rectangles",
    [
        rectangular_composition.rectangles,
        rectangular_composition_sliding.rectangles,
        rectangular_composition_numpy.rectangles,
    ],
    ids=["prefix_sums", "sliding", "numpy"],
)

# Fixed seed: every run, and every implementation, times the same inputs.
_rng = random.Random(0)
_side = 200
_letters = "abcdefghijklmnopqrstuvwxyz"


def _grid(alphabet):
    return ["".join(_rng.choices(alphabet, k=_side)) for _ in range(_side)]


# Each workload is (grid, collection); a collection of 12 has six shapes.
workloads = {
    # Expected case: a four-letter grid, so most windows are near misses.
    "dna_like": (_grid("acgt"), "".join(_rng.choices("acgt", k=12))),
    # Large alphabet: the grid's symbols are mostly absent from the collection.
    "letters": (_grid(_letters), "".join(_rng.choices(_letters, k=12))),
    # Every window of every shape matches.
    "all_hits": (["a" * _side] * _side, "a" * 12),
}


@pytest.mark.parametrize("workload", workloads)
@implementations
def bench_rectangles(benchmark, rectangles, workload):
    grid, s = workloads[workload]
    benchmark.group = workload
    benchmark(lambda: list(rectangles(grid, s)))


# The sliding scan claims Θ(n) space. 64 KB is a deficit counter, a window of
# strips and a few frames, and far below the prefix-sum tables' 1.5-10 MB on
# these grids (measured 2026-10-13), so only a change of shape trips it.
@pytest.mark.limit_memory("64 KB")
@pytest.mark.parametrize("workload", workloads)
def bench_linear_space(workload):
    grid, s = workloads[workload]
    for _ in rectangular_composition_sliding.rectangles(grid, s):
        pass
