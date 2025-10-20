from typing import Dict
from pathlib import Path
import json
from datetime import datetime
from .prompt_tuner import PromptTuner
from .ab_test import ABTest


class FeedbackLoop:
    def __init__(self, prompts_path: str, ab_test_storage: str = "data/ab_tests.json", history_path: str = "data/feedback_history.json"):
        self.tuner = PromptTuner(prompts_path)
        self.ab_test = ABTest(ab_test_storage)
        self.history_path = Path(history_path)
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        self.history = self._load_history()

    def _load_history(self) -> list:
        if self.history_path.exists():
            with open(self.history_path) as f:
                return json.load(f)
        return []

    def _save_history(self):
        with open(self.history_path, "w") as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)

    def run_daily(self, metrics: Dict, channel: str, auto_apply: bool = False) -> Dict:
        timestamp = datetime.now().isoformat()

        tuning_result = self.tuner.tune(metrics, ab_test=False, dry_run=not auto_apply)

        entry = {
            "timestamp": timestamp,
            "channel": channel,
            "metrics": metrics,
            "suggestions": tuning_result["suggestions"],
            "improvements": tuning_result["improvements"],
            "applied": tuning_result["applied"],
            "auto_applied": auto_apply
        }

        self.history.append(entry)
        self._save_history()

        return entry

    def run_weekly(self, weekly_metrics: list[Dict], channel: str, min_sample_size: int = 10) -> Dict:
        timestamp = datetime.now().isoformat()

        aggregated_metrics = self._aggregate_metrics(weekly_metrics)

        active_tests = [tid for tid, test in self.ab_test.tests.items() if test["status"] == "active"]
        analyses = {}

        for test_id in active_tests:
            analysis = self.ab_test.analyze(test_id, min_sample_size)
            if analysis:
                analyses[test_id] = analysis

                if analysis["winner"]:
                    self.ab_test.conclude(test_id)

        tuning_result = self.tuner.tune(aggregated_metrics, ab_test=False, dry_run=True)

        entry = {
            "timestamp": timestamp,
            "channel": channel,
            "period": "weekly",
            "aggregated_metrics": aggregated_metrics,
            "ab_test_analyses": analyses,
            "suggestions": tuning_result["suggestions"]
        }

        self.history.append(entry)
        self._save_history()

        return entry

    def _aggregate_metrics(self, metrics_list: list[Dict]) -> Dict:
        if not metrics_list:
            return {}

        aggregated = {}
        metric_keys = metrics_list[0].keys()

        for key in metric_keys:
            values = [m[key] for m in metrics_list if key in m]
            aggregated[key] = sum(values) / len(values)

        return aggregated

    def get_recent_improvements(self, limit: int = 10) -> list[Dict]:
        return [h for h in self.history if h.get("applied")][-limit:]
