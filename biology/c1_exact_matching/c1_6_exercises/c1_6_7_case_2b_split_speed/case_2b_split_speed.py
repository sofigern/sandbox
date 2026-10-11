"""Exercise 1.6.7: does splitting Case 2b make the Z algorithm faster?

Gusfield, Algorithms on Strings, Trees and Sequences, section 1.6, exercise 7.

If Case 2b of the Z algorithm is split into two subcases, Z[k'] strictly
greater than |β| and Z[k'] equal to |β|, does that speed up the algorithm? You
must count all operations, not only character comparisons.

Measured, not argued: ``case_2b.z_values`` (the split, id ``gusfield_split``)
sits beside ``preprocessing.z_values`` (id ``gusfield``) in
``benchmark/biology/c1_exact_matching/c1_4_linear_preprocessing/bench_preprocessing.py``,
run with ``uv run pytest benchmark -k z_values``; comparison counts come from
the counting symbols in exercise 1.6.6's tests.

Answer: Yes, and for a reason that only shows up when all operations are
counted. On 100,000 characters (one machine, 2026-10-10, median ms):

    workload      gusfield  gusfield_split   character comparisons saved
    all_same         15.47            9.94   none: the box reaches the end
    periodic         11.25            9.48   none
    fibonacci         8.93            8.91   none
    random_dna       10.47            9.97   13 of 24,620 (first 20,000 chars)

The number of character comparisons barely moves, because when Z[k'] > |β|
the chapter's Case 2b calls _match_length and the very first comparison fails
(or none happens at all, when the box already touches the end of s). What the
split removes is that call: its argument setup, the loop entry, the return.
On a run of one symbol every position from 2 on is this case, so the call is
skipped 99,998 times and the time drops by a third; on random text the case
is rare and the gain is within noise. The split never costs anything, since
the extra ``elif`` replaces a call rather than adding to it.

Counting only comparisons, as the chapter's analysis does, would call the two
forms equal; counting operations, the split is faster by up to 36% in CPython,
where a function call is far dearer than a comparison. In C the gap would be
smaller but of the same sign.
"""
