"""Evidence engine: combines ML, NLP, and entity-extraction signals into a
single structured, explainable list of evidence items.

Every item has: type, severity, reason, source.
Evidence is only ever generated for signals that were actually detected --
this module never invents or assumes evidence.
"""

# ML probability tiers for generating an ML-sourced evidence item. Below the
# low tier, no ML evidence item is produced at all (nothing notable to report).
ML_HIGH_THRESHOLD = 0.7
ML_MODERATE_THRESHOLD = 0.4

NLP_SEVERITY = {
    "urgency": "medium",
    "fear": "high",
    "impersonation": "high",
    "reward_manipulation": "medium",
    "credential_request": "high",
    "payment_pressure": "high",
}

NLP_REASONS = {
    "urgency": "The message pressures the recipient to act immediately.",
    "fear": "The message uses threatening or fear-inducing language, such as an account being blocked or legal action.",
    "impersonation": "The message appears to impersonate a bank, government body, or official organization.",
    "reward_manipulation": "The message tries to lure the recipient with a prize, reward, or cashback claim.",
    "credential_request": "The message requests sensitive authentication information such as an OTP, password, or PIN.",
    "payment_pressure": "The message pushes the recipient toward an immediate payment or money transfer.",
}


def _ml_evidence(scam_probability: float) -> list[dict]:
    if scam_probability >= ML_HIGH_THRESHOLD:
        return [{
            "type": "High Scam Probability",
            "severity": "high",
            "reason": "The trained scam classifier assigned a high scam probability to this message.",
            "source": "ml",
        }]
    if scam_probability >= ML_MODERATE_THRESHOLD:
        return [{
            "type": "Moderate Scam Probability",
            "severity": "medium",
            "reason": "The trained scam classifier assigned a moderate scam probability to this message.",
            "source": "ml",
        }]
    return []


def _nlp_evidence(indicators: dict) -> list[dict]:
    evidence = []
    for key, is_present in indicators.items():
        if not is_present:
            continue
        evidence.append({
            "type": key.replace("_", " ").title(),
            "severity": NLP_SEVERITY.get(key, "medium"),
            "reason": NLP_REASONS.get(key, f"The message contains a {key.replace('_', ' ')} signal."),
            "source": "nlp",
        })
    return evidence


def _entity_evidence(entities: dict) -> list[dict]:
    if entities.get("urls"):
        return [{
            "type": "URL Detected",
            "severity": "info",
            "reason": "The message contains a URL.",
            "source": "entity_extraction",
        }]
    return []


def build_evidence(scam_probability: float, indicators: dict, entities: dict) -> list[dict]:
    """Combine ML, NLP, and entity-extraction signals into one evidence list."""
    evidence = []
    evidence.extend(_ml_evidence(scam_probability))
    evidence.extend(_nlp_evidence(indicators))
    evidence.extend(_entity_evidence(entities))
    return evidence
