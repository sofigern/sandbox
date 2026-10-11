"""Exercise 1.6.8 vectorised: the naive window test, one array operation.

Every window of the text is compared with the pattern at once: a view of all
windows over the prev encoding, the clamp applied column by column, equality
reduced along each row. It is the O(nm) naive method, but each of its nm steps
is a vectorised C operation, and the clamped copy of the windows costs O(nm)
memory. Zᵖ values are a sequential recurrence and have no such form, so this
module provides only ``p_find``.
"""

import string
from collections.abc import Iterator

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def prev_encoding(s: str, parameters: str = string.ascii_lowercase) -> np.ndarray:
    """Return the prev encoding as an int64 array: tokens negative, parameters
    the distance back to their previous occurrence, 0 for a first one.

    One pass per parameter letter, each a vectorised scan of the text.

    >>> prev_encoding("XYabCaCXZddbW").tolist()
    [-89, -90, 0, 0, -68, 3, -68, -89, -91, 0, 1, 8, -88]
    """
    codes = np.frombuffer(s.encode("utf-32-le"), dtype=np.uint32).astype(np.int64)
    encoding = -1 - codes
    for c in parameters:
        at = np.flatnonzero(codes == ord(c))
        if at.size:
            encoding[at[0]] = 0
            encoding[at[1:]] = np.diff(at)
    return encoding


def p_find(p: str, t: str, parameters: str = string.ascii_lowercase) -> Iterator[int]:
    """Yield every 0-based offset where a substring of ``t`` p-matches ``p``.

    Analysis: Θ(nm) time and space, with n = len(t) and m = len(p).

    >>> list(p_find("Xab", "XcdXccXef"))
    [0, 6]
    """
    m, n = len(p), len(t)
    if m == 0:
        return iter(range(n + 1))
    if m > n:
        return iter(())
    windows = sliding_window_view(prev_encoding(t, parameters), m)
    clamped = np.where(windows > np.arange(m), 0, windows)
    hits = (clamped == prev_encoding(p, parameters)).all(axis=1)
    return iter(np.flatnonzero(hits).tolist())
