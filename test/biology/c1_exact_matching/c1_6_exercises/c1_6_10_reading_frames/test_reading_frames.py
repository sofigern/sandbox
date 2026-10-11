from collections.abc import Mapping

import pytest
from hypothesis import given
from hypothesis import strategies as st

from biology.c1_exact_matching.c1_6_exercises.c1_6_10_reading_frames.reading_frames import (
    STANDARD_CODE,
    translate_frames,
)


def by_definition(
    dna: str, code: Mapping[str, str] = STANDARD_CODE
) -> tuple[str, str, str]:
    return tuple(
        "".join(code[dna[i : i + 3]] for i in range(frame, len(dna) - 2, 3))
        for frame in range(3)
    )


class CountingDNA:
    """A DNA string that counts every symbol read, a slice counting its length."""

    def __init__(self, dna: str):
        self.dna, self.reads = dna, 0

    def __len__(self):
        return len(self.dna)

    def __getitem__(self, item):
        self.reads += (
            len(range(*item.indices(len(self.dna)))) if isinstance(item, slice) else 1
        )
        return self.dna[item]

    def __iter__(self):
        for c in self.dna:
            self.reads += 1
            yield c


class CountingCode(dict):
    """A genetic code that counts every look-up."""

    lookups = 0

    def __getitem__(self, key):
        CountingCode.lookups += 1
        return super().__getitem__(key)

    def get(self, key, default=None):
        CountingCode.lookups += 1
        return super().get(key, default)


@given(st.text(alphabet="atcg", max_size=20))
def test_agrees_with_the_definition(dna):
    assert translate_frames(dna) == by_definition(dna)


@given(st.text(alphabet="atcg", max_size=20))
def test_reads_each_symbol_once_and_looks_up_each_codon_once(dna):
    counted, code = CountingDNA(dna), CountingCode(STANDARD_CODE)
    CountingCode.lookups = 0
    translate_frames(counted, code)
    assert counted.reads <= len(dna)
    assert CountingCode.lookups <= max(len(dna) - 2, 0)


@given(st.text(alphabet="atcg", max_size=12))
def test_uses_the_code_it_is_given(dna):
    """A code that spells each codon out loud, so a frame reads as its codons."""
    spelled_out = {codon: codon.upper() for codon in STANDARD_CODE}
    assert translate_frames(dna, spelled_out) == by_definition(dna, spelled_out)


@pytest.mark.parametrize(
    ("dna", "frames"),
    [
        ("atggacgga", ("MDG", "WT", "GR")),
        ("tttgtt", ("FV", "L", "C")),
        ("at", ("", "", "")),
        ("", ("", "", "")),
    ],
    ids=["book_example", "book_codons", "too_short", "empty"],
)
def test_examples(dna, frames):
    assert translate_frames(dna) == frames
