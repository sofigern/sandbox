"""Exercise 1.6.10: translating a DNA string in all three reading frames.

Gusfield, Algorithms on Strings, Trees and Sequences, section 1.6, exercise 10.

A DNA molecule can be viewed as a string over the four-symbol alphabet
{a, t, c, g} (nucleotides), and a protein as a string over a twenty-symbol
alphabet (amino acids). A gene, physically embedded in a DNA molecule, usually
encodes the amino acid sequence of a particular protein, as follows. Starting
from a certain point of the DNA string, every three consecutive DNA symbols
are recoded into one amino acid symbol of the protein string, so three
nucleotides specify one amino acid. Such a triple is called a codon, and the
full correspondence of codons to amino acids the genetic code. For example,
the codon ttt specifies the amino acid phenylalanine (abbreviated to the single
symbol F of the amino acid alphabet), and gtt specifies valine (V). Since there
are 4³ = 64 possible triples and only twenty amino acids, two or more triples
may be codons for the same amino acid, and some triples may not be codons at
all. Both happen: leucine, for example, is encoded by six different codons.

Suppose a DNA string of n nucleotides is given, but the correct "reading frame"
is unknown: it is not known whether the correct division into codons starts
at the first, the second or the third nucleotide. Each such "frame shift"
potentially yields its own amino acid string. (Indeed, genes are known in
which each of the three readings not only encodes a string over the amino
acid alphabet but corresponds to a functional protein, a different one in each
case!) The amino acid string for each of the three frames is required. For
example, take the string atggacgga. The first frame has three complete codons,
atg, gac and gga, which the genetic code maps to Met, Asp and Gly. The second
frame has two complete codons, tgg and acg, encoding Trp and Thr. The third
frame has two complete codons, gga and cgg, encoding Gly and Arg.

The problem is to perform these three translations with the fewest checks of
DNA symbols and the fewest index operations (an amino acid is found from a
codon in a table holding the genetic code). Clearly the three translations
can be done with 3n checks of DNA symbols and 3n index operations. Propose a
method that finds the solution with at most n symbol checks and n index
operations.

Hint. The notion of a finite automaton may be useful here, though not
necessary, if you know the terminology.
"""

from collections.abc import Mapping
from itertools import product

# The standard genetic code, one-letter amino acids, "*" for a stop codon.
_AMINO_ACIDS = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
STANDARD_CODE: Mapping[str, str] = {
    "".join(codon): amino
    for codon, amino in zip(product("tcag", repeat=3), _AMINO_ACIDS, strict=True)
}


def translate_frames(
    dna: str, code: Mapping[str, str] = STANDARD_CODE
) -> tuple[str, str, str]:
    """Return the amino acid strings of the three reading frames of ``dna``, each
    built from its complete codons only.

    Analysis: Θ(n) time, with at most n symbol checks and n table look-ups.

    >>> translate_frames("atggacgga")
    ('MDG', 'WT', 'GR')
    """
    frames: tuple[list[str], list[str], list[str]] = ([], [], [])
    window = dna[:2]  # the automaton's state: the last two nucleotides read
    for i, nucleotide in enumerate(dna[2:]):
        window = window[-2:] + nucleotide
        frames[i % 3].append(
            code[window]
        )  # the codon ending here belongs to frame i % 3
    return "".join(frames[0]), "".join(frames[1]), "".join(frames[2])
