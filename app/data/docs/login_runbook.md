# Login Incident Runbook

Authentication incidents affect user access and can become high priority for enterprise customers.

## Investigation Steps

1. Check auth-service error rate.
2. Search logs for AUTH_TIMEOUT or TOKEN_VALIDATION_FAILED.
3. Check if enterprise users are affected.
4. Apply SLA and escalation policies.

## Recommended Action

If authentication failures affect enterprise customers and error rate exceeds 8%, escalate to P1.