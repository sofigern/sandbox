"""Exercise 1.6.5: the Z values that follow from Z[1].

Gusfield, Algorithms on Strings, Trees and Sequences, section 1.6, exercise 5.
The book indexes from 1, so its Z₂ is Z[1] here and its Z_{q+2} is Z[q + 1].

If the Z algorithm finds that Z[1] = q > 0, then all the values Z[2], ...,
Z[q], Z[q + 1] can be obtained directly, with no further comparisons and
without running the main body of the Z algorithm. Justify this claim in
detail.

Answer: Z[1] = q says that the prefix of length q equals the same prefix
shifted by one, s[0:q] == s[1:q + 1], so s[0] == s[1], s[1] == s[2], and so on
up to s[q - 1] == s[q]: the first q + 1 symbols are all the same symbol. The
symbol s[q + 1], if it exists, differs from them, or the shift would have
matched one symbol further and q would be larger. So for 1 <= k <= q the
substring at k runs through the same symbol for exactly q + 1 - k positions
and then meets the different one, giving Z[k] = q + 1 - k, and the substring
at q + 1 starts with the different symbol, giving Z[q + 1] = 0. All q + 2
values follow from q alone, with no further comparisons.
"""


def leading_z_values(s: str) -> list[int]:
    """Return Z[0] .. Z[q + 1] of ``s``, where q = Z[1], comparing only to find q.

    For a string shorter than two characters, all of its Z values.

    Analysis: Θ(q) time and space, with q = Z[1] of s.

    >>> leading_z_values("aaaab")
    [5, 3, 2, 1, 0]
    """
    if not s:
        return [0]  # one position, no Z[1] to read q from
    q = 0
    while q < len(s) - 1 and s[q] == s[q + 1]:
        q += 1
    # s[0] .. s[q] are one symbol and s[q + 1], if any, is another, so the
    # run at k lasts q + 1 - k symbols for 1 <= k <= q, and Z[q + 1] is 0.
    return [len(s), *range(q, 0, -1), 0]
