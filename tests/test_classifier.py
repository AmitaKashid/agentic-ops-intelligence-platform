from app.agent.classifier import classify_task


def test_classifies_escalation_decision():
    query = "EU customers are reporting payment failures. Should this be escalated?"
    assert classify_task(query) == "escalation_decision"


def test_classifies_policy_lookup():
    query = "What does the SLA policy say about payment failure escalation?"
    assert classify_task(query) == "policy_lookup"


def test_classifies_policy_lookup_without_escalation_wording():
    query = "What does the SLA policy say about service reliability?"
    assert classify_task(query) == "policy_lookup"


def test_classifies_sql_lookup():
    query = "What is the payment failure rate in EU?"
    assert classify_task(query) == "sql_lookup"


def test_classifies_log_analysis():
    query = "Find timeout errors in payment-service logs."
    assert classify_task(query) == "log_analysis"


def test_classifies_ambiguous_request():
    query = "Something seems wrong with the application."
    assert classify_task(query) == "ambiguous"