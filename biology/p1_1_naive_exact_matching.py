from collections.abc import Iterator


def naive(p: str, t: str) -> Iterator[int]:
    """Yield every 0-based offset where ``p`` occurs in ``t``, overlaps included.

    Analysis: Θ(nm) time worst case, Θ(n) expected; O(1) space,
    with n = len(t) and m = len(p).

    >>> list(naive("aa", "aaaa"))
    [0, 1, 2]
    """
    for i in range(len(t) - len(p) + 1):
        for j in range(len(p)):
            if p[j] != t[i + j]:
                break
        else:
            yield i
