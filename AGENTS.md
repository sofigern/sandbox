# sandbox: agent instructions

Mykola's personal learning and exercise repo.
Conventions and lessons learned here are recorded in this file; skills specific to this repo go in `.claude/skills/`.
Prune an entry once it stops being true rather than annotating it.

## Layout

Module file names never start with a digit; use a letter prefix such as `p1_1_` so a plain import works (2026-10-01).
`test/` mirrors the source directories, and a test file repeats the name of what it tests (2026-10-01).
Either it repeats the module: `biology/p1_1_x.py` -> `test/biology/test_p1_1_x.py`.
Or, once the module's classes or functions each earn a test file, a directory named after the module holds one file per class or function: `test/biology/p2_1_x/test_BoyerMoore.py`.
The mirrored test directories have no `__init__.py` (a `test` package would shadow the stdlib one), so `pyproject.toml` sets `--import-mode=importlib` to let same-named test files coexist.

## Docstrings

Compact PEP 257 prose in reST, the way Hypothesis writes them, with no NumPy or Google sections (2026-10-01).
A one-line imperative summary, then an inline `Analysis:` line with asymptotic time and space (Unicode `Θ` is fine), then one doctest example.
Type hints carry parameter and return types, so the docstring never repeats them.
Results only, never derivations: a claim like `Θ(nm) worst case` belongs, the proof does not.
Example: `biology/p1_1_naive_exact_matching.py`.

## Running tests

`uv run pytest`.
Test tooling is a uv dev dependency group (`uv add --dev <pkg>`) installed into `.venv/`; `[tool.pyright]` in `pyproject.toml` points the editor at that venv, so imports resolve in nvim.
