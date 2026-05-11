# Evaluation Error Analysis
## Summary
- Total cases: 30
- Task classification accuracy: 0.8
- Tool routing exact accuracy: 0.7333
- Average tool overlap score: 0.8472
- Human-review accuracy: 0.6333
- Escalation/decision accuracy: 0.6
- Average latency ms: 153.62

## Failed or Partially Failed Cases

### Case 6
Query: What is the payment failure rate in EU?
- Expected task type: sql_lookup
- Actual task type: sql_lookup
- Expected tools: sql_tool
- Actual tools: sql_tool
- Expected human review: False
- Actual human review: True
- Expected decision: NO_ESCALATION
- Actual decision: HUMAN_REVIEW
- Confidence: 0.43
- Trace ID: trace_20260511_170111_30f98134

### Case 7
Query: How many affected customers does checkout-service have in EU?
- Expected task type: sql_lookup
- Actual task type: sql_lookup
- Expected tools: sql_tool
- Actual tools: sql_tool
- Expected human review: False
- Actual human review: True
- Expected decision: NO_ESCALATION
- Actual decision: HUMAN_REVIEW
- Confidence: 0.43
- Trace ID: trace_20260511_170111_a0943856

### Case 8
Query: Show the latency for database-service in EU.
- Expected task type: sql_lookup
- Actual task type: sql_lookup
- Expected tools: sql_tool
- Actual tools: sql_tool
- Expected human review: False
- Actual human review: True
- Expected decision: NO_ESCALATION
- Actual decision: HUMAN_REVIEW
- Confidence: 0.43
- Trace ID: trace_20260511_170112_8e1fe03a

### Case 9
Query: What is the error rate for auth-service in EU?
- Expected task type: sql_lookup
- Actual task type: sql_lookup
- Expected tools: sql_tool
- Actual tools: log_search_tool;sql_tool
- Expected human review: False
- Actual human review: False
- Expected decision: NO_ESCALATION
- Actual decision: NO_ESCALATION
- Confidence: 0.66
- Trace ID: trace_20260511_170112_44bfcdf7

### Case 10
Query: How many failed requests happened for payment-service in US?
- Expected task type: sql_lookup
- Actual task type: sql_lookup
- Expected tools: sql_tool
- Actual tools: sql_tool
- Expected human review: False
- Actual human review: True
- Expected decision: NO_ESCALATION
- Actual decision: HUMAN_REVIEW
- Confidence: 0.37
- Trace ID: trace_20260511_170112_07c5606a

### Case 11
Query: Find timeout errors for payment-service in EU logs.
- Expected task type: log_analysis
- Actual task type: log_analysis
- Expected tools: log_search_tool
- Actual tools: log_search_tool
- Expected human review: False
- Actual human review: True
- Expected decision: NO_ESCALATION
- Actual decision: HUMAN_REVIEW
- Confidence: 0.56
- Trace ID: trace_20260511_170112_6b8343c8

### Case 12
Query: Search logs for AUTH_TIMEOUT in EU.
- Expected task type: log_analysis
- Actual task type: log_analysis
- Expected tools: log_search_tool
- Actual tools: log_search_tool
- Expected human review: False
- Actual human review: True
- Expected decision: NO_ESCALATION
- Actual decision: HUMAN_REVIEW
- Confidence: 0.43
- Trace ID: trace_20260511_170112_cc420659

### Case 13
Query: Find database connection pool errors.
- Expected task type: log_analysis
- Actual task type: log_analysis
- Expected tools: log_search_tool
- Actual tools: log_search_tool
- Expected human review: False
- Actual human review: True
- Expected decision: NO_ESCALATION
- Actual decision: HUMAN_REVIEW
- Confidence: 0.43
- Trace ID: trace_20260511_170112_f1bc8f2d

### Case 14
Query: Show checkout latency spike logs.
- Expected task type: log_analysis
- Actual task type: sql_lookup
- Expected tools: log_search_tool
- Actual tools: log_search_tool;sql_tool
- Expected human review: False
- Actual human review: False
- Expected decision: NO_ESCALATION
- Actual decision: NO_ESCALATION
- Confidence: 0.66
- Trace ID: trace_20260511_170112_b52c1804

