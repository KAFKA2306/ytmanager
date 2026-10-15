# Repository Guidelines

## Project Structure & Module Organization
Core pipeline modules live in `2511youtuber/src`, with orchestration in `core/`, reusable building blocks in `steps/`, data contracts in `models.py`, and provider integrations under `providers/`. `apps/youtube` wires the workflow that `src/main.py` exposes and acts as the entrypoint. Configuration templates and prompt variants sit in `config/` (including `.env` overrides and YAML run presets). Media assets live in `assets/`; automation helpers sit in `scripts/`. Tests live in `tests/unit` and `tests/integration`, mirroring module names for clarity.

## Build, Test, and Development Commands
Run these from `2511youtuber/`:
- `python -m venv .venv && source .venv/bin/activate` prepares a Python 3.11 environment matching `requires-python`.
- `pip install -e .[dev]` installs runtime plus dev extras from `pyproject.toml`.
- `python -m src.main --news-query "市場 動向"` runs the end-to-end YouTube pipeline with an override query.
- `python scripts/inspect_tree.py` reports module size, imports, and potential dead code.

## Coding Style & Naming Conventions
Use 4-space indentation, modern type hints, and docstrings only when flow is non-trivial. Ruff enforces linting with a 120-character limit; run `ruff check src tests` until clean. Prefer snake_case for modules/functions, PascalCase for classes, and UPPER_CASE for constants. Keep YAML keys lowercase and space-free.

## Testing Guidelines
Pytest is configured through `pytest.ini`. Fast check: `pytest -m "unit or integration"`; full suites need API creds for `e2e` tests (`GEMINI_API_KEY`, VoiceVox). Name tests `test_<feature>.py`, mark them (`@pytest.mark.unit`) for filtering, and share fixtures via `tests/conftest.py`. Cover new branches and error paths before opening a PR.

## Commit & Pull Request Guidelines
With no history yet, adopt a Conventional Commit style (`feat: add voiceover mixer`, `fix: guard empty news feed`) to keep future automation straightforward. Keep subjects under 72 chars, document motivation and validation in the body, and link tasks when available. Pull requests should summarise pipeline impact, note config changes, list new dependencies or secrets, and attach CLI output or screenshots for user-visible updates.

## Configuration & Secrets
Create `config/.env` from the latest secret bundle and avoid committing live credentials. Tune workflow knobs in `config/default.yaml` and `config/prompts.yaml`; keep experimental variants in dedicated YAML files. Generated media lands under `runs/`—prune large artifacts before pushing and ensure assets referenced in YAML (intro/outro clips, overlays) exist locally to prevent runtime failures.

## Outcome-first task interpretation (Altitude / Depth / Range / Speed)

- **Altitude:** Interpret a task as a verifiable user outcome, not only the named intermediate step. Infer the smallest justified acceptance criteria from the request and current repository state; do not silently expand scope or override explicit instructions.
- **Depth:** Use primary/current evidence and real domain tools and methods. Verify the actual postcondition independently of agent self-report, preferably on the exact changed revision or target runtime.
- **Range:** Combine code, data, tests, runtime/UI, and domain expertise when that materially improves the outcome, while respecting canonical owners and avoiding duplicate systems.
- **Speed:** Complete authorized read-only and reversible work through implementation, focused checks, and read-back without unnecessary approval loops. Bound retries and stop at the proven outcome.
- These principles never bypass repository-specific security, privacy, permission, publication, spending, destructive-action, or release boundaries. State verified results and any remaining `UNVERIFIED` layers.
