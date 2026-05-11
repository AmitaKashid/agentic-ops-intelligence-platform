from typing import Dict, List

from app.schemas import EvidenceItem


def verify_evidence_quality(evidence: List[EvidenceItem]) -> Dict[str, object]:
    strong_count = sum(1 for item in evidence if item.strength == "strong")
    moderate_count = sum(1 for item in evidence if item.strength == "moderate")
    weak_count = sum(1 for item in evidence if item.strength == "weak")

    evidence_sources = sorted(set(item.source for item in evidence))

    if not evidence:
        quality = "missing"
        reason = "No evidence was collected from selected tools."

    elif strong_count >= 2 and len(evidence_sources) >= 2:
        quality = "strong"
        reason = "Multiple strong evidence items were collected from different sources."

    elif strong_count >= 1:
        quality = "moderate"
        reason = "At least one strong evidence item was collected."

    elif moderate_count >= 1:
        quality = "moderate"
        reason = "Only moderate evidence was collected."

    else:
        quality = "weak"
        reason = "Only weak evidence was collected."

    return {
        "quality": quality,
        "reason": reason,
        "strong_count": strong_count,
        "moderate_count": moderate_count,
        "weak_count": weak_count,
        "sources": evidence_sources,
        "evidence_count": len(evidence),
    }