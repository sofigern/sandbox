from hypothesis import given
from hypothesis import strategies as st

from biology.p1_1_naive_exact_matching import naive

# A two-letter alphabet makes matches, overlaps and near-misses common.
dna = st.text(alphabet="ab", max_size=12)


@given(p=dna, t=dna)
def test_yields_every_offset_where_pattern_occurs(p, t):
    expected = [i for i in range(len(t) + 1) if t.startswith(p, i)]
    assert list(naive(p, t)) == expected


def test_reports_overlapping_occurrences_up_to_the_last_offset():
    assert list(naive("aa", "aaaa")) == [0, 1, 2]


def test_empty_pattern_matches_at_every_offset_including_the_end():
    """The empty string occurs at each of the len(t) + 1 positions of t."""
    assert list(naive("", "abc")) == [0, 1, 2, 3]
