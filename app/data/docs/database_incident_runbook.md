# Database Incident Runbook

Database incidents may affect multiple downstream services.

## Investigation Steps

1. Check database-service error rate.
2. Search logs for DB_CONNECTION_POOL_EXHAUSTED.
3. Check latency and failed request volume.
4. Identify affected services and regions.

## Recommended Action

If database error rate is above 7% and customers are affected, escalate to P2 or higher depending on business impact.