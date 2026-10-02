from collections.abc import Callable, Iterator
from itertools import islice

import pytest
from hypothesis import given
from hypothesis import strategies as st

from biology.c1_exact_matching.c1_1_naive.c1_1_1_naive_improvements.naive_improvements import (
    naive_jump,
)
from biology.c1_exact_matching.c1_1_naive.naive import naive

# Every exact-matching algorithm in the chapter must honour the same contract.
implementations = pytest.mark.parametrize(
    "find", [naive, naive_jump], ids=["naive", "naive_jump"]
)


@st.composite
def pattern_and_text(draw):
    """Draw a pattern, and a text glued from copies of it, its prefixes and filler.

    Near-misses, where an alignment matches a prefix and then fails, are where
    skip-ahead matchers go wrong; uniform random text rarely produces them.
    """
    p = draw(st.text(alphabet="ab", min_size=1, max_size=6))
    prefix = st.integers(0, len(p)).map(lambda k: p[:k])
    filler = st.text(alphabet="ab", max_size=3)
    t = "".join(draw(st.lists(st.one_of(st.just(p), prefix, filler), max_size=5)))
    return p, t


def occurrences(find: Callable[[str, str], Iterator[int]], p: str, t: str) -> list[int]:
    """Collect the offsets, capped one past the len(t) + 1 that can exist."""
    return list(islice(find(p, t), len(t) + 2))


@implementations
@given(pattern_and_text())
def test_yields_every_offset_where_pattern_occurs(find, pt):
    p, t = pt
    expected = [i for i in range(len(t) + 1) if t.startswith(p, i)]
    assert occurrences(find, p, t) == expected


@implementations
def test_reports_overlapping_occurrences_up_to_the_last_offset(find):
    assert occurrences(find, "aa", "aaaa") == [0, 1, 2]


@implementations
def test_reports_a_match_starting_inside_a_failed_alignment(find):
    """At offset 0, "aab" fails on t[2], yet an occurrence starts at offset 1."""
    assert occurrences(find, "aab", "aaab") == [1]


@implementations
def test_empty_pattern_matches_at_every_offset_including_the_end(find):
    """The empty string occurs at each of the len(t) + 1 positions of t."""
    assert occurrences(find, "", "abc") == [0, 1, 2, 3]
