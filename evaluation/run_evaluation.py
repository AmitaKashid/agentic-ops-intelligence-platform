import json
import time
from pathlib import Path
from typing import List, Set

import pandas as pd

from app.agent.graph import run_agent_workflow
from app.db.database import Base, SessionLocal, engine
from app.db.seed import seed_database


BENCHMARK_PATH = Path("evaluation/benchmark_queries.csv")
RESULTS_PATH = Path("evaluation/results.csv")
SUMMARY_PATH = Path("evaluation/metrics_summary.json")
ERROR_ANALYSIS_PATH = Path("evaluation/error_analysis.md")


def parse_expected_tools(value: str) -> Set[str]:
    if not isinstance(value, str) or not value.strip():
        return set()

    return set(tool.strip() for tool in value.split(";") if tool.strip())


def normalize_bool(value) -> bool:
    if isinstance(value, bool):
        return value

    value_str = str(value).strip().lower()
    return value_str in {"true", "1", "yes"}


def infer_decision_from_state(final_state: dict) -> str:
    if final_state.get("human_review_required"):
        return "HUMAN_REVIEW"

    rule_result = final_state.get("rule_result")

    if rule_result:
        return rule_result.get("decision", "NO_ESCALATION")

    return "NO_ESCALATION"


def tools_match(expected_tools: Set[str], actual_tools: Set[str]) -> bool:
    return expected_tools == actual_tools


def tools_overlap_score(expected_tools: Set[str], actual_tools: Set[str]) -> float:
    if not expected_tools and not actual_tools:
        return 1.0

    if not expected_tools or not actual_tools:
        return 0.0

    intersection = expected_tools.intersection(actual_tools)
    union = expected_tools.union(actual_tools)

    return len(intersection) / len(union)


def run_single_case(row: pd.Series) -> dict:
    db = SessionLocal()

    try:
        query = row["query"]
        ticket_id = row["ticket_id"] if isinstance(row["ticket_id"], str) and row["ticket_id"] else None

        start_time = time.perf_counter()

        final_state = run_agent_workflow(
            db=db,
            query=query,
            ticket_id=ticket_id,
        )

        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        expected_tools = parse_expected_tools(row["expected_tools"])
        actual_tools = set(final_state.get("selected_tools", []))

        expected_task_type = row["expected_task_type"]
        actual_task_type = final_state.get("task_type")

        expected_human_review = normalize_bool(row["expected_human_review"])
        actual_human_review = bool(final_state.get("human_review_required"))

        expected_priority = row["expected_priority"] if isinstance(row["expected_priority"], str) else ""
        actual_priority = ""

        rule_result = final_state.get("rule_result")
        if rule_result:
            actual_priority = rule_result.get("priority") or ""

        expected_decision = row["expected_decision"]
        actual_decision = infer_decision_from_state(final_state)

        return {
            "id": row["id"],
            "query": query,
            "expected_task_type": expected_task_type,
            "actual_task_type": actual_task_type,
            "task_type_correct": expected_task_type == actual_task_type,
            "expected_tools": ";".join(sorted(expected_tools)),
            "actual_tools": ";".join(sorted(actual_tools)),
            "tools_exact_match": tools_match(expected_tools, actual_tools),
            "tools_overlap_score": round(tools_overlap_score(expected_tools, actual_tools), 3),
            "expected_human_review": expected_human_review,
            "actual_human_review": actual_human_review,
            "human_review_correct": expected_human_review == actual_human_review,
            "expected_priority": expected_priority,
            "actual_priority": actual_priority,
            "priority_correct": expected_priority == actual_priority if expected_priority else True,
            "expected_decision": expected_decision,
            "actual_decision": actual_decision,
            "decision_correct": expected_decision == actual_decision,
            "confidence": final_state.get("confidence"),
            "evidence_count": len(final_state.get("evidence", [])),
            "latency_ms": latency_ms,
            "trace_id": final_state.get("trace_id"),
        }

    finally:
        db.close()


def calculate_accuracy(series: pd.Series) -> float:
    if len(series) == 0:
        return 0.0

    return round(float(series.mean()), 4)


