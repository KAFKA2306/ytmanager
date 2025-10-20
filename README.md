# aiytmanager

YouTube動画自動生成システムの管理リポジトリ

## 役割
2511youtuberを自由自在にマネージメント

## 目的
視聴者を過去以上に楽しませる

## プロジェクト構造

```
aiytmanager/
├── ytmanager/         # 管理層（analytics、optimizer、scheduler）
├── 2511youtuber/      # 実行層（動画生成パイプライン）
├── templates/         # 新規チャンネルテンプレート
├── AGENTS.md          # ytmanager役割定義
├── CLAUDE.md          # ytmanager開発指示
└── README.md          # このファイル
```

### ytmanager/ - 管理層
YouTube Analytics解析、プロンプト自動改善、スケジュール管理、マルチチャンネル管理。

**ディレクトリ構成**
```
ytmanager/
├── src/
│   ├── analytics/      # YouTube API連携、metrics計算
│   ├── optimizer/      # prompts.yaml自動改定
│   ├── scheduler/      # cron管理、シリーズ実行
│   └── channels/       # チャンネル登録、config継承
├── config/
│   └── channels.yaml   # チャンネル/スケジュール定義
└── tests/
```

**機能**
1. **Analytics解析** - YouTube Data/Analytics APIで視聴データ収集、metrics計算（視聴維持率、CTR、engagement）
2. **Optimizer自動改善** - analyticsデータから`2511youtuber/config/prompts.yaml`自動改定
3. **Scheduler管理** - cron/シリーズ実行、実行キュー管理
4. **Channels管理** - マルチチャンネル登録、config継承、2511youtuber起動wrapper

### 2511youtuber/ - 実行層
金融ニュース動画の自動生成パイプライン。

**ディレクトリ構成**
```
2511youtuber/
├── src/
│   ├── core/           # WorkflowOrchestrator、state管理
│   ├── steps/          # NewsCollector、ScriptGenerator等
│   ├── providers/      # Gemini、VOICEVOX、YouTube API wrapper
│   └── utils/          # config、logger、secrets
├── config/
│   ├── default.yaml    # ワークフロー設定
│   ├── prompts.yaml    # プロンプトテンプレート
│   └── .env            # API keys
├── apps/youtube/       # CLI entry point
├── assets/             # fonts、character images、intro/outro clips
├── runs/               # 生成成果物（run_id別）
└── tests/
```

**パイプライン**
1. NewsCollector → news.json
2. ScriptGenerator → script.json
3. AudioSynthesizer → audio.wav
4. SubtitleFormatter → subtitles.srt
5. VideoRenderer → video.mp4
6. Optional: ThumbnailGenerator、YouTubeUploader、TwitterPoster等

詳細は`2511youtuber/CLAUDE.md`参照。

## 手段

### プロンプト微調整
`2511youtuber/config/prompts.yaml`および`default.yaml`をほんの少し改変することで新鮮な調子の動画を作成。

### データ駆動改善
YouTube Analytics情報および`2511youtuber/runs/*.json`から成功/失敗を定量的に判断。

### 柔軟な企画
情勢、ジャンル、シリーズものなど自由な発想で新鮮な動画を提供。

## フィードバックループ

```
1. 2511youtuber実行 → runs/*.json生成
   ↓
2. ytmanager analytics → metrics計算
   ↓
3. ytmanager optimizer → prompts.yaml改定提案
   ↓
4. 承認 → 次回実行に反映
```

## コマンド

### 2511youtuber実行
```bash
cd 2511youtuber
uv sync
cp config/.env.example config/.env
uv run python -m src.main --news-query "トピック"
```

### ytmanager実行
```bash
cd ytmanager
uv sync
uv run python -m ytmanager.analytics --channel byousoku_money
uv run python -m ytmanager.optimizer --channel byousoku_money
uv run python -m ytmanager.scheduler --action list
```

## ドキュメント
- `AGENTS.md` - ytmanager役割定義
- `CLAUDE.md` - ytmanager開発指示
- `2511youtuber/CLAUDE.md` - 2511youtuber開発指示
- `2511youtuber/README.md` - 2511youtuber詳細
- `2511youtuber/docs/` - system_overview、operations等
