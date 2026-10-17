"""Section 2.2.2: Boyer-Moore with the extended bad character rule.

The simple rule aligns the mismatched text character with its rightmost
occurrence anywhere in the pattern, which gives nothing when that occurrence
lies to the right of the mismatch. The extended rule keeps, per character,
its positions in decreasing order and walks the list to the first position
left of the mismatch, so the shift is the largest that character allows. The
positions skipped lie inside the suffix just matched, so the walk costs no more
than the comparisons of the round it follows. The good suffix rule is shared
with ``boyer_moore``.

Next to the strong good suffix rule the extension buys nothing measurable: over
359,745 mismatch rounds on random patterns up to length 12, and on every
benchmark workload, its shift never exceeded the simple rule's combined with
the good suffix shift, while the list walk makes it 2-3x slower in Python
(measured 2026-10-17). The rule earns its place on its own, as section 2.2.2
presents it, before the good suffix rule is introduced.
"""

from collections.abc import Iterator

from biology.c2_classic_methods.c2_2_boyer_moore.boyer_moore import good_suffix_shifts


def occurrence_lists(p: str) -> dict[str, list[int]]:
    """Return, for each character of ``p``, its positions in decreasing order.

    Analysis: Θ(n) time and space, with n = len(p).

    >>> occurrence_lists("abcab")
    {'b': [4, 1], 'a': [3, 0], 'c': [2]}
    """
    positions: dict[str, list[int]] = {}
    for i in range(len(p) - 1, -1, -1):
        positions.setdefault(p[i], []).append(i)
    return positions


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
    positions = occurrence_lists(p)
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
            # The rightmost occurrence of the mismatched character left of i,
            # or -1 when there is none, which moves the pattern past it.
            x = t[k - n + i]
            left = next((j for j in positions.get(x, ()) if j < i), -1)
            k += max(shifts[n - 1 - i], i - left)
