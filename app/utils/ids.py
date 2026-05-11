from datetime import datetime
from uuid import uuid4


def generate_trace_id() -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    suffix = str(uuid4())[:8]
    return f"trace_{timestamp}_{suffix}"


def generate_review_case_id() -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    suffix = str(uuid4())[:8]
    return f"review_{timestamp}_{suffix}"