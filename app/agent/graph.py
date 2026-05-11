from typing import Any, Dict

from langgraph.graph import END, START, StateGraph

from app.agent.classifier import classify_task
from app.agent.confidence import calculate_confidence_score
from app.agent.evidence_verifier import verify_evidence_quality
from app.agent.planner import create_tool_plan
from app.agent.response_generator import generate_final_recommendation
from app.agent.router import execute_tool_plan
from app.agent.state import AgentState
from app.observability.trace_logger import write_trace
from app.tools.human_review_tool import (
    create_review_case_if_needed,
    should_send_to_human_review,
)
from app.utils.ids import generate_trace_id


def classify_node(state: AgentState) -> Dict[str, Any]:
    task_type = classify_task(state["query"])

    return {
        "task_type": task_type,
    }


def plan_node(state: AgentState) -> Dict[str, Any]:
    plan = create_tool_plan(
        task_type=state["task_type"],
        query=state["query"],
    )

    return {
        "selected_tools": plan["selected_tools"],
        "planner_reasons": plan["reasons"],
    }


def route_tools_node(state: AgentState) -> Dict[str, Any]:
    routed_result = execute_tool_plan(
        db=state["db"],
        query=state["query"],
        selected_tools=state["selected_tools"],
    )

    return {
        "tool_outputs": routed_result["tool_outputs"],
        "evidence": routed_result["evidence"],
        "rule_result": routed_result["rule_result"],
    }


def verify_evidence_node(state: AgentState) -> Dict[str, Any]:
    evidence_quality = verify_evidence_quality(
        evidence=state.get("evidence", []),
    )

    return {
        "evidence_quality": evidence_quality,
    }


def confidence_node(state: AgentState) -> Dict[str, Any]:
    rule_result = state.get("rule_result")

    matched_rules = []
    rule_decision = None

    if rule_result:
        matched_rules = rule_result.get("matched_rules", [])
        rule_decision = rule_result.get("decision")

    confidence = calculate_confidence_score(
        evidence=state.get("evidence", []),
        rule_decision=rule_decision,
        matched_rules=matched_rules,
        evidence_quality=state["evidence_quality"],
    )

    return {
        "confidence": confidence,
    }


def human_review_node(state: AgentState) -> Dict[str, Any]:
    rule_result = state.get("rule_result")

    rule_decision = "NO_RULE_DECISION"
    if rule_result:
        rule_decision = rule_result.get("decision", "NO_RULE_DECISION")

    human_review_required = should_send_to_human_review(
        confidence=state["confidence"],
        rule_decision=rule_decision,
        evidence_count=len(state.get("evidence", [])),
    )

    if state.get("task_type") == "ambiguous":
        human_review_required = True

    review_case_id = None

    if human_review_required:
        review_reason = (
            state.get("evidence_quality", {}).get("reason")
            or "Low confidence, ambiguous request, or insufficient evidence."
        )

        review_case = create_review_case_if_needed(
            db=state["db"],
            query=state["query"],
            confidence=state["confidence"],
            human_review_required=human_review_required,
            reason=review_reason,
        )

        review_case_id = review_case.case_id if review_case else None

    return {
        "human_review_required": human_review_required,
        "human_review_case_id": review_case_id,
    }


def response_node(state: AgentState) -> Dict[str, Any]:
    recommendation = generate_final_recommendation(
        task_type=state["task_type"],
        rule_result=state.get("rule_result"),
        evidence=state.get("evidence", []),
        evidence_quality=state.get("evidence_quality", {}),
        human_review_required=state["human_review_required"],
    )

    return {
        "recommendation": recommendation,
    }


def trace_node(state: AgentState) -> Dict[str, Any]:
    trace_payload = {
        "trace_id": state["trace_id"],
        "ticket_id": state.get("ticket_id"),
        "query": state["query"],
        "task_type": state["task_type"],
        "planner": {
            "selected_tools": state.get("selected_tools", []),
            "reasons": state.get("planner_reasons", []),
        },
        "tool_outputs": state.get("tool_outputs", {}),
        "evidence_quality": state.get("evidence_quality", {}),
        "confidence": state.get("confidence"),
        "human_review_required": state.get("human_review_required"),
        "human_review_case_id": state.get("human_review_case_id"),
        "recommendation": state.get("recommendation"),
    }

    write_trace(
        db=state["db"],
        trace_id=state["trace_id"],
        query=state["query"],
        task_type=state["task_type"],
        selected_tools=state.get("selected_tools", []),
        confidence=state["confidence"],
        human_review_required=state["human_review_required"],
        final_decision=state["recommendation"],
        trace_payload=trace_payload,
    )

    return {}


def build_agent_graph():
    graph = StateGraph(AgentState)

    graph.add_node("classify", classify_node)
    graph.add_node("plan", plan_node)
    graph.add_node("route_tools", route_tools_node)
    graph.add_node("verify_evidence", verify_evidence_node)
    graph.add_node("calculate_confidence", confidence_node)
    graph.add_node("human_review", human_review_node)
    graph.add_node("generate_response", response_node)
    graph.add_node("write_trace", trace_node)

    graph.add_edge(START, "classify")
    graph.add_edge("classify", "plan")
    graph.add_edge("plan", "route_tools")
    graph.add_edge("route_tools", "verify_evidence")
    graph.add_edge("verify_evidence", "calculate_confidence")
    graph.add_edge("calculate_confidence", "human_review")
    graph.add_edge("human_review", "generate_response")
    graph.add_edge("generate_response", "write_trace")
    graph.add_edge("write_trace", END)

    return graph.compile()


agent_graph = build_agent_graph()


def run_agent_workflow(
    db,
    query: str,
    ticket_id: str | None = None,
) -> AgentState:
    initial_state: AgentState = {
        "query": query,
        "ticket_id": ticket_id,
        "trace_id": generate_trace_id(),
        "db": db,
    }

    final_state = agent_graph.invoke(initial_state)

    return final_state