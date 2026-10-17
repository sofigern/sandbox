"""Section 2.2: the Boyer-Moore algorithm.

Gusfield, Algorithms on Strings, Trees and Sequences, chapter 2, section 2.2.

The pattern is compared against the text from right to left. After a mismatch,
or a full occurrence, it moves right by the larger of two precomputed shifts.
The bad character rule aligns the mismatched text character with its rightmost
occurrence in the pattern. The strong good suffix rule aligns the matched
suffix with its rightmost other copy in the pattern that is preceded by a
different character, or, when there is none, aligns the longest prefix of the
pattern that is also a suffix of the matched part. Both halves of that rule
come from the N values of section 2.2.4, the Z algorithm run from the right.
"""

from collections.abc import Iterator


def rightmost_positions(p: str) -> dict[str, int]:
    """Return R(x) of the bad character rule: the rightmost position of each
    character of ``p``. A character that is absent reads as -1.

    Analysis: Θ(n) time, Θ(|Σ|) space, with n = len(p).

    >>> rightmost_positions("abcab")
    {'a': 3, 'b': 4, 'c': 2}
    """
    return {x: i for i, x in enumerate(p)}


def n_values(p: str) -> list[int]:
    """Return N[L] for 0 <= L <= len(p): the length of the longest suffix of
    ``p[:L]`` that is also a suffix of ``p``.

    The Z algorithm mirrored: prefixes are scanned from the longest down, and
    the match found so far that reaches furthest left, ``p[lo:hi]``, is a copy
    of the pattern's suffix of the same length, so a prefix ending inside it
    starts from the value of its mirror image in that suffix.

    Analysis: Θ(n) time and space, with n = len(p).

    >>> n_values("aabaa")
    [0, 1, 2, 0, 1, 5]
    """
    n = len(p)
    N = [0] * n + [n]  # the whole pattern is its own suffix
    lo = hi = n  # no match yet
    for L in range(n - 1, 0, -1):
        # p[:L] ends inside the box at L - 1, whose mirror ends p[:n - hi + L];
        # that value holds as far as the box reaches, L - lo characters.
        j = min(N[n - hi + L], L - lo) if L > lo else 0
        while j < L and p[L - 1 - j] == p[n - 1 - j]:
            j += 1
        N[L] = j
        if L - j < lo:
            lo, hi = L - j, L
    return N


def good_suffix_shifts(p: str) -> list[int]:
    """Return the strong good suffix shifts of ``p``: ``shifts[k]`` is how far
    to move ``p`` after its last k characters matched and the character before
    them did not; ``shifts[len(p)]`` is the move after a full occurrence.

    A slot is the book's n - L'(i) when a second copy of the matched suffix
    exists and n - l'(i) otherwise, for the mismatch position i = n - 1 - k.
    Every shift is at least 1.

    Analysis: Θ(n) time and space, with n = len(p).

    >>> good_suffix_shifts("aabaa")
    [2, 1, 3, 3, 3, 3]
    """
    n = len(p)
    N = n_values(p)
    shifts = [0] * (n + 1)
    # Weak rule (the book's l'): slide the longest border, a prefix that is also
    # a suffix, that fits under the k matched characters; p[:k] is a border
    # exactly when N[k] == k, and the whole pattern does not count.
    border = 0
    for k in range(n + 1):
        if 0 < k < n and N[k] == k:
            border = k
        shifts[k] = n - border
    # Strong rule (the book's L'): the suffix of length N[L] has another copy
    # ending at L - 1, preceded by a different character or by nothing; later
    # L overwrite, so the rightmost copy wins. N[L] == 0 fills the slot for a
    # mismatch on the first comparison with the nearest character that differs
    # from the last one.
    for L in range(1, n):
        shifts[N[L]] = n - L
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
            k += shifts[n]
        else:
            k += max(shifts[n - 1 - i], i - rightmost.get(t[k - n + i], -1))
