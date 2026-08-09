import pytest

from src.content_modes import MODE_NAME, build_comprehensive_plan, validate_completion


def test_build_plan_preserves_explicit_coverage_order_and_deduplicates():
    plan = build_comprehensive_plan(
        "NISA",
        "初心者",
        ["何が変わった？", " 仕組みは？ ", "何が変わった？", "注意点は？"],
    )

    assert plan.mode == MODE_NAME
    assert [item.id for item in plan.coverage] == ["Q01", "Q02", "Q03"]
    assert [item.question for item in plan.coverage] == ["何が変わった？", "仕組みは？", "注意点は？"]


def test_plan_is_deterministic_for_same_inputs():
    first = build_comprehensive_plan("topic", "audience", ["a", "b"]).to_dict()
    second = build_comprehensive_plan("topic", "audience", ["a", "b"]).to_dict()

    assert first == second


def test_mode_fails_closed_without_explicit_coverage():
    with pytest.raises(ValueError, match="explicit coverage"):
        build_comprehensive_plan("topic", "audience", [" "])


def test_completion_requires_every_coverage_id():
    plan = build_comprehensive_plan("topic", "audience", ["a", "b", "c"])

    complete, missing = validate_completion(plan, ["Q01", "Q03"])
    assert complete is False
    assert missing == ("Q02",)

    complete, missing = validate_completion(plan, ["Q03", "Q02", "Q01", "Q99"])
    assert complete is True
    assert missing == ()
