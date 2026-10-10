def z_values(s: str) -> list[int]:
    """Return Z[k], the length of the longest substring at k that is a prefix of s.

    Z[0] is len(s) by convention. One path for every position: start from what
    the Z-box already proves, extend by comparison, move the box if it grew.

    Analysis: Θ(n) time, Θ(n) space, with n = len(s).

    >>> z_values("aabcaabxaaz")
    [11, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0]
    """
    n = len(s)
    z = [0] * n
    if n:
        z[0] = n
    l = r = 0  # the Z-box s[l:r] that reaches furthest right so far
    for k in range(1, n):
        if k < r:
            # s[k:r] equals s[k - l:r - l], so reuse what is known, up to r.
            z[k] = min(z[k - l], r - k)
        while k + z[k] < n and s[z[k]] == s[k + z[k]]:
            z[k] += 1
        if k + z[k] > r:
            l, r = k, k + z[k]
    return z
