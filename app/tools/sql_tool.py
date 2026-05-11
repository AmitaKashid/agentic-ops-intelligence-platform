from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.db.models import ServiceMetric


SERVICE_KEYWORDS = {
    "payment-service": ["payment", "payments", "checkout payment", "billing"],
    "auth-service": ["auth", "login", "authentication", "sign in", "signin"],
    "checkout-service": ["checkout", "cart", "purchase"],
    "database-service": ["database", "db", "connection pool", "sql"],
    "notification-service": ["notification", "email", "mail"],
    "search-service": ["search", "query results", "search results"],
}

REGION_KEYWORDS = {
    "EU": ["eu", "europe", "european"],
    "US": ["us", "usa", "america", "american"],
}


def infer_service(query: str) -> Optional[str]:
    query_lower = query.lower()

    for service, keywords in SERVICE_KEYWORDS.items():
        if any(keyword in query_lower for keyword in keywords):
            return service

    return None


def infer_region(query: str) -> Optional[str]:
    query_lower = query.lower()

    for region, keywords in REGION_KEYWORDS.items():
        if any(keyword in query_lower for keyword in keywords):
            return region

    return None


def query_service_metrics(
    db: Session,
    query: str,
) -> Dict[str, Any]:
    service = infer_service(query)
    region = infer_region(query)

    db_query = db.query(ServiceMetric)

    if service:
        db_query = db_query.filter(ServiceMetric.service == service)

    if region:
        db_query = db_query.filter(ServiceMetric.region == region)

    metrics: List[ServiceMetric] = db_query.all()

    evidence = []

    for metric in metrics:
        evidence.append(
            {
                "source": "sql_tool",
                "content": (
                    f"{metric.service} in {metric.region} has error rate "
                    f"{metric.error_rate * 100:.1f}%, latency {metric.latency_ms:.0f} ms, "
                    f"{metric.failed_requests} failed requests, "
                    f"{metric.affected_customers} affected customers, and "
                    f"{metric.enterprise_customers_affected} affected enterprise customers."
                ),
                "strength": "strong"
                if metric.error_rate >= 0.07 or metric.affected_customers >= 50
                else "moderate",
                "raw": {
                    "service": metric.service,
                    "region": metric.region,
                    "error_rate": metric.error_rate,
                    "latency_ms": metric.latency_ms,
                    "failed_requests": metric.failed_requests,
                    "total_requests": metric.total_requests,
                    "affected_customers": metric.affected_customers,
                    "enterprise_customers_affected": metric.enterprise_customers_affected,
                },
            }
        )

    return {
        "tool_name": "sql_tool",
        "service": service,
        "region": region,
        "records_found": len(metrics),
        "evidence": evidence,
        "raw_metrics": [
            {
                "service": metric.service,
                "region": metric.region,
                "error_rate": metric.error_rate,
                "latency_ms": metric.latency_ms,
                "failed_requests": metric.failed_requests,
                "total_requests": metric.total_requests,
                "affected_customers": metric.affected_customers,
                "enterprise_customers_affected": metric.enterprise_customers_affected,
            }
            for metric in metrics
        ],
    }