### Case 15
Query: Find notification delay logs in US.
- Expected task type: log_analysis
- Actual task type: log_analysis
- Expected tools: log_search_tool
- Actual tools: log_search_tool
- Expected human review: False
- Actual human review: True
- Expected decision: NO_ESCALATION
- Actual decision: HUMAN_REVIEW
- Confidence: 0.37
- Trace ID: trace_20260511_170112_bcee33a8

### Case 16
Query: What does the SLA policy say about payment failure escalation?
- Expected task type: policy_lookup
- Actual task type: policy_lookup
- Expected tools: rag_tool
- Actual tools: rag_tool;rule_validator
- Expected human review: False
- Actual human review: True
- Expected decision: NO_ESCALATION
- Actual decision: HUMAN_REVIEW
- Confidence: 0.56
- Trace ID: trace_20260511_170112_eee0d930

### Case 17
Query: What does the escalation policy say about P1 incidents?
- Expected task type: policy_lookup
- Actual task type: escalation_decision
- Expected tools: rag_tool
- Actual tools: log_search_tool;rag_tool;rule_validator;sql_tool
- Expected human review: False
- Actual human review: False
- Expected decision: NO_ESCALATION
- Actual decision: ESCALATE
- Confidence: 0.95
- Trace ID: trace_20260511_170112_7cf005f8

### Case 18
Query: What does the payment runbook recommend for gateway timeouts?
- Expected task type: policy_lookup
- Actual task type: policy_lookup
- Expected tools: rag_tool
- Actual tools: log_search_tool;rag_tool
- Expected human review: False
- Actual human review: False
- Expected decision: NO_ESCALATION
- Actual decision: NO_ESCALATION
- Confidence: 0.93
- Trace ID: trace_20260511_170112_14210ddb

### Case 19
Query: What does the database incident runbook say about connection pool exhaustion?
- Expected task type: policy_lookup
- Actual task type: policy_lookup
- Expected tools: rag_tool
- Actual tools: rag_tool
- Expected human review: False
- Actual human review: True
- Expected decision: NO_ESCALATION
- Actual decision: HUMAN_REVIEW
- Confidence: 0.57
- Trace ID: trace_20260511_170112_a3742168

### Case 25
Query: Users are complaining but there is no clear service name.
- Expected task type: investigation
- Actual task type: ambiguous
- Expected tools: log_search_tool;rag_tool;sql_tool
- Actual tools: human_review_tool
- Expected human review: True
- Actual human review: True
- Expected decision: HUMAN_REVIEW
- Actual decision: HUMAN_REVIEW
- Confidence: 0.2
- Trace ID: trace_20260511_170112_ca74076f

### Case 27
Query: Compare the escalation policy and SLA policy for customer-facing incidents.
- Expected task type: comparison
- Actual task type: comparison
- Expected tools: rag_tool;sql_tool
- Actual tools: rag_tool;rule_validator;sql_tool
- Expected human review: False
- Actual human review: False
- Expected decision: NO_ESCALATION
- Actual decision: NO_ESCALATION
- Confidence: 0.95
- Trace ID: trace_20260511_170112_1670b5e0

### Case 28
Query: Summarize the login incident runbook.
- Expected task type: summarization
- Actual task type: policy_lookup
- Expected tools: rag_tool
- Actual tools: log_search_tool;rag_tool
- Expected human review: False
- Actual human review: False
- Expected decision: NO_ESCALATION
- Actual decision: NO_ESCALATION
- Confidence: 0.79
- Trace ID: trace_20260511_170112_5917785f

### Case 29
Query: Give me an overview of the payment incident runbook.
- Expected task type: summarization
- Actual task type: policy_lookup
- Expected tools: rag_tool
- Actual tools: rag_tool
- Expected human review: False
- Actual human review: False
- Expected decision: NO_ESCALATION
- Actual decision: NO_ESCALATION
- Confidence: 0.69
- Trace ID: trace_20260511_170112_15fa8b0b

### Case 30
Query: Explain the database incident runbook.
- Expected task type: summarization
- Actual task type: policy_lookup
- Expected tools: rag_tool
- Actual tools: rag_tool
- Expected human review: False
- Actual human review: True
- Expected decision: NO_ESCALATION
- Actual decision: HUMAN_REVIEW
- Confidence: 0.63
- Trace ID: trace_20260511_170112_f4157350
