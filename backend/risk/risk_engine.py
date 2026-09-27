"""Risk scoring engine for ScamGraph AI Phase 1."""

RISK_LEVELS = {
    "LOW": (0, 30),
    "MEDIUM": (31, 60),
    "HIGH": (61, 80),
    "CRITICAL": (81, 100),
}


def risk_score_from_probability(scam_probability: float) -> int:
    """Create the primary risk score from the ML probability.

    The initial baseline does not add advanced URL, graph, or embedding signals.
    """
    score = round(float(scam_probability) * 100)
    return max(0, min(100, score))


def calculate_risk_score(scam_probability: float, indicators: dict, entities: dict) -> int:
    """Create a deterministic risk score based on the ML probability and evidence indicators."""
    score = risk_score_from_probability(scam_probability)
    if indicators.get("urgency"):
        score += 8
    if indicators.get("fear"):
        score += 7
    if indicators.get("impersonation"):
        score += 6
    if indicators.get("credential_request"):
        score += 10
    if indicators.get("payment_pressure"):
        score += 5
    if entities.get("urls"):
        score += 4
    if score > 100:
        score = 100
    if score < 0:
        score = 0
    return score


def risk_level_from_score(score: int) -> str:
    """Convert a numeric risk score to the configured risk level label."""
    if score <= 30:
        return "LOW"
    if score <= 60:
        return "MEDIUM"
    if score <= 80:
        return "HIGH"
    return "CRITICAL"
