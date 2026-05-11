# Escalation Policy

Incidents are escalated based on customer impact, service criticality, and operational severity.

## P1 Escalation

Use P1 when:

- Payment systems are failing for production customers.
- Authentication is unavailable for enterprise customers.
- More than 50 customers are affected by a critical service issue.
- A customer-facing incident causes direct revenue impact.

## P2 Escalation

Use P2 when:

- Checkout latency is above threshold but payments are still working.
- Database instability affects part of the application.
- Search or notification issues affect user experience but do not block core workflows.

## No Escalation

Do not escalate if:

- The issue has low customer impact.
- There is no supporting evidence in metrics, logs, or policies.
- The issue is informational only.