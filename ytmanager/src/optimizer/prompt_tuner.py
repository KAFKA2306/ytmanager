from pathlib import Path
from typing import Dict, List
import yaml


class PromptTuner:
    def __init__(self, prompts_path: str):
        self.prompts_path = Path(prompts_path)
        self.prompts = self._load()

    def _load(self) -> Dict:
        with open(self.prompts_path) as f:
            return yaml.safe_load(f)

    def _save(self):
        with open(self.prompts_path, "w") as f:
            yaml.dump(self.prompts, f, allow_unicode=True, sort_keys=False)

    def analyze_metrics(self, metrics: Dict) -> Dict:
        suggestions = {}

        if metrics.get("engagement_rate", 0) < 0.05:
            suggestions["engagement"] = "低engagement率。質問形式・驚き要素を増やす"

        if metrics.get("retention_rate", 0) < 0.4:
            suggestions["retention"] = "低retention率。冒頭のフック強化、テンポ改善"

        if metrics.get("ctr", 0) < 0.05:
            suggestions["ctr"] = "低CTR。タイトル・サムネイル訴求力強化"

        avg_duration = metrics.get("average_view_duration", 0)
        if avg_duration < 180:
            suggestions["duration"] = "短い視聴時間。導入部を簡潔に、本題を早く"

        return suggestions

    def generate_prompt_improvements(self, suggestions: Dict, ab_test: bool = False) -> Dict:
        improvements = {}

        if "engagement" in suggestions:
            improvements["news_prompt"] = {
                "addition": "\n\n視聴者の関心を引く質問形式や驚きの事実を含める。",
                "ab_variant": ab_test
            }

        if "retention" in suggestions:
            improvements["script_prompt"] = {
                "addition": "\n\n冒頭15秒で核心に触れ、視聴継続の動機を明確に示す。テンポよく展開。",
                "ab_variant": ab_test
            }

        if "ctr" in suggestions:
            improvements["metadata_prompt"] = {
                "addition": "\n\nタイトルは数字・疑問形・緊急性を含める。25-35文字推奨。",
                "ab_variant": ab_test
            }

        if "duration" in suggestions:
            improvements["script_prompt"] = {
                "addition": "\n\n導入は30秒以内。すぐ本題へ。",
                "ab_variant": ab_test
            }

        return improvements

    def apply_improvements(self, improvements: Dict, dry_run: bool = False) -> List[str]:
        applied = []

        for key, change in improvements.items():
            if key in self.prompts:
                original = self.prompts[key]
                if change.get("ab_variant"):
                    applied.append(f"A/Bテスト: {key} - {change['addition']}")
                else:
                    self.prompts[key] = original + change["addition"]
                    applied.append(f"適用: {key}")

        if not dry_run:
            self._save()

        return applied

    def tune(self, metrics: Dict, ab_test: bool = False, dry_run: bool = False) -> Dict:
        suggestions = self.analyze_metrics(metrics)
        improvements = self.generate_prompt_improvements(suggestions, ab_test)
        applied = self.apply_improvements(improvements, dry_run)

        return {
            "suggestions": suggestions,
            "improvements": improvements,
            "applied": applied
        }
