from typing import Any, Dict, List


def validate_escalation_rules(
    sql_result: Dict[str, Any],
    log_result: Dict[str, Any],
) -> Dict[str, Any]:
    matched_rules: List[str] = []
    reasons: List[str] = []

    priority = "P3"
    decision = "NO_ESCALATION"

    raw_metrics = sql_result.get("raw_metrics", [])
    raw_logs = log_result.get("raw_logs", [])

    has_error_logs = any(log.get("level") == "ERROR" for log in raw_logs)

    for metric in raw_metrics:
        service = metric["service"]
        error_rate = metric["error_rate"]
        latency_ms = metric["latency_ms"]
        affected_customers = metric["affected_customers"]
        enterprise_customers_affected = metric["enterprise_customers_affected"]

        if service == "payment-service" and error_rate > 0.10:
            matched_rules.append("payment_failure_rate_above_10_percent")
            reasons.append(
                f"Payment-service error rate is {error_rate * 100:.1f}%, above the 10% P1 threshold."
            )
            decision = "ESCALATE"
            priority = "P1"

        if service == "auth-service" and error_rate > 0.08:
            matched_rules.append("auth_failure_rate_above_8_percent")
            reasons.append(
                f"Auth-service error rate is {error_rate * 100:.1f}%, above the 8% enterprise login threshold."
            )
            decision = "ESCALATE"
            priority = "P1"

        if service == "checkout-service" and latency_ms > 1000:
            matched_rules.append("checkout_latency_above_1000ms")
            reasons.append(
                f"Checkout latency is {latency_ms:.0f} ms, above the 1000 ms P2 threshold."
            )
            decision = "ESCALATE"
            if priority != "P1":
                priority = "P2"

        if service == "database-service" and error_rate > 0.07:
            matched_rules.append("database_error_rate_above_7_percent")
            reasons.append(
                f"Database-service error rate is {error_rate * 100:.1f}%, above the 7% threshold."
            )
            decision = "ESCALATE"
            if priority != "P1":
                priority = "P2"

        if affected_customers > 50:
            matched_rules.append("affected_customers_above_50")
            reasons.append(
                f"{affected_customers} customers are affected, which increases incident severity."
            )
            decision = "ESCALATE"
            if priority == "P3":
                priority = "P2"

        if enterprise_customers_affected > 10:
            matched_rules.append("enterprise_customers_above_10")
            reasons.append(
                f"{enterprise_customers_affected} enterprise customers are affected, which increases priority."
            )
            decision = "ESCALATE"
            priority = "P1"

    if has_error_logs:
        matched_rules.append("error_logs_present")
        reasons.append("Error-level logs were found for the affected service.")

    if not raw_metrics and not raw_logs:
        matched_rules.append("missing_metrics_and_logs")
        reasons.append("No matching metrics or logs were found.")
        decision = "HUMAN_REVIEW"
        priority = None

    elif raw_metrics and not raw_logs:
        matched_rules.append("metrics_without_log_confirmation")
        reasons.append("Metrics were found, but no supporting logs were found.")

    elif raw_logs and not raw_metrics:
        matched_rules.append("logs_without_metric_confirmation")
        reasons.append("Logs were found, but no matching service metrics were found.")

    return {
        "tool_name": "rule_validator",
        "decision": decision,
        "priority": priority,
        "matched_rules": list(dict.fromkeys(matched_rules)),
        "reasons": reasons,
    }