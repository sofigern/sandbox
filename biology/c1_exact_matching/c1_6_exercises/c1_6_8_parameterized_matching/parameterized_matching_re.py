"""Exercise 1.6.8 by regular expression: the pattern becomes a regex.

A p-match of a fixed pattern is expressible in ``re``: a token is a literal, a
parameter's first occurrence captures one parameter character that no earlier
capture holds, and a repeated parameter is a backreference. The search then
runs in the regex engine. It is not linear in the worst case, like the naive
method, but the constant is C's.
"""

import re
import string
from collections.abc import Iterator


def p_regex(p: str, parameters: str = string.ascii_lowercase) -> re.Pattern[str]:
    """Compile ``p`` into a lookahead that matches wherever ``p`` p-matches.

    ``parameters`` is the parameter alphabet; every other character is a token.

    >>> p_regex("Xaba", parameters="ab").pattern
    '(?=X(?P<p0>[ab])(?!(?P=p0))(?P<p1>[ab])(?P=p0))'
    """
    char_class = f"[{re.escape(parameters)}]"
    groups: dict[str, str] = {}
    parts = []
    for c in p:
        if c not in parameters:
            parts.append(re.escape(c))
        elif c in groups:
            parts.append(f"(?P={groups[c]})")
        else:
            not_seen = "".join(f"(?!(?P={g}))" for g in groups.values())
            groups[c] = f"p{len(groups)}"
            parts.append(f"{not_seen}(?P<{groups[c]}>{char_class})")
    return re.compile(f"(?={''.join(parts)})")


def p_find(p: str, t: str, parameters: str = string.ascii_lowercase) -> Iterator[int]:
    """Yield every 0-based offset where a substring of ``t`` p-matches ``p``.

    Analysis: O(nm) time worst case, with n = len(t) and m = len(p); linear on
    text where most attempts fail early.

    >>> list(p_find("Xab", "XcdXccXef"))
    [0, 6]
    """
    return (m.start() for m in p_regex(p, parameters).finditer(t))
