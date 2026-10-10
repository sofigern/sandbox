from collections.abc import Iterator

from biology.c1_exact_matching.c1_4_linear_preprocessing.preprocessing import z_values


def _match_length(p: str, i: int, t: str, j: int) -> int:
    """Count how far p[i:] and t[j:] agree."""
    n = 0
    while (i + n) < len(p) and (n + j) < len(t) and p[i + n] == t[j + n]:
        n += 1
    return n


def match(p: str, t: str) -> Iterator[int]:
    """Yield every 0-based offset where ``p`` occurs in ``t``, overlaps included.

    Z-based matching without concatenation: the Z-box runs over ``t`` while the
    reused values come from the Z array of ``p`` alone, so only ``p`` is
    preprocessed and offsets stream out as the scan reaches them. Every
    position of ``t`` is a candidate, including the one after its last
    character, which matches only the empty pattern.

    Analysis: Θ(n + m) time, Θ(m) space, with n = len(t) and m = len(p).

    >>> list(match("aa", "aaaa"))
    [0, 1, 2]
    """
    z = z_values(p)
    l = r = 0
    for k in range(len(t) + 1):
        if k >= r:
            n = _match_length(p, 0, t, k)
            if n:
                l = k
                r = k + n
        else:
            k_ = k - l
            b_len = r - k
            if z[k_] < b_len:
                n = z[k_]
            else:
                n = b_len + _match_length(p, b_len, t, r)
                l = k
                r = k + n
        if n == len(p):
            yield k
