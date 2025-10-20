# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Setup
```bash
cd ytmanager
uv sync
```

### Run Analytics
```bash
uv run python -m ytmanager.analytics --channel byousoku_money
```

### Run Optimizer
```bash
uv run python -m ytmanager.optimizer --channel byousoku_money --mode daily
```

### Schedule Management
```bash
uv run python -m ytmanager.scheduler --action list
uv run python -m ytmanager.scheduler --action run --channel byousoku_money
```

### Code Quality
```bash
uv run ruff format ytmanager tests
uv run ruff check ytmanager tests
```

### Testing
```bash
uv run pytest -m unit -v
uv run pytest -m integration -v
```

## Architecture

### ytmanager Role
ytmanagerは2511youtuberを管理する上位層。役割:
1. **Analytics解析** - YouTube Data/Analytics APIで視聴データ収集、metrics計算
2. **Optimizer自動改善** - analyticsデータから`config/prompts.yaml`自動改定
3. **Scheduler管理** - cron/シリーズ実行、複数チャンネル管理
4. **Channels管理** - マルチチャンネル登録、config継承、実行wrapper

### Directory Structure
```
ytmanager/
├── src/
│   ├── analytics/      # YouTube API連携
│   │   ├── youtube_api.py    # Data/Analytics API
│   │   ├── metrics.py        # 視聴維持率/CTR計算
│   │   └── reporter.py       # Aim/MLflow出力
│   ├── optimizer/      # プロンプト自動改善
│   │   ├── prompt_tuner.py   # prompts.yaml改定
│   │   ├── ab_test.py        # A/Bテスト管理
│   │   └── feedback_loop.py  # metrics→prompt
│   ├── scheduler/      # 実行管理
│   │   ├── cron_manager.py   # 定時実行
│   │   ├── series_manager.py # シリーズ管理
│   │   └── queue.py          # 実行キュー
│   └── channels/       # チャンネル管理
│       ├── registry.py       # チャンネル登録
│       ├── config_merger.py  # default.yaml継承
│       └── launcher.py       # 2511youtuber起動
├── config/
│   └── channels.yaml   # チャンネル/スケジュール定義
├── tests/
└── pyproject.toml
```

### Feedback Loop
```
1. 2511youtuber実行 → runs/*.json生成
2. Analytics解析 → metrics計算（視聴維持率、CTR、engagement）
3. Optimizer判定 → config/prompts.yaml改定提案
4. 承認後 → 次回実行に反映
```

### Configuration Example
```yaml
# ytmanager/config/channels.yaml
channels:
  byousoku_money:
    project_path: ../2511youtuber
    youtube_channel_id: UC***
    schedule: "0 6 * * *"
    analytics:
      metrics:
        - watch_time
        - ctr
        - engagement_rate
      lookback_days: 7
    optimizer:
      auto_tune: true
      ab_test_ratio: 0.1
      feedback_interval: daily
```

## Implementation Strategy

### Phase 1: 骨格作成
- ytmanager/ディレクトリ構造
- channels.yaml定義
- 2511youtuber launcher wrapper

### Phase 2: Analytics実装
- YouTube Data API v3連携
- Analytics API連携
- metrics計算（watch_time, ctr, engagement_rate）
- Aim/MLflow出力

### Phase 3: Optimizer実装
- prompt_tuner: metrics→prompts.yaml改定ロジック
- ab_test: A/Bテスト管理
- feedback_loop: 日次/週次サイクル

### Phase 4: Scheduler実装
- cron_manager: 定時実行
- series_manager: シリーズ企画管理
- queue: 実行キュー（競合回避）

## Code Style
- Python 3.11+, 4-space indents, 120-char line limit (Ruff)
- `snake_case` for functions/modules, `PascalCase` for classes
- Pydantic models for configuration validation
- Type hints required
- コメント禁止（ユーザー指示）
- エラーハンドリング禁止（ユーザー指示）
