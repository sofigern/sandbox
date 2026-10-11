from collections import Counter

import pytest
from hypothesis import given
from hypothesis import strategies as st

from biology.c1_exact_matching.c1_6_exercises.c1_6_11_composition_windows.composition_windows import (
    composition_windows,
    longest_within,
)


def fits(window: str, s: str) -> bool:
    """window uses no symbol more often than s holds it."""
    return not Counter(window) - Counter(s)


def windows_by_definition(t: str, s: str) -> list[int]:
    n = len(s)
    return [i for i in range(len(t) - n + 1) if Counter(t[i : i + n]) == Counter(s)]


def longest_by_definition(t: str, s: str) -> list[int]:
    return [
        max(k for k in range(len(t) - i + 1) if fits(t[i : i + k], s))
        for i in range(len(t) + 1)
    ]


texts = st.text(alphabet="abcd", max_size=12)
collections = st.text(alphabet="abc", max_size=5)


@given(texts, collections)
def test_windows_agree_with_the_definition(t, s):
    assert list(composition_windows(t, s)) == windows_by_definition(t, s)


@given(texts, collections)
def test_longest_agrees_with_the_definition(t, s):
    assert longest_within(t, s) == longest_by_definition(t, s)


@given(texts, collections)
def test_a_window_is_where_the_longest_fit_reaches_the_whole_collection(t, s):
    """Both questions are one scan: a rearrangement of s is a fit of length len(s)."""
    assert list(composition_windows(t, s)) == [
        i for i, k in enumerate(longest_within(t, s)) if k == len(s)
    ]


@pytest.mark.parametrize(
    ("t", "s", "offsets"),
    [
        ("abahgcabah", "abc", [5]),
        ("aab", "ab", [1]),
        ("aaaa", "aa", [0, 1, 2]),
        ("abc", "", [0, 1, 2, 3]),
        ("ab", "abc", []),
    ],
    ids=[
        "book_example",
        "counts_matter",
        "overlapping",
        "empty_collection",
        "collection_longer_than_text",
    ],
)
def test_window_examples(t, s, offsets):
    assert list(composition_windows(t, s)) == offsets
