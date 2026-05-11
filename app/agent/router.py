from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.schemas import EvidenceItem
from app.tools.log_search_tool import search_operational_logs
from app.tools.rag_tool import retrieve_policy_evidence
from app.tools.rule_validator import validate_escalation_rules
from app.tools.sql_tool import query_service_metrics


def _convert_tool_evidence(tool_result: Dict[str, Any]) -> List[EvidenceItem]:
    evidence_items: List[EvidenceItem] = []

    for item in tool_result.get("evidence", []):
        evidence_items.append(
            EvidenceItem(
                source=item["source"],
                content=item["content"],
                strength=item["strength"],
            )
        )

    return evidence_items


def execute_tool_plan(
    db: Session,
    query: str,
    selected_tools: List[str],
) -> Dict[str, Any]:
    tool_outputs: Dict[str, Any] = {}
    evidence: List[EvidenceItem] = []

    sql_result: Dict[str, Any] = {
        "tool_name": "sql_tool",
        "records_found": 0,
        "evidence": [],
        "raw_metrics": [],
    }

    log_result: Dict[str, Any] = {
        "tool_name": "log_search_tool",
        "records_found": 0,
        "evidence": [],
        "raw_logs": [],
    }

    rule_result: Dict[str, Any] | None = None

    if "sql_tool" in selected_tools:
        sql_result = query_service_metrics(db=db, query=query)
        tool_outputs["sql_tool"] = sql_result
        evidence.extend(_convert_tool_evidence(sql_result))

    if "log_search_tool" in selected_tools:
        log_result = search_operational_logs(db=db, query=query)
        tool_outputs["log_search_tool"] = log_result
        evidence.extend(_convert_tool_evidence(log_result))

    if "rag_tool" in selected_tools:
        rag_result = retrieve_policy_evidence(query=query, top_k=3)
        tool_outputs["rag_tool"] = rag_result
        evidence.extend(_convert_tool_evidence(rag_result))

    if "rule_validator" in selected_tools:
        rule_result = validate_escalation_rules(
            sql_result=sql_result,
            log_result=log_result,
        )
        tool_outputs["rule_validator"] = rule_result

    return {
        "tool_outputs": tool_outputs,
        "evidence": evidence,
        "rule_result": rule_result,
    }