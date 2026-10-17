from hypothesis import given
from hypothesis import strategies as st

from biology.c2_classic_methods.c2_2_boyer_moore.boyer_moore import (
    good_suffix_shifts,
    rightmost_positions,
)


def shifts_by_definition(p):
    """The strong good suffix rule spelled out: for the matched suffix p[i + 1:],
    the rightmost copy ending at j that is preceded by a different character, or
    is a prefix; failing that, the longest proper border that fits under it."""
    n = len(p)
    shifts = []
    for i in range(-1, n):
        suffix = p[i + 1 :]
        copies = [
            j
            for j in range(len(suffix) - 1, n - 1)
            if p[j + 1 - len(suffix) : j + 1] == suffix
            and (j + 1 - len(suffix) == 0 or p[j - len(suffix)] != p[i])
        ]
        if copies and i >= 0:
            shifts.append(n - 1 - max(copies))
        else:
            borders = [
                b for b in range(1, min(n, len(suffix) + 1)) if p[:b] == p[n - b :]
            ]
            shifts.append(n - max(borders, default=0))
    return shifts[1:] + shifts[:1]  # slot -1 last, as the implementation lays it out


@given(st.text(alphabet="abc", min_size=1, max_size=9))
def test_shifts_agree_with_the_definition(p):
    assert good_suffix_shifts(p) == shifts_by_definition(p)


@given(st.text(alphabet="abc", min_size=1, max_size=9))
def test_every_shift_moves_the_pattern(p):
    assert min(good_suffix_shifts(p)) >= 1


def test_book_style_example():
    # Suffix a has a copy at 3 preceded by b; aa has a copy at 1; the first
    # comparison looks for the nearest character other than a, the b at 2;
    # a full occurrence overlaps itself by the border aa.
    assert good_suffix_shifts("aabaa") == [3, 3, 3, 1, 2, 3]


def test_no_repeats_means_full_shifts():
    assert good_suffix_shifts("abcd") == [4, 4, 4, 1, 4]


def test_rightmost_position_wins():
    assert rightmost_positions("abcab") == {"a": 3, "b": 4, "c": 2}
