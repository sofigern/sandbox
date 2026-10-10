import pytest
from hypothesis import given
from hypothesis import strategies as st

from biology.c1_exact_matching.c1_6_exercises.c1_6_1_cyclic_shift.cyclic_shift import (
    is_cyclic_shift,
)


@given(st.text(alphabet="ab", max_size=12), st.integers(0, 12))
def test_rotating_a_string_by_any_amount_gives_a_cyclic_shift(b, k):
    k = k % len(b) if b else 0
    assert is_cyclic_shift(b[k:] + b[:k], b)


@given(st.text(alphabet="ab", max_size=8), st.text(alphabet="ab", max_size=8))
def test_agrees_with_the_definition(a, b):
    by_definition = len(a) == len(b) and any(
        a == b[k:] + b[:k] for k in range(len(b) + 1)
    )
    assert is_cyclic_shift(a, b) == by_definition


def test_gusfield_example():
    assert is_cyclic_shift("defabc", "abcdef")


@pytest.mark.parametrize(
    ("a", "b"),
    [("abcdef", "abcdef"), ("", ""), ("aaaa", "aaaa")],
    ids=["same_string", "both_empty", "all_one_letter"],
)
def test_every_string_is_a_cyclic_shift_of_itself(a, b):
    assert is_cyclic_shift(a, b)


@pytest.mark.parametrize(
    ("a", "b"),
    [("abcde", "abcdef"), ("aabb", "abab"), ("abcdef", "abcdeg"), ("a", "")],
    ids=["shorter", "same_letters_other_order", "one_letter_differs", "empty_other"],
)
def test_rejects_strings_that_are_not_rotations(a, b):
    assert not is_cyclic_shift(a, b)
