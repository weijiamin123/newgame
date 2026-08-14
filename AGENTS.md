# Repository Guidelines

This repository is a single-file Python console game collection. `new_game.py` contains four mini-games (history quiz, "21" game, code-breaking, dungeon adventure) and uses only the Python standard library, with no build step or test suite yet.

## Project Structure & Module Organization

All source code lives in `new_game.py` at the repository root; there are no separate directories for tests or assets.

- Keep small games as classes in this file (`HistoryGame`, `Game_21`, `Game_chen`, `Down_city`) and shared menu logic in `game_menu()`.
- If the file grows past roughly 1000 lines, split each game into its own module under a `games/` package and keep `new_game.py` as the launcher.

## Build, Test, and Development Commands

No build step is required. Key commands:

- `python new_game.py` — start the interactive game menu.
- `python -m py_compile new_game.py` — syntax-check the module without running it.
- `python -m unittest discover tests` — run tests once a `tests/` directory exists.

## Coding Style & Naming Conventions

Follow PEP 8: 4-space indentation, two blank lines between top-level classes and functions, snake_case for methods and variables, and PascalCase for class names (`Game_21` is a legacy exception). Save source as UTF-8 without BOM. User-facing strings are Chinese and should keep the existing tone. Use comments only where intent is not obvious. No linter or formatter is configured; adopt `black` and `ruff` if the project grows.

## Testing Guidelines

No test framework is configured and no tests exist. When adding tests, use the standard library `unittest`, place them in `tests/`, and name files `test_*.py` and methods `test_<behavior>` (e.g., `tests/test_game_21.py` and `test_winning_move_takes_21`). Keep scoring and game rules in pure helper methods that can be tested without capturing `input()` or `print()`.

## Commit & Pull Request Guidelines

This directory is not yet a Git repository, so no commit history exists to follow. When version control is introduced, use Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`), keep subjects under 72 characters and imperative (for example, `fix: validate player input in Game_21`). Before opening a pull request, verify the game runs, describe what changed and why, link any related issue, and include output or screenshots for user-visible changes.

## Security & Configuration Tips

Never commit secrets or machine-specific paths. The games read arbitrary user input, so validate with `int()` checks or explicit constraints instead of trusting raw strings. Keep new features dependency-free unless there is a clear reason to add a package.
