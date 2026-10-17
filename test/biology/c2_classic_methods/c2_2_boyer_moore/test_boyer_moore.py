from hypothesis import given
from hypothesis import strategies as st

from biology.c1_exact_matching.c1_5_linear_simple.linear_compact import z_values
from biology.c2_classic_methods.c2_2_boyer_moore.boyer_moore import (
    good_suffix_shifts,
    n_values,
    rightmost_positions,
)

patterns = st.text(alphabet="abc", min_size=1, max_size=9)


def n_by_definition(p):
    n = len(p)
    return [
        max(k for k in range(L + 1) if p[L - k : L] == p[n - k :] or k == 0)
        for L in range(n + 1)
    ]


def shifts_by_definition(p):
    """The strong good suffix rule spelled out by matched length k: the rightmost
    copy of the last k characters that ends earlier and is preceded by a different
    character, or is a prefix; failing that, the longest proper border that fits."""
    n = len(p)
    shifts = []
    for k in range(n + 1):
        suffix = p[n - k :]
        copies = [
            end
            for end in range(k, n)  # the copy is p[end - k:end]
            if p[end - k : end] == suffix
            and (end == k or p[end - k - 1] != p[n - k - 1])
        ]
        if copies and k < n:
            shifts.append(n - max(copies))
        else:
            borders = [b for b in range(1, min(n, k + 1)) if p[:b] == p[n - b :]]
            shifts.append(n - max(borders, default=0))
    return shifts


@given(patterns)
def test_n_values_agree_with_the_definition(p):
    assert n_values(p) == n_by_definition(p)


@given(patterns)
def test_n_values_are_the_reversed_z_values(p):
    assert n_values(p) == z_values(p[::-1])[::-1]


@given(patterns)
def test_shifts_agree_with_the_definition(p):
    assert good_suffix_shifts(p) == shifts_by_definition(p)


@given(patterns)
def test_every_shift_moves_the_pattern(p):
    assert min(good_suffix_shifts(p)) >= 1


def test_book_style_example():
    # Nothing matched: the nearest character other than the last a is the b at 2.
    # One a matched: its copy at 3 is preceded by b. Two matched, aa: copy at 1.
    # A full occurrence overlaps itself by the border aa.
    assert good_suffix_shifts("aabaa") == [2, 1, 3, 3, 3, 3]


def test_no_repeats_means_full_shifts():
    assert good_suffix_shifts("abcd") == [1, 4, 4, 4, 4]


def test_rightmost_position_wins():
    assert rightmost_positions("abcab") == {"a": 3, "b": 4, "c": 2}
