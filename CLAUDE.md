# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Setup
```bash
uv sync
cp config/.env.example config/.env
```

### Run Pipeline
```bash
uv run python -m src.main --news-query "トヨタ 四半期 決算"
```

### Code Quality
```bash
uv run ruff format src tests
uv run ruff check src tests
uv run ruff check --fix src tests
```

### Testing
```bash
uv run pytest -m unit -v --cov=src --cov-report=term-missing
uv run pytest -m integration -v
uv run pytest -m e2e -v
uv run pytest tests/unit/test_specific.py::test_function_name -v
```

## Architecture

### Workflow Orchestration
The system uses a checkpoint-based orchestration model where `WorkflowOrchestrator` (`src/core/orchestrator.py`) executes a sequence of `Step` subclasses. Each step:
- Declares `name`, `output_filename`, and `is_required` attributes
- Implements `execute(config, previous_outputs)` to produce artifacts
- Writes outputs to `runs/<run_id>/`
- Persists completion state in `state.json` for resumability

Steps execute in order: `NewsCollector` → `ScriptGenerator` → `AudioSynthesizer` → `SubtitleFormatter` → `VideoRenderer` → optional steps (thumbnail, metadata, uploads).

### Configuration System
`Config.load()` (`src/utils/config.py`) reads `config/default.yaml` and validates strongly typed Pydantic models. Steps consume only their config slice (e.g., `config.steps.video.effects`). Provider credentials load from `config/.env` via `python-dotenv`.

Key config sections:
- `workflow` - run directory, checkpoint behavior
- `steps.<step_name>` - per-step parameters (speakers, subtitle width, video effects)
- `providers` - Gemini models, VOICEVOX server URL, API endpoints

### Provider Pattern
`src/providers/base.py` defines a fallback chain for resilience. `NewsCollector` tries Perplexity → Gemini. Provider classes abstract LLM/TTS APIs:
- `GeminiProvider` / `PerplexityProvider` - handle prompt templates from `config/prompts.yaml`
- `VOICEVOXProvider` - maps speaker aliases to IDs, auto-starts server, synthesizes audio

### Step Implementations
Each `src/steps/*.py` module is self-contained:
- **NewsCollector** - queries news APIs, returns JSON
- **ScriptGenerator** - prompts Gemini with speaker profiles, previous context
- **AudioSynthesizer** - concatenates VOICEVOX audio segments
- **SubtitleFormatter** - estimates timing by character count, wraps Japanese text
- **VideoRenderer** - applies FFmpeg filters (Ken Burns, overlays), burns subtitles

Optional steps (`ThumbnailGenerator`, `YouTubeUploader`, `TwitterPoster`, etc.) are config-gated and `is_required=False`.

### Data Flow
```
src/main.py (entry)
  └─> apps/youtube/cli.py::run()
      ├─> _create_run_id() → timestamped identifier
      ├─> _build_steps(config) → instantiate enabled steps
      └─> WorkflowOrchestrator.execute()
          ├─> _load_previous_outputs() → resume from state.json
          └─> for each step:
              ├─> step.run(config, previous_outputs)
              ├─> write step output to runs/<run_id>/<output_filename>
              └─> persist state
```

### Asset and Output Paths
- `config/default.yaml` references `assets/` for fonts, character images, intro/outro clips
- `runs/<run_id>/` contains all generated artifacts: `news.json`, `script.json`, `audio.wav`, `subtitles.srt`, `video.mp4`, `state.json`
- Intro/outro paths are absolute in config - update if repository moves

## Testing Structure
- `tests/unit/` - fast, no external deps
- `tests/integration/` - mocked APIs
- `tests/e2e/` - real APIs (requires `GEMINI_API_KEY`)
- `tests/fixtures/` - reusable test payloads

Use `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.e2e` to control test scope.

## Code Style
- Python 3.11+, 4-space indents, 120-char line limit (Ruff)
- `snake_case` for functions/modules, `PascalCase` for classes, `UPPERCASE` for constants
- Pydantic models for structured data validation
- Configuration-driven (YAML) over hardcoded literals
- Prefer docstrings over inline comments
