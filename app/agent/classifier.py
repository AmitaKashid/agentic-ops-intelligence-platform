from typing import Literal


TaskType = Literal[
    "escalation_decision",
    "prioritization",
    "sql_lookup",
    "log_analysis",
    "policy_lookup",
    "summarization",
    "comparison",
    "investigation",
    "ambiguous",
]


def classify_task(query: str) -> TaskType:
    query_lower = query.lower()

    escalation_terms = [
        "should this be escalated",
        "should we escalate",
        "escalate",
        "p1",
        "p2",
        "priority",
        "incident response",
    ]

    sql_terms = [
        "how many",
        "failure rate",
        "error rate",
        "latency",
        "affected customers",
        "failed requests",
        "metrics",
        "count",
    ]

    log_terms = [
        "log",
        "logs",
        "error",
        "timeout",
        "exception",
        "warning",
        "error code",
    ]

    policy_terms = [
        "policy",
        "sla",
        "runbook",
        "documentation",
        "threshold",
        "what does the policy say",
    ]

    summary_terms = [
        "summarize",
        "summary",
        "explain",
        "overview",
    ]

    comparison_terms = [
        "compare",
        "difference",
        "versus",
        "vs",
    ]

    ambiguous_terms = [
    "something wrong",
    "something seems wrong",
    "seems wrong",
    "not working",
    "issue",
    "problem",
    "broken",
    "feels broken",
    "do not know where",
    "don't know where",
    "no clear service",
]

    if any(term in query_lower for term in escalation_terms):
        return "escalation_decision"

    if any(term in query_lower for term in comparison_terms):
        return "comparison"

    if any(term in query_lower for term in policy_terms):
        return "policy_lookup"

    if any(term in query_lower for term in sql_terms):
        return "sql_lookup"

    if any(term in query_lower for term in log_terms):
        return "log_analysis"

    if any(term in query_lower for term in summary_terms):
        return "summarization"

    if any(term in query_lower for term in ambiguous_terms):
        return "ambiguous"

    return "investigation"