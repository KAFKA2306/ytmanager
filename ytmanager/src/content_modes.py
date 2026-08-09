"""Deterministic content-planning modes for ytmanager."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Iterable


MODE_NAME = "comprehensive_one_video"


@dataclass(frozen=True)
class CoverageItem:
    """A question that must be answered by the final video."""

    id: str
    question: str


@dataclass(frozen=True)
class ComprehensivePlan:
    """Coverage contract for a self-contained explanatory video."""

    mode: str
    topic: str
    audience: str
    coverage: tuple[CoverageItem, ...]

    def to_dict(self) -> dict:
        return {
            "mode": self.mode,
            "topic": self.topic,
            "audience": self.audience,
            "coverage": [asdict(item) for item in self.coverage],
            "completion_contract": {
                "required_coverage_ids": [item.id for item in self.coverage],
                "rule": "Every required coverage item must be answered before the video is complete.",
            },
        }


def _clean(value: str, field_name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name} must not be empty")
    return cleaned


def build_comprehensive_plan(topic: str, audience: str, questions: Iterable[str]) -> ComprehensivePlan:
    """Build a stable coverage contract for the 'one video is enough' mode.

    Questions are normalized by trimming whitespace and removing exact duplicates while
    preserving their first-seen order. At least one explicit coverage question is required;
    the mode never invents missing subject-matter requirements on its own.
    """

    normalized_topic = _clean(topic, "topic")
    normalized_audience = _clean(audience, "audience")

    unique_questions: list[str] = []
    seen: set[str] = set()
    for question in questions:
        cleaned = question.strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        unique_questions.append(cleaned)

    if not unique_questions:
        raise ValueError("at least one explicit coverage question is required")

    coverage = tuple(
        CoverageItem(id=f"Q{index:02d}", question=question)
        for index, question in enumerate(unique_questions, start=1)
    )
    return ComprehensivePlan(
        mode=MODE_NAME,
        topic=normalized_topic,
        audience=normalized_audience,
        coverage=coverage,
    )


def validate_completion(plan: ComprehensivePlan, answered_coverage_ids: Iterable[str]) -> tuple[bool, tuple[str, ...]]:
    """Return whether every required coverage item has explicit evidence of completion."""

    answered = {coverage_id.strip() for coverage_id in answered_coverage_ids if coverage_id.strip()}
    missing = tuple(item.id for item in plan.coverage if item.id not in answered)
    return not missing, missing


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a self-contained comprehensive-video coverage contract")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument(
        "--question",
        action="append",
        required=True,
        dest="questions",
        help="Question that the video must answer. Repeat for every required coverage item.",
    )
    args = parser.parse_args()
    plan = build_comprehensive_plan(args.topic, args.audience, args.questions)
    print(json.dumps(plan.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
