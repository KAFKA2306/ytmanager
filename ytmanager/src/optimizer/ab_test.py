from pathlib import Path
from typing import Dict, Optional
import json
import random
from datetime import datetime


class ABTest:
    def __init__(self, storage_path: str = "data/ab_tests.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.tests = self._load()

    def _load(self) -> Dict:
        if self.storage_path.exists():
            with open(self.storage_path) as f:
                return json.load(f)
        return {}

    def _save(self):
        with open(self.storage_path, "w") as f:
            json.dump(self.tests, f, indent=2, ensure_ascii=False)

    def create_test(self, test_id: str, variant_a: Dict, variant_b: Dict, ratio: float = 0.5) -> Dict:
        self.tests[test_id] = {
            "created_at": datetime.now().isoformat(),
            "variant_a": variant_a,
            "variant_b": variant_b,
            "ratio": ratio,
            "results": {
                "a": {"runs": 0, "total_metrics": {}},
                "b": {"runs": 0, "total_metrics": {}}
            },
            "status": "active"
        }
        self._save()
        return self.tests[test_id]

    def select_variant(self, test_id: str) -> str:
        test = self.tests.get(test_id)
        return "b" if random.random() < test["ratio"] else "a"

    def record_result(self, test_id: str, variant: str, metrics: Dict):
        test = self.tests[test_id]
        result = test["results"][variant]
        result["runs"] += 1

        for metric, value in metrics.items():
            if metric not in result["total_metrics"]:
                result["total_metrics"][metric] = 0
            result["total_metrics"][metric] += value

        self._save()

    def get_averages(self, test_id: str) -> Dict:
        test = self.tests[test_id]
        averages = {"a": {}, "b": {}}

        for variant in ["a", "b"]:
            result = test["results"][variant]
            runs = result["runs"]
            if runs > 0:
                for metric, total in result["total_metrics"].items():
                    averages[variant][metric] = total / runs

        return averages

    def analyze(self, test_id: str, min_sample_size: int = 10) -> Optional[Dict]:
        test = self.tests[test_id]
        results_a = test["results"]["a"]
        results_b = test["results"]["b"]

        if results_a["runs"] < min_sample_size or results_b["runs"] < min_sample_size:
            return None

        averages = self.get_averages(test_id)
        winner = None
        improvements = {}

        for metric in averages["a"].keys():
            a_val = averages["a"][metric]
            b_val = averages["b"][metric]
            diff = ((b_val - a_val) / a_val * 100) if a_val > 0 else 0
            improvements[metric] = diff

            if abs(diff) > 10:
                winner = "b" if diff > 0 else "a"

        return {
            "winner": winner,
            "averages": averages,
            "improvements": improvements,
            "sample_sizes": {"a": results_a["runs"], "b": results_b["runs"]}
        }

    def conclude(self, test_id: str) -> Dict:
        analysis = self.analyze(test_id)
        self.tests[test_id]["status"] = "concluded"
        self.tests[test_id]["conclusion"] = analysis
        self._save()
        return analysis
