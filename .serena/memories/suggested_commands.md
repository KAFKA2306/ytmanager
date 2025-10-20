# Suggested Commands

## Setup
```bash
uv sync
cp config/.env.example config/.env
```

## Run Pipeline
```bash
uv run python -m src.main --news-query "FOMC 金利"
```

## Development
```bash
# Dry run (smoke test)
uv run python -m src.main --dry-run

# Format code
uv run ruff format src tests

# Lint code
uv run ruff check src tests

# Fix linting issues automatically
uv run ruff check --fix src tests
```

## Testing
```bash
# Unit tests with coverage
uv run pytest -m unit -v --cov=src --cov-report=term-missing

# Integration tests
uv run pytest -m integration -v

# E2E tests (requires API keys)
uv run pytest -m e2e -v

# All tests
uv run pytest -v
```

## Markers
- `@pytest.mark.unit` - fast, no external deps
- `@pytest.mark.integration` - mocked APIs
- `@pytest.mark.e2e` - real APIs (slow)
