from app.agent.planner import create_tool_plan


def test_escalation_plan_uses_all_core_tools():
    plan = create_tool_plan(
        task_type="escalation_decision",
        query="Should this payment issue be escalated?",
    )

    assert set(plan["selected_tools"]) == {
        "sql_tool",
        "log_search_tool",
        "rag_tool",
        "rule_validator",
    }


def test_policy_lookup_uses_rag_only():
    plan = create_tool_plan(
        task_type="policy_lookup",
        query="What does the SLA policy say?",
    )

    assert plan["selected_tools"] == ["rag_tool"]


def test_sql_lookup_uses_sql_only():
    plan = create_tool_plan(
        task_type="sql_lookup",
        query="What is the payment failure rate?",
    )

    assert plan["selected_tools"] == ["sql_tool"]


def test_log_analysis_uses_log_search_only():
    plan = create_tool_plan(
        task_type="log_analysis",
        query="Find timeout errors in logs.",
    )

    assert plan["selected_tools"] == ["log_search_tool"]


def test_ambiguous_request_goes_to_human_review_tool():
    plan = create_tool_plan(
        task_type="ambiguous",
        query="Something is wrong.",
    )

    assert plan["selected_tools"] == ["human_review_tool"]


def test_safety_expansion_adds_rag_for_policy_wording():
    plan = create_tool_plan(
        task_type="investigation",
        query="Check the SLA policy for this issue.",
    )

    assert "rag_tool" in plan["selected_tools"]


def test_safety_expansion_adds_log_search_for_error_wording():
    plan = create_tool_plan(
        task_type="investigation",
        query="Check this timeout error.",
    )

    assert "log_search_tool" in plan["selected_tools"]