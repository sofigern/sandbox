import pytest
from hypothesis import given
from hypothesis import strategies as st

from biology.c1_exact_matching.c1_6_exercises.c1_6_8_parameterized_matching import (
    parameterized_matching,
    parameterized_matching_numba,
    parameterized_matching_numpy,
    parameterized_matching_re,
)
from biology.c1_exact_matching.c1_6_exercises.c1_6_8_parameterized_matching.parameterized_matching import (
    p_match,
)

# numba compiles on first use, which would trip Hypothesis's per-example deadline.
parameterized_matching_numba.pz_values("Xa")

finders = pytest.mark.parametrize(
    "p_find",
    [
        parameterized_matching.p_find,
        parameterized_matching_re.p_find,
        parameterized_matching_numba.p_find,
        parameterized_matching_numpy.p_find,
    ],
    ids=["z_values", "regex", "numba", "numpy"],
)
z_implementations = pytest.mark.parametrize(
    "pz_values",
    [parameterized_matching.pz_values, parameterized_matching_numba.pz_values],
    ids=["python", "numba"],
)

# Three parameter letters: with only two, "differs from the previous one" fixes a
# parameter completely and whole classes of bugs stay invisible.
strings = st.text(alphabet="ABabc", max_size=8)


def p_match_by_definition(s1: str, s2: str) -> bool:
    if len(s1) != len(s2):
        return False
    forward, backward = {}, {}
    for x, y in zip(s1, s2, strict=True):
        if x.islower() != y.islower():
            return False
        if not x.islower():
            if x != y:
                return False
        elif forward.setdefault(x, y) != y or backward.setdefault(y, x) != x:
            return False
    return True


@given(strings, strings)
def test_p_match_agrees_with_the_definition(s1, s2):
    assert p_match(s1, s2) == p_match_by_definition(s1, s2)


@given(strings, st.dictionaries(st.sampled_from("ab"), st.sampled_from("abc")))
def test_p_match_decides_a_renaming_by_whether_it_is_one_to_one(s1, renaming):
    """s2 is s1 with its parameters renamed, so the two p-match exactly when
    the renaming is injective on the parameters s1 actually uses."""
    s2 = "".join(renaming.get(c, c) if c.islower() else c for c in s1)
    used = {c for c in s1 if c.islower()}
    injective = len({renaming.get(c, c) for c in used}) == len(used)
    assert p_match(s1, s2) is injective


@pytest.mark.parametrize(
    ("s1", "s2", "expected"),
    [
        ("XYabCaCXZddbW", "XYdxCdCXZccxW", True),
        ("XYa", "XZa", False),
        ("aab", "abb", False),
        ("ab", "aa", False),
        ("aA", "Aa", False),
        ("", "", True),
    ],
    ids=[
        "book_pair",
        "token_differs",
        "one_param_to_two",
        "two_params_to_one",
        "token_vs_param",
        "empty",
    ],
)
def test_p_match_examples(s1, s2, expected):
    assert p_match(s1, s2) is expected


@z_implementations
@given(strings)
def test_pz_values_agree_with_the_definition(pz_values, s):
    expected = [
        max(
            n
            for n in range(len(s) - k + 1)
            if p_match_by_definition(s[k : k + n], s[:n])
        )
        for k in range(len(s) + 1)
    ]
    assert pz_values(s) == expected


@finders
@given(st.text(alphabet="ABabc", max_size=4), st.text(alphabet="ABabc", max_size=10))
def test_p_find_reports_every_window_that_p_matches(p_find, p, t):
    expected = [
        i
        for i in range(len(t) - len(p) + 1)
        if p_match_by_definition(t[i : i + len(p)], p)
    ]
    assert list(p_find(p, t)) == expected
