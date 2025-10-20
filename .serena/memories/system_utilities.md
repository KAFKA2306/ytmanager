# System Utilities

## Platform
Linux (WSL2: 6.6.87.2-microsoft-standard-WSL2)

## Standard Commands
```bash
# Package management
uv sync              # Install dependencies
uv add <package>     # Add package
uv remove <package>  # Remove package
uv run <command>     # Run in virtual env

# Git
git status
git add .
git commit -m "message"
git push
git pull

# File operations
ls -la
cd <dir>
cat <file>
grep -r "pattern" <dir>
find <dir> -name "pattern"

# Process management
ps aux | grep <process>
kill <pid>
pkill <name>
```

## Project-Specific Commands
```bash
# Run with custom query
uv run python -m src.main --news-query "テーマ"

# Check config
cat config/default.yaml

# View logs
tail -f runs/<run_id>/state.json

# Clean runs
rm -rf runs/*
```
