# Project Overview

## Purpose
YouTube AI Video Generator v2: 日本語の金融ニュース動画を自動生成。毎日のニュースからナレーション付き動画を生成し、YouTubeへのアップロードまでの全工程を自動化。

## Tech Stack
- Python 3.11-3.12
- Gemini (script generation, news analysis)
- Voicevox (Japanese TTS)
- FFmpeg (video rendering)
- Pydantic (data validation)
- LiteLLM (LLM abstraction)
- Pillow (image processing)
- pytest (testing)

## Key Dependencies
- `pydantic>=2.0` - structured data models
- `pyyaml>=6.0` - configuration files
- `litellm>=1.0` - LLM provider abstraction
- `ffmpeg-python>=0.2` - video processing
- `google-api-python-client>=2.0` - YouTube API
- `tweepy==4.*` - Twitter integration
- `discord.py>=2.3` - Discord notifications
- `feedgen>=1.0.0` - RSS feed generation

## Python Version
Requires Python >=3.11, <3.13
