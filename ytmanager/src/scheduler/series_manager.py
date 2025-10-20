from pathlib import Path
from typing import Dict, List, Optional
import json
from datetime import datetime


class SeriesManager:
    def __init__(self, series_file: str = "data/series.json"):
        self.series_file = Path(series_file)
        self.series_file.parent.mkdir(parents=True, exist_ok=True)
        self.series = self._load()

    def _load(self) -> Dict:
        if self.series_file.exists():
            with open(self.series_file) as f:
                return json.load(f)
        return {}

    def _save(self):
        with open(self.series_file, "w") as f:
            json.dump(self.series, f, indent=2, ensure_ascii=False)

    def create(self, series_id: str, title: str, episodes: int, schedule: str, prompt_template: Optional[Dict] = None) -> Dict:
        self.series[series_id] = {
            "title": title,
            "total_episodes": episodes,
            "schedule": schedule,
            "prompt_template": prompt_template or {},
            "episodes_produced": [],
            "status": "active",
            "created_at": datetime.now().isoformat()
        }
        self._save()
        return self.series[series_id]

    def add_episode(self, series_id: str, run_id: str, episode_number: int, metadata: Optional[Dict] = None):
        series = self.series[series_id]
        series["episodes_produced"].append({
            "episode": episode_number,
            "run_id": run_id,
            "produced_at": datetime.now().isoformat(),
            "metadata": metadata or {}
        })
        self._save()

    def get_next_episode(self, series_id: str) -> int:
        series = self.series[series_id]
        return len(series["episodes_produced"]) + 1

    def is_complete(self, series_id: str) -> bool:
        series = self.series[series_id]
        return len(series["episodes_produced"]) >= series["total_episodes"]

    def complete(self, series_id: str):
        self.series[series_id]["status"] = "completed"
        self.series[series_id]["completed_at"] = datetime.now().isoformat()
        self._save()

    def list_active(self) -> List[Dict]:
        return [{"series_id": sid, **info} for sid, info in self.series.items() if info["status"] == "active"]

    def get(self, series_id: str) -> Optional[Dict]:
        return self.series.get(series_id)

    def get_prompt_for_episode(self, series_id: str, episode_number: int) -> Optional[Dict]:
        series = self.series.get(series_id)
        if not series or not series.get("prompt_template"):
            return None

        template = series["prompt_template"].copy()
        template["episode"] = episode_number
        template["total_episodes"] = series["total_episodes"]

        return template
