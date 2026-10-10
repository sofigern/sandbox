from collections.abc import Iterator

from biology.c1_exact_matching.c1_4_linear_preprocessing.preprocessing_compact import (
    z_values,
)


def match(p: str, t: str) -> Iterator[int]:
    """Yield every 0-based offset where ``p`` occurs in ``t``, overlaps included.

    The Z scan over ``t`` with every shortcut the chapter found: candidates are
    only the offsets where ``p`` fits, found by ``str.find`` on its first
    character so the interpreter skips the rest at C speed; the Z-box, from the
    Z array of ``p`` alone, carries what is already known into each candidate;
    the inner loop has one bound. ``p[:1]`` as the search key makes the empty
    pattern a candidate at every position.

    Analysis: Θ(n + m) time, Θ(m) space, with n = len(t) and m = len(p).

    >>> list(match("aa", "aaaa"))
    [0, 1, 2]
    """
    m, n = len(p), len(t)
    z = z_values(p)
    first = p[:1]
    last = n - m
    l = r = 0
    k = t.find(first)
    while 0 <= k <= last:
        j = min(z[k - l], r - k) if k < r else 0
        while j < m and p[j] == t[k + j]:
            j += 1
        if k + j > r:
            l, r = k, k + j
        if j == m:
            yield k
        k = t.find(first, k + 1)
