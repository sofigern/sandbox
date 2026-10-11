"""Exercise 1.6.6: Case 2b without the optional comparison.

Gusfield, Algorithms on Strings, Trees and Sequences, section 1.6, exercise 6.
In the chapter's notation k' = k - l and |β| = r - k, the part of the Z-box
from k to its end; in preprocessing.z_values they are ``k_`` and ``b_len``.

In Case 2b, when Z[k'] ≥ |β|, the Z algorithm compares characters explicitly
until a mismatch. That is a good way to organise the algorithm, but in fact
this optional comparison can be avoided in Case 2b. Show that if Z[k'] > |β|
then Z[k] = |β|, so no comparisons are needed; explicit comparison is needed
only when Z[k'] = |β|.

Answer: Write α = s[l:r] for the Z-box, so s[l:r] == s[0:r - l], and
β = s[k:r] for its part from k on, so |β| = r - k and β == s[k':k' + |β|] with
k' = k - l.

First, Z[k] >= |β|. Z[k'] > |β| means the substring at k' agrees with the
prefix of s for more than |β| symbols, in particular β == s[k':k' + |β|]
== s[0:|β|], so β is itself a prefix of s and the match at k runs at least to
r. (Were Z[k] < |β|, we would be in Case 2a with Z[k'] < |β| as well.)

Second, Z[k] <= |β|, which is only in question if a symbol s[r] after the box
exists. The box was set when Z[l] was computed as the longest prefix match at
l, so s[r] != s[r - l], or Z[l] would have been one larger and r one further
right. Now k' + |β| = (k - l) + (r - k) = r - l, so Z[k'] > |β| says the
symbol after the copy of β at k' equals the symbol after the prefix β:
s[r - l] == s[|β|]. Together, s[r] != s[|β|]: the symbol after the box differs
from the symbol the match at k would have to continue with, so the match at k
stops exactly at r and Z[k] = |β|.

Hence when Z[k'] > |β| no comparison is needed, and the explicit comparisons
of Case 2b are needed only when Z[k'] == |β|, where s[r - l] != s[|β|] and
nothing is known about s[r] against s[|β|].
"""

from biology.c1_exact_matching.c1_4_linear_preprocessing.preprocessing import (
    _match_length,
)


def z_values(s: str) -> list[int]:
    """Return Z[k] for each position k of s, 0 <= k <= len(s), comparing
    characters in Case 2b only when Z[k - l] equals r - k.

    Analysis: Θ(n) time, Θ(n) space, with n = len(s).

    >>> z_values("aabcaabxaaz")
    [11, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0, 0]
    """
    z = [0] * (len(s) + 1)
    z[0] = len(s)
    l = r = 0
    for k in range(1, len(s)):
        if k >= r:
            if n := _match_length(s, 0, k):
                l = k
                r = k + n
            z[k] = n
        else:
            k_ = k - l
            b_len = r - k
            if z[k_] < b_len:
                z[k] = z[k_]
            elif z[k_] > b_len:
                z[k] = b_len  # the symbol after the box cannot continue the match
            else:
                n = _match_length(s, b_len, r)
                z[k] = b_len + n
                l = k
                r = r + n
    return z
