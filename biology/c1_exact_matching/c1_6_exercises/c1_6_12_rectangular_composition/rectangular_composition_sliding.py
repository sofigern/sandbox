"""Exercise 1.6.12, the rectangular variant by sliding a deficit counter.

The task text is in ``rectangular_composition``. Here each shape is scanned
with one window per band, moved one strip at a time: the strip that leaves is
refunded to the deficit counter and the strip that enters is taken from it,
the way ``composition_windows`` of exercise 11 does in one dimension. A band
runs along the longer side of the shape, so a strip has the shorter side's
cells.
"""

from collections import Counter, deque
from collections.abc import Iterable, Iterator, Sequence


def rectangles(grid: Sequence[str], s: str) -> Iterator[tuple[int, int, int, int]]:
    """Yield ``(row, col, height, width)`` for every rectangle of ``grid`` whose
    cells are a rearrangement of ``s``.

    Rectangles come in no particular order. An empty ``s`` is matched by a
    0 × 0 rectangle at each of the (rows + 1) × (cols + 1) corner positions,
    the chapter's convention that an empty pattern matches at every position.

    Analysis: Θ(R·C·Σ min(h, w)) time over the d shapes h × w of area n = len(s)
    that fit the R × C grid, so at most Θ(R·C·d·√n); Θ(n) space.

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

    wanted = Counter(s)
    shapes = [(h, n // h) for h in range(1, n + 1) if n % h == 0]
    for height, width in shapes:
        if height <= width:  # bands of rows slid rightwards; a strip is a column
            for r in range(rows - height + 1):
                band = grid[r : r + height]
                strips = ([row[c] for row in band] for c in range(cols))
                for c in _windows(strips, width, wanted):
                    yield (r, c, height, width)
        else:  # bands of columns slid downwards; a strip is a row segment
            for c in range(cols - width + 1):
                strips = (grid[r][c : c + width] for r in range(rows))
                for r in _windows(strips, height, wanted):
                    yield (r, c, height, width)


def _windows(
    strips: Iterable[Iterable[str]], length: int, wanted: Counter[str]
) -> Iterator[int]:
    """Yield the index of the first strip of every run of ``length`` consecutive
    strips whose cells together are a rearrangement of ``wanted``.

    Analysis: Θ(total cells) time, Θ(window cells) space.

    >>> list(_windows(["ab", "cd", "ab", "ba"], 2, Counter("abcd")))
    [0, 1]
    """
    deficit = Counter(wanted)  # per symbol, how many the window still lacks
    missing = sum(wanted.values())  # cells the window still lacks in total
    window: deque[Iterable[str]] = deque()
    for i, strip in enumerate(strips):
        window.append(strip)
        for x in strip:
            if deficit[x] > 0:
                missing -= 1
            deficit[x] -= 1
        if len(window) > length:
            for x in window.popleft():
                deficit[x] += 1
                if deficit[x] > 0:
                    missing += 1
        if missing == 0:  # impossible before the window holds `length` strips
            yield i - length + 1
