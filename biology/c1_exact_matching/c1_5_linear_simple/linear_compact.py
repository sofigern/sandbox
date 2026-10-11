from collections.abc import Iterator, Sequence


def prefix_lengths(p: str, t: str, z: Sequence[int], start: int = 0) -> Iterator[int]:
    """Yield, for each position k of ``t`` from ``start`` to ``len(t)``, how long a
    prefix of ``p`` begins at ``t[k]``: the Z values of ``p`` read across ``t``.

    The compact Z scan over two strings: start from what the Z-box already
    proves, extend by comparison, move the box if it grew. ``z`` must hold the Z
    values of ``p`` for every index below ``k - l`` by the time position ``k`` is
    reached; a complete Z array satisfies this, and so does :func:`z_values`,
    which appends each value as it consumes it.

    Analysis: Θ(n + m) time, O(1) space beyond ``z``, with n = len(t) and m = len(p).

    >>> list(prefix_lengths("aab", "aaab", [3, 1, 0, 0]))
    [2, 3, 1, 0, 0]
    """
    m, n = len(p), len(t)
    l = r = 0
    for k in range(start, n + 1):
        j = min(z[k - l], r - k) if k < r else 0
        while j < m and k + j < n and p[j] == t[k + j]:
            j += 1
        if k + j > r:
            l, r = k, k + j
        yield j


def z_values(s: str) -> list[int]:
    """Return Z[k] for each position k of s, 0 <= k <= len(s): the length of the
    longest substring at k that is a prefix of s.

    Z[0] is len(s) and Z[len(s)] is 0, the empty suffix. The Z array is
    :func:`prefix_lengths` of ``s`` against itself, reading the list it is
    still filling.

    Analysis: Θ(n) time, Θ(n) space, with n = len(s).

    >>> z_values("aabcaabxaaz")
    [11, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0, 0]
    """
    z = [len(s)]
    # Not `z.extend(...)`: the scan reads z while it grows, so each value must
    # be in place before the next one is asked for.
    for j in prefix_lengths(s, s, z, start=1):
        z.append(j)  # noqa: PERF402
    return z


def match(p: str, t: str) -> Iterator[int]:
    """Yield every 0-based offset where ``p`` occurs in ``t``, overlaps included.

    The positions of ``t`` where the prefix of ``p`` that matches is all of
    ``p``. Only ``p`` is preprocessed and offsets stream out as the scan
    reaches them; the position after the last character of ``t`` matches only
    the empty pattern.

    Analysis: Θ(n + m) time, Θ(m) space, with n = len(t) and m = len(p).

    >>> list(match("aa", "aaaa"))
    [0, 1, 2]
    """
    m = len(p)
    return (k for k, j in enumerate(prefix_lengths(p, t, z_values(p))) if j == m)
