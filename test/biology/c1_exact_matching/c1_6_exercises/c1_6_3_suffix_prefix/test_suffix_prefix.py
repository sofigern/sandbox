import pytest
from hypothesis import given
from hypothesis import strategies as st

from biology.c1_exact_matching.c1_6_exercises.c1_6_3_suffix_prefix.suffix_prefix import (
    suffix_prefix_overlap,
)


def by_definition(a: str, b: str) -> int:
    return max(
        k for k in range(min(len(a), len(b)) + 1) if b.startswith(a[len(a) - k :])
    )


@given(st.text(alphabet="ab", max_size=10), st.text(alphabet="ab", max_size=10))
def test_agrees_with_the_definition(a, b):
    assert suffix_prefix_overlap(a, b) == by_definition(a, b)


@given(
    st.text(alphabet="ab", max_size=6),
    st.text(alphabet="ab", max_size=6),
    st.text(alphabet="ab", min_size=1, max_size=4),
)
def test_a_shared_piece_glued_on_both_sides_is_found(left, right, piece):
    """The overlap of left + piece and piece + right is at least len(piece)."""
    assert suffix_prefix_overlap(left + piece, piece + right) >= len(piece)


@pytest.mark.parametrize(
    ("a", "b", "overlap"),
    [
        ("abcxyz", "xyzabc", 3),
        ("abc", "abc", 3),
        ("abc", "abcdef", 3),
        ("xyzabc", "abc", 3),
        ("aaa", "aaaa", 3),
        ("abc", "xyz", 0),
        ("", "abc", 0),
        ("abc", "", 0),
        ("abab", "ababab", 4),
    ],
    ids=[
        "book_style",
        "equal",
        "a_is_prefix_of_b",
        "b_is_suffix_of_a",
        "all_one_letter",
        "disjoint",
        "empty_a",
        "empty_b",
        "periodic",
    ],
)
def test_examples(a, b, overlap):
    assert suffix_prefix_overlap(a, b) == overlap
