# ytmanager

YouTube channel management system with analytics and auto-optimization

## 機能

### 1. Analytics解析
YouTube Data/Analytics APIから視聴データ収集、metrics計算

- watch_time - 総視聴時間
- ctr - クリック率
- engagement_rate - エンゲージメント率
- average_view_duration - 平均視聴時間

### 2. Optimizer自動改善
analyticsデータから`prompts.yaml`自動改定提案

- A/Bテスト管理
- フィードバックループ（日次/週次）
- 最小サンプルサイズ制御

### 3. Scheduler管理
cron/シリーズ実行、実行キュー管理

- 定時実行
- シリーズ企画管理
- 競合回避キュー

### 4. Channels管理
マルチチャンネル登録、config継承、2511youtuber起動wrapper

## セットアップ

```bash
uv sync
cp config/channels.yaml.example config/channels.yaml
```

`config/channels.yaml`を編集:
- `youtube_channel_id`を設定
- `project_path`を確認
- analytics/optimizer設定

## コマンド

### Analytics実行
```bash
uv run python -m ytmanager.analytics --channel byousoku_money
```

### Optimizer実行
```bash
uv run python -m ytmanager.optimizer --channel byousoku_money --mode daily
```

### Scheduler管理
```bash
uv run python -m ytmanager.scheduler --action list
uv run python -m ytmanager.scheduler --action run --channel byousoku_money
```

## ディレクトリ構造

```
ytmanager/
├── src/
│   ├── analytics/
│   │   ├── youtube_api.py    # Data/Analytics API
│   │   ├── metrics.py        # metrics計算
│   │   └── reporter.py       # Aim/MLflow出力
│   ├── optimizer/
│   │   ├── prompt_tuner.py   # prompts.yaml改定
│   │   ├── ab_test.py        # A/Bテスト
│   │   └── feedback_loop.py  # metrics→prompt
│   ├── scheduler/
│   │   ├── cron_manager.py   # 定時実行
│   │   ├── series_manager.py # シリーズ管理
│   │   └── queue.py          # 実行キュー
│   └── channels/
│       ├── registry.py       # チャンネル登録
│       ├── config_merger.py  # config継承
│       └── launcher.py       # 2511youtuber起動
├── config/
│   └── channels.yaml         # チャンネル定義
└── tests/
```

## フィードバックループ

```
1. 2511youtuber実行 → runs/*.json生成
2. ytmanager analytics → metrics計算
3. ytmanager optimizer → prompts.yaml改定提案
4. 承認 → 次回実行に反映
```
