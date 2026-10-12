from itertools import product

import pytest
from hypothesis import given
from hypothesis import strategies as st

from biology.c1_exact_matching.c1_6_exercises.c1_6_10_reading_frames.reading_frames import (
    STANDARD_CODE,
)
from biology.c1_exact_matching.c1_6_exercises.c1_6_13_overlapping_genes.overlapping_genes import (
    can_encode_within,
)

CODONS = {}
for codon, amino in STANDARD_CODE.items():
    CODONS.setdefault(amino, []).append(codon)


def encodings(protein):
    return ["".join(choice) for choice in product(*(CODONS[a] for a in protein))]


def by_definition(s1, s2):
    """Enumerate every DNA encoding of both; feasible only for tiny proteins."""
    inner = encodings(s1)
    return any(e1 in e2 for e2 in encodings(s2) for e1 in inner)


# Amino acids with few codons keep the enumeration small: M, W have one; F, Y, H two; I three.
proteins = st.text(alphabet="MWFYHI", min_size=1, max_size=3)


@given(proteins, proteins)
def test_agrees_with_the_definition(s1, s2):
    assert can_encode_within(s1, s2) == by_definition(s1, s2)


@pytest.mark.parametrize(
    ("s1", "s2", "expected"),
    [("W", "MW", True), ("M", "WW", False), ("MW", "MW", True), ("Y", "FF", False)],
    ids=["present_in_frame", "absent", "whole_protein", "no_frame_shift_gives_y"],
)
def test_examples(s1, s2, expected):
    assert can_encode_within(s1, s2) is expected
