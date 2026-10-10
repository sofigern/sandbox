from collections.abc import Iterator

from biology.c1_exact_matching.c1_4_linear_preprocessing.preprocessing import z_values


def match(p: str, t: str) -> Iterator[int]:
    """Yield every 0-based offset where ``p`` occurs in ``t``, overlaps included.

    Z-based matching: ``p`` occurs at offset ``i`` exactly when the Z value of
    ``p + t`` at the position of ``t[i]`` is at least ``len(p)``. No separator
    is needed, and the position after the last character of ``t`` matches only
    the empty pattern.

    Analysis: Θ(n + m) time and space, with n = len(t) and m = len(p).

    >>> list(match("aa", "aaaa"))
    [0, 1, 2]
    """
    m = len(p)
    z = z_values(p + t)
    yield from (k - m for k in range(m, len(z)) if z[k] >= m)
