# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure & Module Organization
Core pipeline modules live in `2511youtuber/src`, with orchestration in `core/`, reusable building blocks in `steps/`, data contracts in `models.py`, and provider integrations under `providers/`. `apps/youtube` wires the workflow that `src/main.py` exposes and acts as the entrypoint. Configuration templates and prompt variants sit in `config/` (including `.env` overrides and YAML run presets). Media assets live in `assets/`; automation helpers sit in `scripts/`. Tests live in `tests/unit` and `tests/integration`, mirroring module names for clarity.

## Commands


### Run Pipeline
```bash
uv run python -m 2511youtuber.src.main --news-query "トヨタ 四半期 決算"
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
The system uses a checkpoint-based orchestration model where `WorkflowOrchestrator` (`2511youtuber/src/core/orchestrator.py`) executes a sequence of `Step` subclasses. Each step:
- Declares `name`, `output_filename`, and `is_required` attributes
- Implements `execute(config, previous_outputs)` to produce artifacts
- Writes outputs to `runs/<run_id>/`
- Persists completion state in `state.json` for resumability

Steps execute in order: `NewsCollector` → `ScriptGenerator` → `AudioSynthesizer` → `SubtitleFormatter` → `VideoRenderer` → optional steps (thumbnail, metadata, uploads).

### Configuration System
`Config.load()` (`2511youtuber/src/utils/config.py`) reads `config/default.yaml` and validates strongly typed Pydantic models. Steps consume only their config slice (e.g., `2511youtuber.config.steps.video.effects`). Provider credentials load from `2511youtuber/config/.env` via `python-dotenv`.

Key config sections:
- `workflow` - run directory, checkpoint behavior
- `steps.<step_name>` - per-step parameters (speakers, subtitle width, video effects)
- `providers` - Gemini models, VOICEVOX server URL, API endpoints

### Provider Pattern
`src/providers/base.py` defines a fallback chain for resilience. `NewsCollector` tries Perplexity → Gemini. Provider classes abstract LLM/TTS APIs:
- `GeminiProvider` / `PerplexityProvider` - handle prompt templates from `2511youtuber/config/prompts.yaml`
- `VOICEVOXProvider` - maps speaker aliases to IDs, auto-starts server, synthesizes audio

### Step Implementations
Each `2511youtuber/src/steps/*.py` module is self-contained:
- **NewsCollector** - queries news APIs, returns JSON
- **ScriptGenerator** - prompts Gemini with speaker profiles, previous context
- **AudioSynthesizer** - concatenates VOICEVOX audio segments
- **SubtitleFormatter** - estimates timing by character count, wraps Japanese text
- **VideoRenderer** - applies FFmpeg filters (Ken Burns, overlays), burns subtitles

Optional steps (`ThumbnailGenerator`, `YouTubeUploader`, `TwitterPoster`, etc.) are config-gated and `is_required=False`.

### Data Flow
```
2511youtuber/src/main.py (entry)
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
- `2511youtuber/config/default.yaml` references `assets/` for fonts, character images, intro/outro clips
- `runs/<run_id>/` contains all generated artifacts: `news.json`, `script.json`, `audio.wav`, `subtitles.srt`, `video.mp4`, `state.json`
- Intro/outro paths are absolute in config - update if repository moves


## Code Style
- Python 3.11+, 4-space indents, 120-char line limit (Ruff)
- `snake_case` for functions/modules, `PascalCase` for classes, `UPPERCASE` for constants
- Pydantic models for structured data validation
- Configuration-driven (YAML) over hardcoded literals
- Prefer docstrings over inline comments
