from collections.abc import Iterator


def match(p: str, t: str) -> Iterator[int]:
    """Yield every 0-based offset where ``p`` occurs in ``t``, overlaps included.

    The baseline: ``str.find`` resumed one past each hit, so the search itself
    runs in the interpreter's C code and Python only loops over the hits.

    Analysis: Θ(nm) time worst case, O(1) space, with n = len(t) and m = len(p);
    CPython's ``find`` mixes several algorithms and is linear on most inputs.

    >>> list(match("aa", "aaaa"))
    [0, 1, 2]
    """
    i = t.find(p)
    while i != -1:
        yield i
        i = t.find(p, i + 1)
