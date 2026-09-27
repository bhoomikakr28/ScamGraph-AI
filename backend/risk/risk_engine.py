"""Risk scoring engine for ScamGraph AI Phase 1.

These weights and thresholds are engineering defaults for the Phase 1
baseline, not universal scientific values -- kept as named constants here so
they're easy to tune in one place as the model/dataset improve.
"""

RISK_LEVELS = {
    "LOW": (0, 30),
    "MEDIUM": (31, 60),
    "HIGH": (61, 80),
    "CRITICAL": (81, 100),
}

# Points added on top of the ML-derived base score when a signal is present.
# The ML probability remains the primary/dominant signal; these are secondary
# nudges, not counted twice for the same underlying evidence.
INDICATOR_WEIGHTS = {
    "urgency": 8,
    "fear": 7,
    "impersonation": 6,
    "reward_manipulation": 4,
    "credential_request": 10,
    "payment_pressure": 5,
}
URL_PRESENT_WEIGHT = 4


def risk_score_from_probability(scam_probability: float) -> int:
    """Create the primary risk score from the ML probability.

    The initial baseline does not add advanced URL, graph, or embedding signals.
    """
    score = round(float(scam_probability) * 100)
    return max(0, min(100, score))


def calculate_risk_score(scam_probability: float, indicators: dict, entities: dict) -> int:
    """Create a deterministic risk score based on the ML probability and evidence indicators.

    The ML probability sets the base score; each detected NLP indicator and a
    detected URL each add a fixed, configurable bonus. The score is clamped to
    0-100 either way, so no single signal alone can force a CRITICAL result.
    """
    score = risk_score_from_probability(scam_probability)
    for key, weight in INDICATOR_WEIGHTS.items():
        if indicators.get(key):
            score += weight
    if entities.get("urls"):
        score += URL_PRESENT_WEIGHT
    return max(0, min(100, score))


def risk_level_from_score(score: int) -> str:
    """Convert a numeric risk score to the configured risk level label."""
    for level, (low, high) in RISK_LEVELS.items():
        if low <= score <= high:
            return level
    return "CRITICAL" if score > 100 else "LOW"
