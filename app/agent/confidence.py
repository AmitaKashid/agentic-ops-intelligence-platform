from typing import Dict, List

from app.schemas import EvidenceItem


def calculate_confidence_score(
    evidence: List[EvidenceItem],
    rule_decision: str | None,
    matched_rules: List[str],
    evidence_quality: Dict[str, object],
) -> float:
    if not evidence:
        return 0.20

    confidence = 0.30

    strong_count = int(evidence_quality.get("strong_count", 0))
    moderate_count = int(evidence_quality.get("moderate_count", 0))
    weak_count = int(evidence_quality.get("weak_count", 0))
    source_count = len(evidence_quality.get("sources", []))

    confidence += min(strong_count * 0.13, 0.39)
    confidence += min(moderate_count * 0.07, 0.21)
    confidence += min(weak_count * 0.02, 0.04)

    if source_count >= 2:
        confidence += 0.10

    if source_count >= 3:
        confidence += 0.05

    if matched_rules:
        confidence += 0.12

    if rule_decision == "HUMAN_REVIEW":
        confidence -= 0.25

    if evidence_quality.get("quality") == "missing":
        confidence -= 0.25

    if evidence_quality.get("quality") == "weak":
        confidence -= 0.10

    return round(max(0.0, min(confidence, 0.95)), 2)