"""Section 2.2: the Boyer-Moore algorithm.

Gusfield, Algorithms on Strings, Trees and Sequences, chapter 2, section 2.2.

The pattern is compared against the text from right to left. After a mismatch,
or a full occurrence, it moves right by the larger of two precomputed shifts.
The bad character rule aligns the mismatched text character with its rightmost
occurrence in the pattern. The strong good suffix rule aligns the matched
suffix with its rightmost other copy in the pattern that is preceded by a
different character, or, when there is none, aligns the longest prefix of the
pattern that is also a suffix of the matched part. Both tables come from the
N values of section 2.2.4, which are the Z values of the reversed pattern.
"""

from collections.abc import Iterator

from biology.c1_exact_matching.c1_5_linear_simple.linear_compact import z_values


def rightmost_positions(p: str) -> dict[str, int]:
    """Return R(x) of the bad character rule: the rightmost position of each
    character of ``p``. A character that is absent reads as -1.

    Analysis: Θ(n) time, Θ(|Σ|) space, with n = len(p).

    >>> rightmost_positions("abcab")
    {'a': 3, 'b': 4, 'c': 2}
    """
    return {x: i for i, x in enumerate(p)}


def good_suffix_shifts(p: str) -> list[int]:
    """Return the strong good suffix shifts of ``p``: ``shifts[i]`` is how far
    to move ``p`` after ``p[i + 1:]`` matched and ``p[i]`` did not, and
    ``shifts[-1]``, the slot for i = -1, how far after a full occurrence.

    A slot is the book's n - L'(i + 1), here n - 1 - L' with 0-based L', when
    a second copy of the matched suffix exists, and n - l'(i + 1) otherwise.
    Every shift is at least 1.

    Analysis: Θ(n) time and space, with n = len(p).

    >>> good_suffix_shifts("aabaa")
    [3, 3, 3, 1, 2, 3]
    """
    n = len(p)
    N = z_values(p[::-1])[::-1][1:]  # N[j]: longest suffix of p[:j + 1] that ends p
    shifts = [0] * (n + 1)
    # Weak rule (the book's l'): slide the longest border that fits under the
    # matched suffix; a border of length b is a j = b - 1 with N[j] == b.
    border = 0
    for i in range(n - 1, -2, -1):
        length = n - 1 - i  # of the matched suffix
        if 0 < length < n and N[length - 1] == length:
            border = length
        shifts[i] = n - border
    # Strong rule (the book's L'): a copy of the length-N[j] suffix ends at j and
    # serves the mismatch at n - 1 - N[j]; later j overwrite, so the rightmost wins.
    for j in range(n - 1):
        shifts[n - 1 - N[j]] = n - 1 - j
    return shifts


def match(p: str, t: str) -> Iterator[int]:
    """Yield every 0-based offset where ``p`` occurs in ``t``.

    Analysis: Θ(n + |Σ|) preprocessing, then Θ(nm) comparisons worst case and
    typically far fewer than m; Θ(n + |Σ|) space, with n = len(p), m = len(t).

    >>> list(match("aba", "abababa"))
    [0, 2, 4]
    """
    n, m = len(p), len(t)
    if not p:
        yield from range(m + 1)
        return
    rightmost = rightmost_positions(p)
    shifts = good_suffix_shifts(p)
    k = n  # the text position just past the current alignment
    while k <= m:
        i = n - 1
        while i >= 0 and p[i] == t[k - n + i]:
            i -= 1
        if i < 0:
            yield k - n
            k += shifts[-1]
        else:
            k += max(shifts[i], i - rightmost.get(t[k - n + i], -1))
