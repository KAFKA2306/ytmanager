# Codebase Structure

```
├── apps/              # Application entry points
│   └── youtube/cli.py # Standard pipeline driver
├── config/            # YAML configuration & prompt templates
│   ├── default.yaml   # Workflow toggles, credentials, rendering params
│   ├── prompts.yaml   # Runtime prompt templates
│   └── .env.example   # Environment variable template
├── docs/              # System overview and operations guides
│   ├── system_overview.md
│   └── operations.md
├── src/               # Core workflow, providers, step implementations
│   ├── main.py        # CLI bootstrap
│   ├── core/          # State coordination
│   │   └── orchestrator.py
│   ├── steps/         # Pipeline stages
│   │   ├── news.py    # Perplexity/Gemini news collection
│   │   ├── script.py  # Gemini dialogue generation
│   │   ├── audio.py   # Voicevox TTS synthesis
│   │   ├── subtitle.py # SRT formatting
│   │   ├── video.py   # FFmpeg rendering
│   │   └── thumbnail.py
│   ├── providers/     # External API integrations
│   │   ├── base.py
│   │   ├── news.py
│   │   └── tts.py
│   └── utils/         # Shared helpers
│       └── config.py  # Typed configuration models
├── tests/             # Unit, integration, e2e suites
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── fixtures/
├── assets/            # Fonts and character art for rendering
├── scripts/           # Automation scripts
└── runs/              # Generated artifacts per run (created on demand)
    └── <run_id>/
        ├── state.json # Persisted pipeline state
        ├── news.json
        ├── script.json
        ├── audio.wav
        ├── subtitles.srt
        └── video.mp4
```

## Workflow Flow
1. `apps/youtube/cli.py` → entry point
2. `src/main.py` → bootstrap
3. `src/core/orchestrator.py` → coordinate steps
4. `src/steps/` → execute pipeline stages
5. `src/providers/` → interact with external APIs
6. `runs/<run_id>/state.json` → resume mid-pipeline
