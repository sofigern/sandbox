"""Exercise 1.6.13: can one protein's gene hide inside another's?

Gusfield, Algorithms on Strings, Trees and Sequences, section 1.6, exercise 13.

As noted in exercise 10, there are organisms (some viruses, for example) with
stretches of DNA that code not for one protein but for three, obtained under
different settings of the reading frame. So if each protein has n amino
acids, the DNA string encoding the three of them has length 3n + 2
nucleotides (the edition prints n + 2). A very compact encoding.

Research problem. Propose an algorithm for the following problem. Given a
protein string S₁ (over the amino acid alphabet) of length n and another
protein string S₂ of length m > n, determine whether a DNA string encoding S₂
can contain, at any point, a DNA substring encoding S₁. The encoding of S₁ may
start at any point of the DNA string for S₂, that is, in any reading frame of
that string. The problem is hard because of the degeneracy of the genetic code
and the freedom to use any reading frame.
"""

from collections import defaultdict
from collections.abc import Mapping

from biology.c1_exact_matching.c1_6_exercises.c1_6_10_reading_frames.reading_frames import (
    STANDARD_CODE,
)


def can_encode_within(
    s1: str, s2: str, code: Mapping[str, str] = STANDARD_CODE
) -> bool:
    """Tell whether some DNA string encoding ``s2`` contains, in some reading
    frame, a DNA substring encoding ``s1``.

    Analysis: Θ(nm) time, Θ(n) space, with n = len(s1) and m = len(s2); the
    genetic code is fixed, so its codons per amino acid are a constant.

    >>> can_encode_within("W", "MW")
    True
    """
    if not s1:
        return True
    codons = defaultdict(list)
    for codon, amino in code.items():
        codons[amino].append(codon)

    # A state is (j, carry): j amino acids of s1 matched so far, and the 0 to 2
    # nucleotides of the current codon of s2 not yet consumed by s1's frame.
    # reachable holds the states after the amino acids of s2 seen so far; the
    # fresh state is always among them, since a match may begin anywhere.
    fresh = (0, "")
    reachable = {fresh}
    for amino in s2:
        following = {fresh}
        for j, carry in reachable:
            for codon in codons[amino]:
                if (j, carry) == fresh:  # s1 may begin inside this codon
                    following.add((0, codon[1:]))
                    following.add((0, codon[2:]))
                read = carry + codon
                if code[read[:3]] == s1[j]:
                    if j + 1 == len(s1):
                        return True
                    following.add((j + 1, read[3:]))
        reachable = following
    return False
