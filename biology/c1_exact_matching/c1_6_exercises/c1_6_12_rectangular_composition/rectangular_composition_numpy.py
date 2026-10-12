"""Exercise 1.6.12, the rectangular variant with numpy.

The task text is in ``rectangular_composition``. This is the same per-symbol
prefix-sum algorithm, with the tables built by two cumulative sums and every
position of a shape checked at once by array arithmetic, so the Python
interpreter runs per symbol and shape rather than per cell.
"""

from collections import Counter
from collections.abc import Iterator, Sequence

import numpy as np


def rectangles(grid: Sequence[str], s: str) -> Iterator[tuple[int, int, int, int]]:
    """Yield ``(row, col, height, width)`` for every rectangle of ``grid`` whose
    cells are a rearrangement of ``s``.

    Rectangles come in no particular order. An empty ``s`` is matched by a
    0 × 0 rectangle at each of the (rows + 1) × (cols + 1) corner positions,
    the chapter's convention that an empty pattern matches at every position.

    Analysis: Θ(R·C·d·k) time and Θ(R·C·k) space for an R × C grid, where k is
    the number of distinct symbols of s and d the number of rectangle shapes of
    area len(s) that fit the grid.

    >>> sorted(rectangles(["ab", "ba"], "ab"))
    [(0, 0, 1, 2), (0, 0, 2, 1), (0, 1, 2, 1), (1, 0, 1, 2)]
    """
    rows = len(grid)
    cols = 0 if not rows else len(grid[0])
    n = len(s)

    if not s:
        for r in range(rows + 1):
            for c in range(cols + 1):
                yield (r, c, 0, 0)
        return
    if not rows or not cols:
        return

    cells = np.array([list(row) for row in grid])
    wanted = Counter(s)
    # counts[x][i, j] is how many x the i × j top-left corner holds; the zero
    # row and column on top and left make the four-corner difference uniform.
    counts = {}
    for x in wanted:
        table = np.zeros((rows + 1, cols + 1), dtype=np.int64)
        table[1:, 1:] = (cells == x).cumsum(axis=0).cumsum(axis=1)
        counts[x] = table

    shapes = [(h, n // h) for h in range(1, n + 1) if n % h == 0]
    for height, width in shapes:
        if height > rows or width > cols:
            continue
        # hit[r, c] stays true while every symbol's count in the rectangle at
        # (r, c) equals the wanted one.
        hit = np.ones((rows - height + 1, cols - width + 1), dtype=bool)
        for x, k in wanted.items():
            t = counts[x]
            found = (
                t[height:, width:]
                - t[:-height, width:]
                - t[height:, :-width]
                + t[:-height, :-width]
            )
            hit &= found == k
        for r, c in np.argwhere(hit):
            yield (int(r), int(c), height, width)
