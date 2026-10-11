"""Exercise 1.6.9: match counts of all pairs of windows (Paul Horton).

Gusfield, Algorithms on Strings, Trees and Sequences, section 1.6, exercise 9.
The book introduces exercises 9 to 11 with: "The next three problems can be
solved without the Z algorithm or other special tools. They just need thought."

Given two strings of n characters each and an additional parameter k. Each
string has n − k + 1 substrings of length k, so there are Θ(n²) pairs of
substrings with one taken from the first string and the other from the second.
For a pair of substrings define the match count as the number of corresponding
characters that agree when the two length-k substrings are aligned. Compute
the match counts for all Θ(n²) pairs. Clearly this can be done in O(kn²)
operations (character comparisons and arithmetic). But a sensible organisation
of the computation brings it down to O(n²) operations.
"""


def match_counts(a: str, b: str, k: int) -> list[list[int]]:
    """Return ``counts[i][j]``, the number of positions where ``a[i:i + k]`` and
    ``b[j:j + k]`` agree, for every pair of length-k windows.

    Analysis: Θ(n²) time and space, with n = len(a) = len(b), independent of k.

    >>> match_counts("abc", "abd", 2)
    [[2, 0], [0, 1]]
    """
    n = len(a)
    # agree[i][j]: agreeing pairs on the diagonal ending just before (i, j)
    agree = [[0] * (n + 1) for _ in range(n + 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            agree[i + 1][j + 1] = agree[i][j] + (x == y)
    windows = range(n - k + 1)
    return [[agree[i + k][j + k] - agree[i][j] for j in windows] for i in windows]
