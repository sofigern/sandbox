"""Exercise 1.6.8: parameterized matching (Baker).

Gusfield, Algorithms on Strings, Trees and Sequences, section 1.6, exercise 8.
The statement continues on page 36; the part below is page 35.

Baker [43] introduced the following matching problem, which she applied to
software maintenance: "The application tracks duplication in a large software
system. We want to find not only exact matches of code sections, but also
parameterized matches, in which one section turns into another under a
one-to-one renaming of parameters (that is, identifiers and constants)."

Now the formal statement. Let Σ and Π be two alphabets with no symbols in
common. Symbols of Σ are called tokens, symbols of Π parameters. A string may
consist of any mix of tokens and parameters. For example, if Σ is the upper
case English letters and Π the lower case ones, then XYabCaCXZddW is a legal
string over Σ and Π. Two strings S₁ and S₂ are called p-matching if and only
if:

a. every token of S₁ (or S₂) is aligned with the same token in S₂ (or S₁);
b. every parameter of S₁ (or S₂) is aligned with a parameter in S₂ (or S₁);
c. if for any parameter x one occurrence of x in S₁ (S₂) is aligned with a
   parameter y in S₂ (S₁), then every occurrence of x in S₁ (S₂) must be
   aligned with y in S₂ (S₁). In other words, aligning the parameters of S₁
   and S₂ defines a one-to-one correspondence between the parameter names of
   S₁ and those of S₂.

The strings S₁ = XYabCaCXZddbW and S₂ = XYdxCdCXZccxW p-match. Note that the
parameter a of S₁ maps to the parameter d of S₂, while the parameter d of S₁
maps to c of S₂; this does not contradict the definition.

In Baker's application a token stands for a part of the program that cannot
be changed, and a parameter for a program variable that may be renamed as long
as all its occurrences are renamed consistently. So if S₁ and S₂ p-match,
renaming the variables of S₁ to the corresponding names in S₂ makes the two
programs identical; if both are parts of a larger program, they can be
replaced by calls of one subroutine.

The most important p-matching problem is this. Given a text T and a pattern
P, both over Σ and Π, find all substrings of T that p-match P; naturally one
wants all occurrences in O(|P| + |T|) time. Let the function Zᵖ[i] of a string
S give the length of the longest string starting at position i that p-matches
a prefix of S. Show how to modify the Z algorithm to compute all values Zᵖ[i]
in O(|S|) time (the implementation details are a little trickier than for
Z[i], but ... continues on page 36).
"""

from collections.abc import Callable, Iterator


def prev_encoding(
    s: str, is_parameter: Callable[[str], bool] = str.islower
) -> list[str | int]:
    """Return Baker's prev encoding of ``s``: a token stays itself, a parameter
    becomes the distance back to its previous occurrence, 0 for a first one.

    Two strings p-match exactly when their encodings are equal.

    Analysis: Θ(n) time and space, with n = len(s).

    >>> prev_encoding("XYabCaCXZddbW")
    ['X', 'Y', 0, 0, 'C', 3, 'C', 'X', 'Z', 0, 1, 8, 'W']
    """
    encoding: list[str | int] = []
    last: dict[str, int] = {}
    for i, c in enumerate(s):
        if is_parameter(c):
            encoding.append(i - last.get(c, i))
            last[c] = i
        else:
            encoding.append(c)
    return encoding


def p_match(
    s1: str, s2: str, is_parameter: Callable[[str], bool] = str.islower
) -> bool:
    """Tell whether ``s1`` and ``s2`` p-match: tokens equal, parameters in bijection.

    Analysis: Θ(n) time and space, with n = len(s1).

    >>> p_match("XYabCaCXZddbW", "XYdxCdCXZccxW")
    True
    """
    return prev_encoding(s1, is_parameter) == prev_encoding(s2, is_parameter)


def pz_values(s: str, is_parameter: Callable[[str], bool] = str.islower) -> list[int]:
    """Return Zᵖ[k] for each position k of s, 0 <= k <= len(s): the length of the
    longest string at k that p-matches a prefix of s.

    The compact Z scan over the prev encoding. Equality of encodings is
    p-matching, except that a parameter whose previous occurrence lies before
    the window is a first occurrence as far as the window is concerned.

    Analysis: Θ(n) time, Θ(n) space, with n = len(s).

    >>> pz_values("aba")
    [3, 2, 1, 0]
    """
    n = len(s)
    encoding = prev_encoding(s, is_parameter)
    z = [n] + [0] * n
    l = r = 0
    for k in range(1, n + 1):
        if k < r and z[k - l] < r - k:
            z[k] = z[k - l]
            continue
        j = max(0, r - k)
        while k + j < n:
            y = encoding[k + j]
            if isinstance(y, int) and y > j:  # looks back past the window's start
                y = 0
            if encoding[j] != y:
                break
            j += 1
        z[k] = j
        l, r = k, k + j
    return z


def p_find(
    p: str, t: str, is_parameter: Callable[[str], bool] = str.islower
) -> Iterator[int]:
    """Yield every 0-based offset where a substring of ``t`` p-matches ``p``.

    Analysis: Θ(n + m) time, with n = len(t) and m = len(p).

    >>> list(p_find("Xab", "XcdXccXef"))
    [0, 6]
    """
    # The prefix of p + t is p, so a window of t p-matches p exactly when its
    # Zᵖ value is at least len(p). A window's checks never look back before
    # its own start, so nothing leaks across the boundary between p and t.
    m = len(p)
    z = pz_values(p + t, is_parameter)
    yield from (k - m for k in range(m, len(z)) if z[k] >= m)
