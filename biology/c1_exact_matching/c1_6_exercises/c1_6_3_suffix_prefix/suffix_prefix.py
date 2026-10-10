"""Exercise 1.6.3: suffix-prefix matching.

Gusfield, Algorithms on Strings, Trees and Sequences, section 1.6, exercise 3.
Paraphrased from the English edition; check the wording against your copy.

Give an algorithm that takes two strings α and β, of lengths n and m, and
finds the longest suffix of α that exactly matches a prefix of β. The
algorithm should run in O(n + m) time.
"""

from biology.c1_exact_matching.c1_5_linear_simple.linear_compact import (
    prefix_lengths,
    z_values,
)


def suffix_prefix_overlap(a: str, b: str) -> int:
    """Return the length of the longest suffix of ``a`` that is a prefix of ``b``.

    Zero when no non-empty suffix qualifies; at most ``min(len(a), len(b))``.

    Analysis: Θ(n + m) time, with n = len(a) and m = len(b).

    >>> suffix_prefix_overlap("abcxyz", "xyzabc")
    3
    """
    z = z_values(b)
    return max(m for i, m in enumerate(prefix_lengths(b, a, z)) if (m + i) == len(a))
