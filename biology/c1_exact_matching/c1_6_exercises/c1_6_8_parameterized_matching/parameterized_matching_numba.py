"""Exercise 1.6.8 compiled: the same encoding and Z scan, run through numba.

Nothing algorithmic changes against ``parameterized_matching``; the loops are
the same lines. numba compiles them to machine code on first call (about half
a second, then cached on disk), so this is the pure-Python solution's own
speed ceiling rather than a different method. Tokens become negative codes
and parameters their back distance, so the encoding is one integer array.
"""

import string
from collections.abc import Iterator

import numpy as np
from numba import njit


def _codes(s: str) -> np.ndarray:
    return np.frombuffer(s.encode("utf-32-le"), dtype=np.uint32).astype(np.int64)


@njit(cache=True)
def _encode(codes: np.ndarray, is_parameter: np.ndarray) -> np.ndarray:
    n = codes.size
    encoding = np.empty(n, np.int64)
    last = np.full(codes.max() + 1 if n else 1, -1, np.int64)
    for i in range(n):
        c = codes[i]
        if is_parameter[i]:
            encoding[i] = 0 if last[c] < 0 else i - last[c]
            last[c] = i
        else:
            encoding[i] = -1 - c
    return encoding


@njit(cache=True)
def _pz(encoding: np.ndarray) -> np.ndarray:
    n = encoding.size
    z = np.zeros(n + 1, np.int64)
    z[0] = n
    l = r = 0
    for k in range(1, n + 1):
        if k < r and z[k - l] < r - k:
            z[k] = z[k - l]
            continue
        j = max(0, r - k)
        while k + j < n:
            y = encoding[k + j]
            if y > j:  # looks back past the window's start
                y = 0
            if encoding[j] != y:
                break
            j += 1
        z[k] = j
        l, r = k, k + j
    return z


def prev_encoding(s: str, parameters: str = string.ascii_lowercase) -> np.ndarray:
    """Return the prev encoding as an int64 array: tokens negative, parameters
    the distance back to their previous occurrence, 0 for a first one.

    >>> prev_encoding("XYab").tolist()
    [-89, -90, 0, 0]
    """
    codes = _codes(s)
    is_parameter = np.isin(codes, np.array([ord(c) for c in parameters], np.int64))
    return _encode(codes, is_parameter)


def pz_values(s: str, parameters: str = string.ascii_lowercase) -> list[int]:
    """Return Zᵖ[k] for each position k of s, 0 <= k <= len(s).

    Analysis: Θ(n) time, Θ(n) space, with n = len(s).

    >>> pz_values("aba")
    [3, 2, 1, 0]
    """
    return _pz(prev_encoding(s, parameters)).tolist()


def p_find(p: str, t: str, parameters: str = string.ascii_lowercase) -> Iterator[int]:
    """Yield every 0-based offset where a substring of ``t`` p-matches ``p``.

    Analysis: Θ(n + m) time, with n = len(t) and m = len(p).

    >>> list(p_find("Xab", "XcdXccXef"))
    [0, 6]
    """
    m = len(p)
    z = _pz(prev_encoding(p + t, parameters))
    return iter(np.flatnonzero(z[m:] >= m).tolist())