def write_error_analysis(results_df: pd.DataFrame, summary: dict) -> None:
    failed_cases = results_df[
        ~(
            results_df["task_type_correct"]
            & results_df["tools_exact_match"]
            & results_df["human_review_correct"]
            & results_df["decision_correct"]
        )
    ]

    lines: List[str] = []

    lines.append("# Evaluation Error Analysis\n")
    lines.append("## Summary\n")
    lines.append(f"- Total cases: {summary['total_cases']}\n")
    lines.append(f"- Task classification accuracy: {summary['task_classification_accuracy']}\n")
    lines.append(f"- Tool routing exact accuracy: {summary['tool_routing_exact_accuracy']}\n")
    lines.append(f"- Average tool overlap score: {summary['average_tool_overlap_score']}\n")
    lines.append(f"- Human-review accuracy: {summary['human_review_accuracy']}\n")
    lines.append(f"- Escalation/decision accuracy: {summary['decision_accuracy']}\n")
    lines.append(f"- Average latency ms: {summary['average_latency_ms']}\n")

    lines.append("\n## Failed or Partially Failed Cases\n")

    if failed_cases.empty:
        lines.append("\nNo failed cases found in this benchmark run.\n")
    else:
        for _, row in failed_cases.iterrows():
            lines.append(f"\n### Case {row['id']}\n")
            lines.append(f"Query: {row['query']}\n")
            lines.append(f"- Expected task type: {row['expected_task_type']}\n")
            lines.append(f"- Actual task type: {row['actual_task_type']}\n")
            lines.append(f"- Expected tools: {row['expected_tools']}\n")
            lines.append(f"- Actual tools: {row['actual_tools']}\n")
            lines.append(f"- Expected human review: {row['expected_human_review']}\n")
            lines.append(f"- Actual human review: {row['actual_human_review']}\n")
            lines.append(f"- Expected decision: {row['expected_decision']}\n")
            lines.append(f"- Actual decision: {row['actual_decision']}\n")
            lines.append(f"- Confidence: {row['confidence']}\n")
            lines.append(f"- Trace ID: {row['trace_id']}\n")

    ERROR_ANALYSIS_PATH.write_text("".join(lines), encoding="utf-8")


def main():
    if not BENCHMARK_PATH.exists():
        raise FileNotFoundError(f"Benchmark file not found: {BENCHMARK_PATH}")

    Base.metadata.create_all(bind=engine)
    seed_database()

    benchmark_df = pd.read_csv(BENCHMARK_PATH).fillna("")

    results = []

    for _, row in benchmark_df.iterrows():
        print(f"Evaluating case {row['id']}: {row['query']}")
        result = run_single_case(row)
        results.append(result)

    results_df = pd.DataFrame(results)
    results_df.to_csv(RESULTS_PATH, index=False)

    summary = {
        "total_cases": int(len(results_df)),
        "task_classification_accuracy": calculate_accuracy(results_df["task_type_correct"]),
        "tool_routing_exact_accuracy": calculate_accuracy(results_df["tools_exact_match"]),
        "average_tool_overlap_score": round(float(results_df["tools_overlap_score"].mean()), 4),
        "human_review_accuracy": calculate_accuracy(results_df["human_review_correct"]),
        "priority_accuracy": calculate_accuracy(results_df["priority_correct"]),
        "decision_accuracy": calculate_accuracy(results_df["decision_correct"]),
        "average_confidence": round(float(results_df["confidence"].mean()), 4),
        "average_latency_ms": round(float(results_df["latency_ms"].mean()), 2),
        "p95_latency_ms": round(float(results_df["latency_ms"].quantile(0.95)), 2),
    }

    SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    write_error_analysis(results_df, summary)

    print("\nEvaluation complete.")
    print(json.dumps(summary, indent=2))
    print(f"\nResults written to: {RESULTS_PATH}")
    print(f"Summary written to: {SUMMARY_PATH}")
    print(f"Error analysis written to: {ERROR_ANALYSIS_PATH}")


if __name__ == "__main__":
    main()