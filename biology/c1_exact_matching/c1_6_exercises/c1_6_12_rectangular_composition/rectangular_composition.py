"""Exercise 1.6.12: the two-dimensional version.

Gusfield, Algorithms on Strings, Trees and Sequences, section 1.6, exercise 12.

Consider a two-dimensional version of the previous problem. The input is a
two-dimensional text (say, a filled-in crossword) and a collection of symbols.
The problem is to find in the text a two-dimensional substructure that uses
the symbols of the collection. How can it be done? A simple variant of the
problem is when the structure is rectangular.

General form: a connected set of cells whose symbols are a rearrangement of
the collection. On the grid graph this is the Graph Motif problem, NP-complete
in general (Lacroix, Fernandes, Sagot 2006; from memory, not checked for grids
specifically), so no linear scan is expected; a backtracking search that grows
a connected region cell by cell and prunes on the remaining multiset is the
straightforward answer. The code below takes the rectangular variant, where
the shape is any rectangle of any height and width, with one prefix-sum table
per symbol; ``rectangular_composition_sliding`` solves the same variant with a
sliding window and constant memory per collection size.
"""

from collections import Counter
from collections.abc import Iterator, Sequence


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

    # counts[x][i][j] is how many x the i × j top-left corner holds, so a
    # rectangle's count of x is a sum and difference of four corner entries.
    # Only the symbols of s are counted: a rectangle of area n that holds the
    # wanted number of each of them has no cell left for anything else.
    wanted = Counter(s)
    counts = {x: [[0] * (cols + 1) for _ in range(rows + 1)] for x in wanted}
    for i, row in enumerate(grid, 1):
        for j, cell in enumerate(row, 1):
            for x, t in counts.items():
                t[i][j] = t[i - 1][j] + t[i][j - 1] - t[i - 1][j - 1] + (cell == x)
    targets = [(counts[x], k) for x, k in wanted.items()]

    # Every divisor h of n gives the shape (h, n // h); its mirror image shows
    # up on its own when the loop reaches n // h.
    shapes = [(h, n // h) for h in range(1, n + 1) if n % h == 0]
    for height, width in shapes:
        for r in range(rows - height + 1):
            for c in range(cols - width + 1):
                if all(
                    t[r + height][c + width]
                    - t[r][c + width]
                    - t[r + height][c]
                    + t[r][c]
                    == k
                    for t, k in targets
                ):
                    yield (r, c, height, width)
