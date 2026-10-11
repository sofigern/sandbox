import pytest
from hypothesis import given
from hypothesis import strategies as st

from biology.c1_exact_matching.c1_6_exercises.c1_6_9_match_counts.match_counts import (
    match_counts,
)


def by_definition(a: str, b: str, k: int) -> list[list[int]]:
    windows = len(a) - k + 1
    return [
        [
            sum(x == y for x, y in zip(a[i : i + k], b[j : j + k], strict=True))
            for j in range(windows)
        ]
        for i in range(windows)
    ]


@st.composite
def two_strings_and_k(draw):
    n = draw(st.integers(0, 8))
    a = draw(st.text(alphabet="ab", min_size=n, max_size=n))
    b = draw(st.text(alphabet="ab", min_size=n, max_size=n))
    return a, b, draw(st.integers(0, n))


@given(two_strings_and_k())
def test_agrees_with_the_definition(abk):
    a, b, k = abk
    assert match_counts(a, b, k) == by_definition(a, b, k)


@pytest.mark.parametrize(
    ("a", "b", "k", "counts"),
    [
        ("abc", "abd", 2, [[2, 0], [0, 1]]),
        ("abc", "abc", 3, [[3]]),
        ("aaa", "aaa", 1, [[1, 1, 1], [1, 1, 1], [1, 1, 1]]),
        ("abc", "xyz", 1, [[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
        ("ab", "ab", 0, [[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
        ("", "", 0, [[0]]),
    ],
    ids=["book_style", "whole_string", "all_same", "disjoint", "k_zero", "empty"],
)
def test_examples(a, b, k, counts):
    assert match_counts(a, b, k) == counts
