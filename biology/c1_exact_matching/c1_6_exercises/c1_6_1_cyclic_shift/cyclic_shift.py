"""Exercise 1.6.1: cyclic shift.

Gusfield, Algorithms on Strings, Trees and Sequences, section 1.6, exercise 1.

Use the existence of a linear-time exact matching algorithm to solve the
following problem in linear time. Given two strings α and β, determine whether
α is a cyclic shift of β (that is, α and β have the same length and α consists
of a suffix of β glued to a prefix of β). For example, defabc is a cyclic shift
of abcdef. This is a classic problem with a very elegant solution.
"""


def is_cyclic_shift(a: str, b: str) -> bool:
    """Tell whether ``a`` is a cyclic shift of ``b``.

    That is, the two have the same length and ``a`` is a suffix of ``b`` glued
    to a prefix of ``b``; every string is a cyclic shift of itself.

    Analysis: Θ(n) time, with n = len(b).

    >>> is_cyclic_shift("defabc", "abcdef")
    True
    """
    return len(a) == len(b) and b in a + a
