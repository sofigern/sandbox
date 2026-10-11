import pytest
from hypothesis import given
from hypothesis import strategies as st

from biology.c1_exact_matching.c1_4_linear_preprocessing.preprocessing_compact import (
    z_values,
)
from biology.c1_exact_matching.c1_6_exercises.c1_6_5_leading_z_values.leading_z_values import (
    leading_z_values,
)


class Sym:
    """A character that counts how often it is compared."""

    comparisons = 0

    def __init__(self, c: str):
        self.c = c

    def __eq__(self, other):
        Sym.comparisons += 1
        return self.c == other.c


@given(st.text(alphabet="ab", min_size=2, max_size=12))
def test_matches_the_z_array_up_to_position_q_plus_one(s):
    z = z_values(s)
    assert leading_z_values(s) == z[: z[1] + 2]


@given(st.text(alphabet="ab", min_size=2, max_size=12))
def test_compares_only_to_find_q(s):
    """q matching comparisons, plus the mismatch unless the string ran out."""
    q = z_values(s)[1]
    Sym.comparisons = 0
    leading_z_values([Sym(c) for c in s])
    assert Sym.comparisons == min(q + 1, len(s) - 1)


@pytest.mark.parametrize(
    ("s", "values"),
    [
        ("aaaab", [5, 3, 2, 1, 0]),
        ("aaaa", [4, 3, 2, 1, 0]),
        ("ab", [2, 0]),
        ("a", [1, 0]),
        ("", [0]),
    ],
    ids=["run_then_break", "all_one_letter", "q_is_zero", "one_char", "empty"],
)
def test_examples(s, values):
    assert leading_z_values(s) == values
