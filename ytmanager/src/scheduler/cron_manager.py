from pathlib import Path
from typing import Dict, List
import subprocess
import json
from datetime import datetime


class CronManager:
    def __init__(self, cron_file: str = "data/cron_schedule.json"):
        self.cron_file = Path(cron_file)
        self.cron_file.parent.mkdir(parents=True, exist_ok=True)
        self.schedule = self._load()

    def _load(self) -> Dict:
        if self.cron_file.exists():
            with open(self.cron_file) as f:
                return json.load(f)
        return {}

    def _save(self):
        with open(self.cron_file, "w") as f:
            json.dump(self.schedule, f, indent=2, ensure_ascii=False)

    def add(self, channel: str, cron_expression: str, command: str) -> Dict:
        self.schedule[channel] = {
            "cron": cron_expression,
            "command": command,
            "enabled": True,
            "last_run": None,
            "next_run": self._calculate_next_run(cron_expression)
        }
        self._save()
        self._update_system_cron()
        return self.schedule[channel]

    def remove(self, channel: str):
        if channel in self.schedule:
            del self.schedule[channel]
            self._save()
            self._update_system_cron()

    def enable(self, channel: str):
        if channel in self.schedule:
            self.schedule[channel]["enabled"] = True
            self._save()
            self._update_system_cron()

    def disable(self, channel: str):
        if channel in self.schedule:
            self.schedule[channel]["enabled"] = False
            self._save()
            self._update_system_cron()

    def list(self) -> List[Dict]:
        return [{"channel": ch, **info} for ch, info in self.schedule.items()]

    def _calculate_next_run(self, cron_expression: str) -> str:
        return datetime.now().isoformat()

    def _update_system_cron(self):
        cron_entries = []
        for channel, info in self.schedule.items():
            if info["enabled"]:
                cron_entries.append(f"{info['cron']} {info['command']}")

        cron_content = "\n".join(cron_entries)
        temp_file = Path("/tmp/ytmanager_cron")
        temp_file.write_text(cron_content)

        subprocess.run(["crontab", str(temp_file)], check=False)

    def record_run(self, channel: str):
        if channel in self.schedule:
            self.schedule[channel]["last_run"] = datetime.now().isoformat()
            self._save()
