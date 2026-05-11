import pandas as pd

from app.db.database import Base, engine, SessionLocal
from app.db.models import Ticket, Incident, ServiceMetric, OperationalLog


def seed_tickets(db):
    df = pd.read_csv("app/data/tickets.csv")
    for _, row in df.iterrows():
        exists = db.query(Ticket).filter(Ticket.ticket_id == row["ticket_id"]).first()
        if exists:
            continue

        db.add(
            Ticket(
                ticket_id=row["ticket_id"],
                timestamp=row["timestamp"],
                customer_tier=row["customer_tier"],
                service=row["service"],
                region=row["region"],
                description=row["description"],
                status=row["status"],
            )
        )


def seed_incidents(db):
    df = pd.read_csv("app/data/incidents.csv")
    for _, row in df.iterrows():
        exists = db.query(Incident).filter(Incident.incident_id == row["incident_id"]).first()
        if exists:
            continue

        db.add(
            Incident(
                incident_id=row["incident_id"],
                ticket_id=row["ticket_id"],
                priority=row["priority"],
                service=row["service"],
                region=row["region"],
                status=row["status"],
                summary=row["summary"],
            )
        )


def seed_service_metrics(db):
    df = pd.read_csv("app/data/service_metrics.csv")
    for _, row in df.iterrows():
        exists = db.query(ServiceMetric).filter(ServiceMetric.metric_id == row["metric_id"]).first()
        if exists:
            continue

        db.add(
            ServiceMetric(
                metric_id=row["metric_id"],
                service=row["service"],
                region=row["region"],
                timestamp=row["timestamp"],
                error_rate=float(row["error_rate"]),
                latency_ms=float(row["latency_ms"]),
                failed_requests=int(row["failed_requests"]),
                total_requests=int(row["total_requests"]),
                affected_customers=int(row["affected_customers"]),
                enterprise_customers_affected=int(row["enterprise_customers_affected"]),
            )
        )


def seed_logs(db):
    df = pd.read_csv("app/data/logs.csv")
    for _, row in df.iterrows():
        exists = db.query(OperationalLog).filter(OperationalLog.log_id == row["log_id"]).first()
        if exists:
            continue

        db.add(
            OperationalLog(
                log_id=row["log_id"],
                timestamp=row["timestamp"],
                service=row["service"],
                region=row["region"],
                level=row["level"],
                error_code=row["error_code"],
                message=row["message"],
            )
        )


def seed_database():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_tickets(db)
        seed_incidents(db)
        seed_service_metrics(db)
        seed_logs(db)
        db.commit()
        print("Database seeded successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()