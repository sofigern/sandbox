from collections import Counter

import pytest
from hypothesis import given
from hypothesis import strategies as st

from biology.c1_exact_matching.c1_6_exercises.c1_6_12_rectangular_composition import (
    rectangular_composition,
    rectangular_composition_numpy,
    rectangular_composition_sliding,
)

implementations = pytest.mark.parametrize(
    "rectangles",
    [
        rectangular_composition.rectangles,
        rectangular_composition_sliding.rectangles,
        rectangular_composition_numpy.rectangles,
    ],
    ids=["prefix_sums", "sliding", "numpy"],
)


def by_definition(grid, s):
    rows, cols = len(grid), len(grid[0]) if grid else 0
    if not s:  # the chapter's convention: an empty pattern matches at every position
        return [(r, c, 0, 0) for r in range(rows + 1) for c in range(cols + 1)]
    wanted = Counter(s)
    return [
        (r, c, height, width)
        for height in range(1, rows + 1)
        for width in range(1, cols + 1)
        for r in range(rows - height + 1)
        for c in range(cols - width + 1)
        if Counter("".join(row[c : c + width] for row in grid[r : r + height]))
        == wanted
    ]


@st.composite
def grid_and_collection(draw):
    rows, cols = draw(st.integers(1, 5)), draw(st.integers(1, 5))
    grid = [
        draw(st.text(alphabet="ab", min_size=cols, max_size=cols)) for _ in range(rows)
    ]
    s = draw(st.text(alphabet="ab", max_size=rows * cols))
    return grid, s


@given(grid_and_collection())
@implementations
def test_agrees_with_the_definition(rectangles, case):
    grid, s = case
    assert sorted(rectangles(grid, s)) == sorted(by_definition(grid, s))


@implementations
def test_finds_every_shape_of_the_right_area(rectangles):
    assert sorted(rectangles(["ab", "ba"], "ab")) == [
        (0, 0, 1, 2),
        (0, 0, 2, 1),
        (0, 1, 2, 1),
        (1, 0, 1, 2),
    ]


@implementations
def test_book_style_example(rectangles):
    assert sorted(rectangles(["abc", "cab", "bca"], "abcc")) == [(1, 0, 2, 2)]


@implementations
def test_ignores_symbols_outside_the_collection(rectangles):
    assert list(rectangles(["ab", "xy"], "ab")) == [(0, 0, 1, 2)]


@implementations
def test_empty_collection_matches_a_point_at_every_corner(rectangles):
    assert sorted(rectangles(["ab"], "")) == [
        (0, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 2, 0, 0),
        (1, 0, 0, 0),
        (1, 1, 0, 0),
        (1, 2, 0, 0),
    ]
