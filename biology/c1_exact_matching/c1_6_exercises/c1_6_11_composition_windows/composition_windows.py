"""Exercise 1.6.11: substrings made of a given collection of symbols.

Gusfield, Algorithms on Strings, Trees and Sequences, section 1.6, exercise 11.

Let T be a text string of length m and S a collection of n symbols. The
problem is to find all substrings of T of length n composed of the symbols of
S. For example, let S = {a, b, c} and T = abahgcabah. Then caba is a substring
of T composed of symbols of S. Propose a solution running in O(m) time. The
method should also be able to find, for every position i, the length of the
longest substring of T starting at i and composed of symbols of S.

Reading: the English edition calls S a multiset, and the digression below
needs the counts, so here "composed of S" means "a rearrangement of S", and
the longest substring from i is the longest that uses no symbol more often
than S holds it. The book's own example caba fits only the looser reading, a
run of symbols that belong to S; the test oracles make the choice explicit.

Digression on deciphering a protein. The problem can help in deciphering a
protein of an organism whose genome is largely sequenced; simplest in
prokaryotes, whose genes are not interrupted by introns, so a protein is
encoded by one contiguous DNA segment, one codon per amino acid. Chemically
determining a protein's amino acid sequence is slow, costly and not wholly
reliable, while determining the collection S of its amino acids is relatively
simple. So: translate the genome's DNA into the amino acid alphabet (three
passes may be needed to find the right reading frame) to get a string T, then
find every substring of T of length |S| composed of the amino acids of S.
Those substrings are candidates for the protein's sequence, and a match also
locates the protein's gene in the long DNA string.
"""

from collections import Counter
from collections.abc import Iterator


def composition_windows(t: str, s: str) -> Iterator[int]:
    """Yield every 0-based offset where ``t[i:i + len(s)]`` is a rearrangement of ``s``.

    Analysis: Θ(m + n) time, Θ(n) space, with m = len(t) and n = len(s).

    >>> list(composition_windows("abahgcabah", "abc"))
    [5]
    """
    yield from (i for i, k in enumerate(longest_within(t, s)) if k == len(s))


def longest_within(t: str, s: str) -> list[int]:
    """Return, for every position i of ``t``, 0 <= i <= len(t), the length of the
    longest substring starting at i that uses no symbol more often than ``s``
    holds it; the end position fits 0.

    Analysis: Θ(m + n) time, Θ(n) space, with m = len(t) and n = len(s).

    >>> longest_within("abahgcabah", "abc")
    [2, 2, 1, 0, 0, 3, 2, 2, 1, 0, 0]
    """
    available = Counter(s)  # how many more of each symbol the window may still take
    fits = []
    j = 0  # first position not yet taken; it never moves back
    for i in range(len(t)):
        while j < len(t) and available[t[j]]:
            available[t[j]] -= 1
            j += 1
        fits.append(j - i)
        if j == i:  # t[i] itself did not fit: skip it, nothing to refund
            j += 1
        else:
            available[t[i]] += 1
    return [*fits, 0]
