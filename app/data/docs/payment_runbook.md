# Payment Incident Runbook

Payment incidents should be investigated immediately because they may cause revenue loss.

## Investigation Steps

1. Check payment-service error rate.
2. Search logs for PAYMENT_GATEWAY_TIMEOUT.
3. Check whether the affected region has elevated failed requests.
4. Confirm whether enterprise customers are affected.
5. Apply the SLA escalation policy.

## Common Error Codes

- PAYMENT_GATEWAY_TIMEOUT
- PAYMENT_AUTHORIZATION_FAILED
- RETRY_LIMIT_REACHED

## Recommended Action

If payment failure rate is above 10% and logs confirm gateway timeout errors, escalate to P1 incident response.