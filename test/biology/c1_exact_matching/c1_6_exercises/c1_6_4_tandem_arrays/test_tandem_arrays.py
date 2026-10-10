import pytest
from hypothesis import given
from hypothesis import strategies as st

from biology.c1_exact_matching.c1_6_exercises.c1_6_4_tandem_arrays.tandem_arrays import (
    maximal_tandem_arrays,
)


def by_definition(s: str, base: str) -> list[tuple[int, int]]:
    m = len(base)
    out = []
    for start in range(len(s)):
        copies = 0
        while s.startswith(base, start + copies * m):
            copies += 1
        extends_left = start >= m and s.startswith(base, start - m)
        if copies >= 2 and not extends_left:
            out.append((start, copies))
    return out


@given(
    st.text(alphabet="ab", max_size=14), st.text(alphabet="ab", min_size=1, max_size=3)
)
def test_agrees_with_the_definition(s, base):
    """Order is not part of the contract, so both sides are compared sorted."""
    assert sorted(maximal_tandem_arrays(s, base)) == by_definition(s, base)


@pytest.mark.parametrize(
    ("s", "base", "arrays"),
    [
        ("xyzabcabcabcabcpq", "abc", [(3, 4)]),
        ("xyzabcabcabcabcpq", "abcabc", [(3, 2)]),
        ("abcabc", "abc", [(0, 2)]),
        ("abc", "abc", []),
        ("aaaa", "a", [(0, 4)]),
        ("aaaaa", "aa", [(0, 2), (1, 2)]),
        ("aaaaaa", "aa", [(0, 3), (1, 2)]),
        ("abababa", "ab", [(0, 3)]),
        ("abababa", "ba", [(1, 3)]),
        ("abab.abab", "ab", [(0, 2), (5, 2)]),
        ("", "a", []),
    ],
    ids=[
        "book_example",
        "longer_base",
        "whole_string",
        "single_copy",
        "one_letter",
        "two_phases_overlap",
        "phases_end_in_the_other_order",
        "even_phase",
        "odd_phase",
        "two_arrays",
        "empty_s",
    ],
)
def test_examples(s, base, arrays):
    assert sorted(maximal_tandem_arrays(s, base)) == arrays


def test_rejects_an_empty_base():
    with pytest.raises(ValueError):
        maximal_tandem_arrays("aaa", "")
