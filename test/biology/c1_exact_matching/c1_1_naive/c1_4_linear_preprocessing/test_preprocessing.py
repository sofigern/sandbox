import pytest
from hypothesis import given
from hypothesis import strategies as st

from biology.c1_exact_matching.c1_1_naive.c1_4_linear_preprocessing import (
    preprocessing,
    preprocessing_compact,
)

implementations = pytest.mark.parametrize(
    "z_of",
    [preprocessing.z_values, preprocessing_compact.z_values],
    ids=["gusfield", "compact"],
)


def z_by_definition(s: str) -> list[int]:
    """Z[k] is the length of the longest substring at k that is a prefix of s."""
    z = []
    for k in range(len(s)):
        n = 0
        while k + n < len(s) and s[n] == s[k + n]:
            n += 1
        z.append(n)
    return z


@implementations
@given(st.text(alphabet="ab", max_size=20))
def test_each_value_is_the_longest_prefix_match_at_that_position(z_of, s):
    assert z_of(s) == z_by_definition(s)


@implementations
def test_first_value_is_the_whole_string(z_of):
    assert z_of("abc")[0] == 3


@implementations
def test_empty_string_has_no_values(z_of):
    assert z_of("") == []


@implementations
def test_gusfield_example(z_of):
    """Gusfield, Algorithms on Strings, Trees and Sequences, section 1.3."""
    assert z_of("aabcaabxaaz") == [11, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0]


@implementations
def test_extends_a_z_box_reached_from_inside_another(z_of):
    """At k=3, k lies inside the Z-box [2, 5) and Z[1] reaches its end, so the
    match is extended past r by explicit comparison."""
    assert z_of("abababx") == [7, 0, 4, 0, 2, 0, 0]
