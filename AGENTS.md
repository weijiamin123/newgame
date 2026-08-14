# Repository Guidelines

This repository is a FastAPI web game hub with four browser games: history quiz, "21" game, code-breaking, and dungeon adventure.

## Project Structure & Module Organization

- `app.py`: FastAPI app that exposes the JSON API and hosts the frontend.
- `game_engines/`: pure Python state machines used by the API; no `input()` or `print()`.
- `static/`: `index.html`, `style.css`, `app.js` single-page frontend.
- `tests/`: pytest tests for engines and the API.
- `requirements.txt`: runtime and test dependencies.

## Build, Test, and Development Commands

- `pip install -r requirements.txt` — install dependencies.
- `python -m uvicorn app:app --reload --port 5000` — start the web app.
- `python -m pytest` — run all tests.

## Coding Style & Naming Conventions

Follow PEP 8 for Python: 4-space indentation, snake_case functions and variables, PascalCase classes. JavaScript uses 2-space indentation and `const` by default. Save source as UTF-8. User-facing strings are Chinese and should keep the existing tone. Use comments only where intent is not obvious. No formatter is configured; adopt `black` and `ruff` for Python if the project grows.

## Testing Guidelines

Use `pytest`. Engine tests live in `tests/test_<engine>.py`, API tests in `tests/test_api.py`. Name test methods `test_<behavior>` (for example, `test_invalid_guess_rejected`). Engines must stay free of `input()` and `print()` so rules can be tested without console interaction; dice randomness in the dungeon engine is controlled via monkeypatching `roll_dice`.

## Commit & Pull Request Guidelines

Use Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`), keep subjects under 72 characters and imperative (for example, `feat: add grab 21 engine`). Before opening a pull request, verify the web app runs, run the full test suite, and include output or screenshots for user-visible changes.

## Security & Configuration Tips

Never commit secrets or machine-specific paths. API sessions live in memory and reset when the server restarts; the code-breaking engine never sends the secret password to the client. Validate player input in the engine layer and return Chinese error messages.
