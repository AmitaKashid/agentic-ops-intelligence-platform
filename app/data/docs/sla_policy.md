# SLA Policy

Customer-facing incidents must be escalated when they exceed service reliability thresholds.

## Escalation Thresholds

- Payment failure rate above 10% requires P1 escalation.
- Checkout latency above 1000 ms for more than 10 minutes requires P2 escalation.
- Authentication failure rate above 8% for enterprise customers requires P1 escalation.
- Database error rate above 7% with customer impact requires P2 escalation.
- Enterprise customer impact increases the priority of an incident.

## Human Review Conditions

Send a case to human review if:

- Evidence is missing from both metrics and logs.
- Policy evidence conflicts with operational metrics.
- The request is ambiguous.
- The recommended action is high risk but confidence is below 0.70.