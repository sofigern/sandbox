from hypothesis import given
from hypothesis import strategies as st

from biology.c1_exact_matching.c1_4_linear_preprocessing import preprocessing
from biology.c1_exact_matching.c1_6_exercises.c1_6_6_case_2b_without_comparison import (
    case_2b,
)


class Sym:
    """A character that counts how often it is compared."""

    comparisons = 0

    def __init__(self, c: str):
        self.c = c

    def __eq__(self, other):
        Sym.comparisons += 1
        return self.c == other.c


def comparisons(z_of, s: str) -> int:
    Sym.comparisons = 0
    z_of([Sym(c) for c in s])
    return Sym.comparisons


@given(st.text(alphabet="ab", max_size=20))
def test_computes_the_same_z_array(s):
    assert case_2b.z_values(s) == preprocessing.z_values(s)


@given(st.text(alphabet="ab", max_size=20))
def test_never_compares_more_than_the_case_split_form(s):
    assert comparisons(case_2b.z_values, s) <= comparisons(preprocessing.z_values, s)


def test_saves_comparisons_when_z_of_k_prime_exceeds_the_box():
    """In a run of one letter every Case 2b position has Z[k'] > |β|."""
    assert comparisons(case_2b.z_values, "aaaaaaab") < comparisons(
        preprocessing.z_values, "aaaaaaab"
    )
