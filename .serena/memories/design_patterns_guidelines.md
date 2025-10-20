# Design Patterns & Guidelines

## Architecture Patterns

### Modular Workflow Steps
各stepは独立したモジュールとして`src/steps/`に配置:
- `news.py` - ニュース収集
- `script.py` - スクリプト生成
- `audio.py` - 音声合成
- `subtitle.py` - 字幕生成
- `video.py` - 動画レンダリング

### Provider Pattern
`src/providers/base.py`でbase interfaceを定義、fallback chainingをサポート:
- Perplexity → Gemini (news)
- Voicevox (TTS)

### State Management
`src/core/state.py`でpipeline state永続化、`runs/<run_id>/state.json`で中断からの再開可能

### Configuration-Driven
- `config/default.yaml` - workflow toggles, credentials
- `config/prompts.yaml` - runtime prompts
- `config/.env` - secrets (gitignored)

## Key Principles

1. **Composability**: 各関数は単一責任、合成可能に
2. **Type Safety**: Pydanticでdata validation
3. **Resumability**: state.jsonでpipeline再開
4. **Flexibility**: YAMLでprovider/step有効化切替

## Security Guidelines
- `config/.env`でcredentials管理（gitignore必須）
- `runs/`の機密データは共有環境で削除
- Gemini key rotation推奨
- `.env.example`から`.env`コピーして設定

## Testing Strategy
- `tests/fixtures/` - 再現可能なpayload
- Unit: 外部依存なし、fast
- Integration: mocked APIs
- E2E: real APIs、regression tests
- Coverage gate維持
