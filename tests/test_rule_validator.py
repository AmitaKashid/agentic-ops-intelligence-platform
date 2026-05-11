from app.tools.rule_validator import validate_escalation_rules


def test_payment_error_rate_triggers_p1():
    sql_result = {
        "raw_metrics": [
            {
                "service": "payment-service",
                "error_rate": 0.187,
                "latency_ms": 920,
                "affected_customers": 74,
                "enterprise_customers_affected": 12,
            }
        ]
    }

    log_result = {
        "raw_logs": [
            {
                "level": "ERROR",
                "error_code": "PAYMENT_GATEWAY_TIMEOUT",
            }
        ]
    }

    result = validate_escalation_rules(sql_result, log_result)

    assert result["decision"] == "ESCALATE"
    assert result["priority"] == "P1"
    assert "payment_failure_rate_above_10_percent" in result["matched_rules"]


def test_checkout_latency_triggers_p2():
    sql_result = {
        "raw_metrics": [
            {
                "service": "checkout-service",
                "error_rate": 0.04,
                "latency_ms": 1420,
                "affected_customers": 40,
                "enterprise_customers_affected": 5,
            }
        ]
    }

    log_result = {"raw_logs": []}

    result = validate_escalation_rules(sql_result, log_result)

    assert result["decision"] == "ESCALATE"
    assert result["priority"] == "P2"
    assert "checkout_latency_above_1000ms" in result["matched_rules"]


def test_missing_metrics_and_logs_goes_to_human_review():
    sql_result = {"raw_metrics": []}
    log_result = {"raw_logs": []}

    result = validate_escalation_rules(sql_result, log_result)

    assert result["decision"] == "HUMAN_REVIEW"
    assert result["priority"] is None
    assert "missing_metrics_and_logs" in result["matched_rules"]


def test_low_impact_notification_issue_does_not_escalate():
    sql_result = {
        "raw_metrics": [
            {
                "service": "notification-service",
                "error_rate": 0.026,
                "latency_ms": 280,
                "affected_customers": 9,
                "enterprise_customers_affected": 1,
            }
        ]
    }

    log_result = {
        "raw_logs": [
            {
                "level": "INFO",
                "error_code": "EMAIL_QUEUE_DELAY",
            }
        ]
    }

    result = validate_escalation_rules(sql_result, log_result)

    assert result["decision"] == "NO_ESCALATION"
    assert result["priority"] == "P3"