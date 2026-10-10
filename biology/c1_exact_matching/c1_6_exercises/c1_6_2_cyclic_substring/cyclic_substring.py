"""Exercise 1.6.2: substring of a cyclic string.

Gusfield, Algorithms on Strings, Trees and Sequences, section 1.6, exercise 2.

Similarly to exercise 1, design an algorithm that determines in linear time
whether a string α is a substring of a cyclic string β. A cyclic string of
length n is a string in which the n-th character is considered to precede the
first (Fig. 1.6). Another way to picture the problem: let β̄ be the linear
string obtained from β by starting at the first character and ending at the
n-th. Then α is a substring of the cyclic string β if and only if α is a
substring of some cyclic shift of β̄.

Fig. 1.6: the cyclic string β whose linear string β̄ is accatggc.

Digression on cyclic strings in DNA. The two problems are mainly exercises on
the existence of linear-time algorithms; we know of no serious biological
problem where they would be used. Still, circular DNA is typical and
important: bacterial and mitochondrial DNA are usually circular, as are
plasmids, the additional small double-stranded circular DNA molecules; even
some eukaryotes, such as yeast, have plasmids besides their nuclear DNA.
"""

from biology.c1_exact_matching.c1_4_linear_preprocessing.preprocessing_compact import (
    z_values,
)


def is_cyclic_substring(a: str, b: str) -> bool:
    """Tell whether ``a`` is a substring of the cyclic string ``b``.

    That is, ``a`` is a substring of some cyclic shift of ``b``; it may wrap
    from the last character of ``b`` round to the first, but it is never longer
    than ``b``. The empty string is a substring of every cyclic string.

    Analysis: Θ(n + m) time, with n = len(b) and m = len(a).

    >>> is_cyclic_substring("gcac", "accatggc")
    True
    """
    n = len(a)
    if n > len(b):
        return False  # a substring of a cyclic shift is never longer than the circle
    if n == 0:
        return True
    z = z_values(a)

    l = r = k = 0
    while k < len(b):
        m = 0
        if k < r:
            m = min(z[k - l], r - k)
        while m < n and a[m] == b[(m + k) % len(b)]:
            m += 1
        if (m + k) > r:
            l, r = k, k + m
        if m == n:
            return True
        k += 1
    return False
