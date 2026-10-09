def _match_length(s: str, i: int, j: int) -> int:
    """Count how far s[i:] and s[j:] agree, for i < j."""
    n = 0
    while j + n < len(s) and s[i + n] == s[j + n]:
        n += 1
    return n


def z_values(s: str) -> list[int]:
    """Return Z[k], the length of the longest substring at k that is a prefix of s.

    Z[0] is len(s) by convention. Gusfield's case split: a position outside the
    Z-box is compared from scratch, one inside reuses Z[k - l] and compares only
    past the box's end.

    Analysis: Θ(n) time, Θ(n) space, with n = len(s).

    >>> z_values("aabcaabxaaz")
    [11, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0]
    """
    if not s:
        return []

    z = [len(s)]
    l = r = 0
    for k in range(1, len(s)):
        if k >= r:
            if n := _match_length(s, 0, k):
                l = k
                r = k + n
            z.append(n)
        else:
            k_ = k - l
            b_len = r - k
            if z[k_] < b_len:
                z.append(z[k_])
            else:
                n = _match_length(s, b_len, r)
                z.append(b_len + n)
                l = k
                r = r + n
    return z
