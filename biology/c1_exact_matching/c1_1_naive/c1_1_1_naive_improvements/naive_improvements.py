from collections.abc import Iterator


def naive_jump(p: str, t: str) -> Iterator[int]:
    """Yield every 0-based offset where ``p`` occurs in ``t``, overlaps included.

    Naive matching that jumps: each alignment notes the first later position
    holding ``p[0]`` and resumes there, skipping alignments that cannot match
    and the first character it has already checked.

    Analysis: Θ(nm) time worst case, Θ(n) expected; O(1) space,
    with n = len(t) and m = len(p).

    >>> list(naive_jump("aa", "aaaa"))
    [0, 1, 2]
    """
    if not p:
        yield from range(len(t) + 1)
        return

    first = p[0]
    last = len(t) - len(p)
    i = 0
    start = 0  # 1 when t[i] == p[0] is already known, so that check is skipped
    while i <= last:
        next_i = None
        for j in range(start, len(p)):
            c = t[i + j]
            if next_i is None and j > 0 and c == first:
                next_i = i + j
            if c != p[j]:
                break
        else:
            yield i

        if next_i is not None:
            i, start = next_i, 1
        else:
            i, start = i + 1, 0
