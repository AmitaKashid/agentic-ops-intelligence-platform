from typing import Dict, List

from app.schemas import EvidenceItem


def generate_final_recommendation(
    task_type: str,
    rule_result: Dict[str, object] | None,
    evidence: List[EvidenceItem],
    evidence_quality: Dict[str, object],
    human_review_required: bool,
) -> str:
    if human_review_required:
        return (
            "Send this case to human review because the available evidence is not strong enough "
            "for a reliable automated recommendation."
        )

    if task_type == "policy_lookup":
        if not evidence:
            return "No relevant policy or runbook evidence was found."

        return (
            "Relevant policy/runbook evidence was retrieved. Review the cited evidence items "
            "to understand the applicable operational guidance."
        )

    if task_type == "sql_lookup":
        if not evidence:
            return "No matching structured metrics were found for this request."

        return (
            "Structured operational metrics were retrieved. Review the SQL evidence items "
            "for error rate, latency, failed requests, and customer impact."
        )

    if task_type == "log_analysis":
        if not evidence:
            return "No matching operational logs were found for this request."

        return (
            "Relevant operational logs were found. Review the log evidence items for error codes, "
            "severity levels, and service-specific failure messages."
        )

    if rule_result and rule_result.get("decision") == "ESCALATE":
        priority = rule_result.get("priority")
        reasons = rule_result.get("reasons", [])
        reason_text = " ".join(str(reason) for reason in reasons)

        return f"Escalate this incident as {priority}. {reason_text}"

    if rule_result and rule_result.get("decision") == "NO_ESCALATION":
        return (
            "No escalation is recommended based on the available evidence and escalation rules. "
            "Continue monitoring the affected service."
        )

    if evidence_quality.get("quality") in {"strong", "moderate"}:
        return (
            "The system found relevant operational evidence. No deterministic escalation decision "
            "was triggered, but the collected evidence can support further investigation."
        )

    return (
        "The request was analyzed, but the evidence was limited. Further investigation may be needed."
    )