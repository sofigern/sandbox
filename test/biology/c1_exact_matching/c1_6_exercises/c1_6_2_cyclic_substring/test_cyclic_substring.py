import pytest
from hypothesis import given
from hypothesis import strategies as st

from biology.c1_exact_matching.c1_6_exercises.c1_6_2_cyclic_substring.cyclic_substring import (
    is_cyclic_substring,
)


def rotations(b: str) -> list[str]:
    return [b[k:] + b[:k] for k in range(len(b))] or [""]


@given(st.text(alphabet="ab", max_size=8), st.text(alphabet="ab", max_size=8))
def test_agrees_with_the_definition(a, b):
    by_definition = len(a) <= len(b) and any(a in r for r in rotations(b))
    assert is_cyclic_substring(a, b) == by_definition


@given(
    st.text(alphabet="ab", min_size=1, max_size=10),
    st.integers(0, 9),
    st.integers(0, 9),
)
def test_any_window_of_the_cyclic_string_is_a_substring(b, start, length):
    """A window that starts anywhere on the circle and runs at most len(b) characters."""
    start, length = start % len(b), min(length, len(b))
    assert is_cyclic_substring((b + b)[start : start + length], b)


@pytest.mark.parametrize(
    "a",
    ["gcac", "cat", "ccatggca", "accatggc", ""],
    ids=["wraps_round_the_end", "inside", "a_rotation", "itself", "empty"],
)
def test_substrings_of_the_figure_1_6_string(a):
    assert is_cyclic_substring(a, "accatggc")


@pytest.mark.parametrize(
    ("a", "b"),
    [("cag", "accatggc"), ("ababab", "ab"), ("a", ""), ("accatggcac", "accatggc")],
    ids=[
        "absent",
        "longer_than_the_circle_though_periodic",
        "empty_circle",
        "longer_than_the_circle",
    ],
)
def test_rejects_strings_that_are_not_substrings_of_any_rotation(a, b):
    assert not is_cyclic_substring(a, b)
