# Task Completion Workflow

## After Code Changes

### 1. Format
```bash
uv run ruff format src tests
```

### 2. Lint
```bash
uv run ruff check src tests
```

### 3. Test
```bash
# Unit tests (always)
uv run pytest -m unit -v --cov=src --cov-report=term-missing

# Integration tests (before refactoring)
uv run pytest -m integration -v

# E2E tests (when changing API integrations)
uv run pytest -m e2e -v
```

### 4. Coverage Gate
Maintain coverage at or above default `--cov=src` gate

### 5. Commit
Conventional Commits形式: `feat:`, `fix:`, `refactor:`
- Imperative, <72 chars
- 本文で意図を説明

## Before PR
- All tests passing
- Coverage maintained
- Ruff format + lint clean
- Configuration impact documented
