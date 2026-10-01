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

## Running tests

`uv run --no-project --with pytest --with hypothesis pytest`
