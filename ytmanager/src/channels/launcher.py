import subprocess
from pathlib import Path
from typing import Optional


class Launcher:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)

    def run(self, news_query: Optional[str] = None, dry_run: bool = False) -> subprocess.CompletedProcess:
        cmd = ["uv", "run", "python", "-m", "src.main"]
        if news_query:
            cmd.extend(["--news-query", news_query])
        if dry_run:
            cmd.append("--dry-run")
        return subprocess.run(cmd, cwd=self.project_path, capture_output=True, text=True)

    def get_latest_run_id(self) -> Optional[str]:
        runs_dir = self.project_path / "runs"
        runs = sorted(runs_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
        return runs[0].name if runs else None

    def get_run_outputs(self, run_id: str) -> dict:
        run_dir = self.project_path / "runs" / run_id
        outputs = {}
        for file in run_dir.glob("*.json"):
            outputs[file.stem] = file
        return outputs
