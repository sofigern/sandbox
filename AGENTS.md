# sandbox: agent instructions

Mykola's personal learning and exercise repo.
Conventions and lessons learned here are recorded in this file; skills specific to this repo go in `.claude/skills/`.
Prune an entry once it stops being true rather than annotating it.

## Layout

Course structure is nested packages, one per level, each with an `__init__.py` (2026-10-01):
chapter `c1_exact_matching/`, section inside it `c1_1_naive/`, sub-step inside the section `c1_1_1_naive_improvements/`.
A folder name is `c` plus its full dotted number with `_` separators, then the topic; the leading letter keeps it importable.
Nesting, not siblings: as siblings `c1_1_1_x` would sort above `c1_1_x`, because `_` sorts after digits. No zero padding and no letter suffixes (Mykola's call).
Inside a level, modules have plain topic names: `c1_1_naive/naive.py`, `c1_1_1_naive_improvements/naive_improvements.py`.
`test/` mirrors the source directories, and a test file repeats the name of what it tests (2026-10-01).
Either it repeats the module: `biology/c1_exact_matching/c1_1_naive/naive.py` -> `test/biology/c1_exact_matching/c1_1_naive/test_naive.py`.
Or, once the module's classes or functions each earn a test file, a directory named after the module holds one file per class or function: `test/.../c2_1_boyer_moore/boyer_moore/test_BoyerMoore.py`.
The mirrored test directories have no `__init__.py` (a `test` package would shadow the stdlib one), so `pyproject.toml` sets `--import-mode=importlib` to let same-named test files coexist.

## Docstrings

Compact PEP 257 prose in reST, the way Hypothesis writes them, with no NumPy or Google sections (2026-10-01).
A one-line imperative summary, then an inline `Analysis:` line with asymptotic time and space (Unicode `Θ` is fine), then one doctest example.
Type hints carry parameter and return types, so the docstring never repeats them.
Results only, never derivations: a claim like `Θ(nm) worst case` belongs, the proof does not.
Example: `biology/c1_exact_matching/c1_1_naive/naive.py`.

## Running tests

`uv run pytest` runs the tests and the doctest examples in source docstrings (`--doctest-modules`).
`uv run ruff check .` and `uv run ruff format .` lint and format; rules are the defaults plus `I`, `UP`, `B` in `[tool.ruff.lint]`.
Test tooling is a uv dev dependency group (`uv add --dev <pkg>`) installed into `.venv/`; `[tool.pyright]` in `pyproject.toml` points the editor at that venv, so imports resolve in nvim.
