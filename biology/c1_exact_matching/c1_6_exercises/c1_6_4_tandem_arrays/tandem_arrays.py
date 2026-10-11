"""Exercise 1.6.4: tandem arrays.

Gusfield, Algorithms on Strings, Trees and Sequences, section 1.6, exercise 4.
Paraphrased from the English edition; check the wording against your copy.

A substring α of a string S is called a tandem array of β (the base) if α
consists of more than one consecutive copy of β. For example, if
S = xyzabcabcabcabcpq, then α = abcabcabcabc is a tandem array of β = abc.
Note that S also contains a tandem array of abcabc, that is, a tandem array
with a longer base. A maximal tandem array is one that cannot be extended to
the left or to the right. Given the base β, a tandem array of β in S can be
described by two numbers (s, k): where it starts in S and how many times β is
repeated. Suppose S has length n and β has length m. Give an O(n + m)-time
algorithm that finds all maximal tandem arrays of β in S.

Then give an O(n) algorithm that, from S and β, finds every maximal tandem
array of β and outputs the pair (s, k) for each occurrence. Since maximal
tandem arrays with a given base can overlap, a naive algorithm gives only an
O(n²) bound.
"""

from biology.c1_exact_matching.c1_5_linear_simple.linear_compact import (
    prefix_lengths,
    z_values,
)


def maximal_tandem_arrays(s: str, base: str) -> list[tuple[int, int]]:
    """Return every maximal tandem array of ``base`` in ``s`` as ``(start, copies)``.

    A tandem array is at least two consecutive copies of ``base``; it is
    maximal when neither the copy before it nor the one after it is also
    ``base``. Arrays come in no particular order.

    Analysis: Θ(n + m) time, Θ(m) space, with n = len(s) and m = len(base).

    >>> maximal_tandem_arrays("xyzabcabcabcabcpq", "abc")
    [(3, 4)]

    >>> maximal_tandem_arrays("abaababaaba", "aba")
    [(0, 2), (5, 2)]
    """
    m = len(base)
    if m == 0:
        raise ValueError("base must not be empty")

    # Consecutive copies of base sit at positions congruent modulo m, so a run
    # is identified by its phase i % m and one counter per phase is enough.
    copies = [0] * m
    arrays = []
    for i, matched in enumerate(prefix_lengths(base, s, z_values(base))):
        phase = i % m
        if matched == m:
            copies[phase] += 1
            continue
        if copies[phase] > 1:
            arrays.append((i - copies[phase] * m, copies[phase]))
        copies[phase] = 0
    return arrays
