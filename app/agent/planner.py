from typing import Dict, List

from app.agent.classifier import TaskType


def create_tool_plan(task_type: TaskType, query: str) -> Dict[str, object]:
    query_lower = query.lower()

    selected_tools: List[str] = []
    reasons: List[str] = []

    if task_type == "escalation_decision":
        selected_tools.extend(
            [
                "sql_tool",
                "log_search_tool",
                "rag_tool",
                "rule_validator",
            ]
        )
        reasons.append(
            "Escalation decisions require metrics, logs, policy evidence, and rule validation."
        )

    elif task_type == "prioritization":
        selected_tools.extend(
            [
                "sql_tool",
                "log_search_tool",
                "rag_tool",
                "rule_validator",
            ]
        )
        reasons.append(
            "Prioritization requires severity metrics, operational logs, policy context, and escalation rules."
        )

    elif task_type == "sql_lookup":
        selected_tools.append("sql_tool")
        reasons.append(
            "The request asks for structured operational metrics, so SQL lookup is required."
        )

    elif task_type == "log_analysis":
        selected_tools.append("log_search_tool")
        reasons.append(
            "The request mentions logs, errors, timeouts, or exceptions, so log search is required."
        )

    elif task_type == "policy_lookup":
        selected_tools.append("rag_tool")
        reasons.append(
            "The request asks about policy, SLA, runbook, or documentation, so document retrieval is required."
        )

    elif task_type == "summarization":
        selected_tools.append("rag_tool")
        reasons.append(
            "The request asks for explanation or summary, so policy/runbook retrieval is useful."
        )

    elif task_type == "comparison":
        selected_tools.extend(["sql_tool", "rag_tool"])
        reasons.append(
            "Comparison requests may require structured data and policy context."
        )

    elif task_type == "ambiguous":
        selected_tools.append("human_review_tool")
        reasons.append(
            "The request is ambiguous and does not contain enough operational detail for reliable automation."
        )

    else:
        selected_tools.extend(["sql_tool", "log_search_tool", "rag_tool"])
        reasons.append(
            "General investigation requests may require metrics, logs, and policy context."
        )

    # Add safety expansion if escalation-like terms appear even if classifier missed them.
    if "escalat" in query_lower and "rule_validator" not in selected_tools:
        selected_tools.append("rule_validator")
        reasons.append(
            "Escalation-related wording was detected, so rule validation was added."
        )

    if "policy" in query_lower or "sla" in query_lower or "runbook" in query_lower:
        if "rag_tool" not in selected_tools:
            selected_tools.append("rag_tool")
            reasons.append(
                "Policy-related wording was detected, so RAG retrieval was added."
            )

    if "error" in query_lower or "timeout" in query_lower or "log" in query_lower:
        if "log_search_tool" not in selected_tools:
            selected_tools.append("log_search_tool")
            reasons.append(
                "Error/log-related wording was detected, so log search was added."
            )

    return {
        "task_type": task_type,
        "selected_tools": list(dict.fromkeys(selected_tools)),
        "reasons": reasons,
    }