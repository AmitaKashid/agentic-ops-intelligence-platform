from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.db.models import OperationalLog
from app.tools.sql_tool import infer_region, infer_service


ERROR_KEYWORDS = {
    "PAYMENT_GATEWAY_TIMEOUT": ["payment", "gateway", "timeout", "checkout"],
    "AUTH_TIMEOUT": ["login", "auth", "authentication", "timeout"],
    "CHECKOUT_LATENCY_SPIKE": ["checkout", "latency", "slow"],
    "DB_CONNECTION_POOL_EXHAUSTED": ["database", "db", "connection", "pool"],
    "EMAIL_QUEUE_DELAY": ["email", "notification", "delay"],
    "SEARCH_CACHE_MISS_HIGH": ["search", "cache", "slow"],
}


def infer_error_codes(query: str) -> List[str]:
    query_lower = query.lower()
    matched_codes = []

    for error_code, keywords in ERROR_KEYWORDS.items():
        if any(keyword in query_lower for keyword in keywords):
            matched_codes.append(error_code)

    return matched_codes


def search_operational_logs(
    db: Session,
    query: str,
) -> Dict[str, Any]:
    service = infer_service(query)
    region = infer_region(query)
    error_codes = infer_error_codes(query)

    db_query = db.query(OperationalLog)

    if service:
        db_query = db_query.filter(OperationalLog.service == service)

    if region:
        db_query = db_query.filter(OperationalLog.region == region)

    logs: List[OperationalLog] = db_query.all()

    if error_codes:
        logs = [log for log in logs if log.error_code in error_codes]

    evidence = []

    for log in logs:
        strength = "strong" if log.level == "ERROR" else "moderate"

        evidence.append(
            {
                "source": "log_search_tool",
                "content": (
                    f"{log.level} log found for {log.service} in {log.region}: "
                    f"{log.error_code} - {log.message}"
                ),
                "strength": strength,
                "raw": {
                    "timestamp": log.timestamp,
                    "service": log.service,
                    "region": log.region,
                    "level": log.level,
                    "error_code": log.error_code,
                    "message": log.message,
                },
            }
        )

    return {
        "tool_name": "log_search_tool",
        "service": service,
        "region": region,
        "error_codes": error_codes,
        "records_found": len(logs),
        "evidence": evidence,
        "raw_logs": [
            {
                "timestamp": log.timestamp,
                "service": log.service,
                "region": log.region,
                "level": log.level,
                "error_code": log.error_code,
                "message": log.message,
            }
            for log in logs
        ],
    }