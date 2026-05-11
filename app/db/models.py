from sqlalchemy import Boolean, Column, Float, Integer, String, Text, DateTime
from datetime import datetime

from app.db.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True)
    timestamp = Column(String)
    customer_tier = Column(String)
    service = Column(String, index=True)
    region = Column(String, index=True)
    description = Column(Text)
    status = Column(String, default="open")


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String, unique=True, index=True)
    ticket_id = Column(String, index=True)
    priority = Column(String)
    service = Column(String, index=True)
    region = Column(String, index=True)
    status = Column(String)
    summary = Column(Text)


class ServiceMetric(Base):
    __tablename__ = "service_metrics"

    id = Column(Integer, primary_key=True, index=True)
    metric_id = Column(String, unique=True, index=True)
    service = Column(String, index=True)
    region = Column(String, index=True)
    timestamp = Column(String)
    error_rate = Column(Float)
    latency_ms = Column(Float)
    failed_requests = Column(Integer)
    total_requests = Column(Integer)
    affected_customers = Column(Integer)
    enterprise_customers_affected = Column(Integer)


class OperationalLog(Base):
    __tablename__ = "operational_logs"

    id = Column(Integer, primary_key=True, index=True)
    log_id = Column(String, unique=True, index=True)
    timestamp = Column(String)
    service = Column(String, index=True)
    region = Column(String, index=True)
    level = Column(String)
    error_code = Column(String, index=True)
    message = Column(Text)


class HumanReviewCase(Base):
    __tablename__ = "human_review_cases"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String, unique=True, index=True)
    query = Column(Text)
    reason = Column(Text)
    confidence = Column(Float)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)


class AgentTrace(Base):
    __tablename__ = "agent_traces"

    id = Column(Integer, primary_key=True, index=True)
    trace_id = Column(String, unique=True, index=True)
    query = Column(Text)
    task_type = Column(String)
    selected_tools = Column(Text)
    confidence = Column(Float)
    human_review_required = Column(Boolean)
    final_decision = Column(Text)
    trace_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)