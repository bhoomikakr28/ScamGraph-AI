"""Temporary analysis service wrapper for the real Step 3 ML-backed workflow.

The ML service is isolated here so the FastAPI route and response schema stay
stable while replacing the Step 2 mock result with a trained artifact-based predictor.
"""

from datetime import datetime, timezone

from backend.ml.predictor import predict_scam
from backend.nlp.entity_extractor import extract_entities
from backend.nlp.preprocessing import normalize_text, lowercase_text, remove_extra_whitespace
from backend.nlp.scam_indicators import detect_indicators
from backend.risk.risk_engine import calculate_risk_score, risk_level_from_score
from backend.schemas.investigation import AnalyzeRequest, AnalyzeResponse


INDICATOR_REASON_LOOKUP = {
    "urgency": "The message creates urgency or demands immediate action.",
    "fear": "The message uses fear, pressure, account-blocking, or threat language.",
    "impersonation": "The message appears to impersonate a bank, authority, or official contact.",
    "reward_manipulation": "The message attempts to manipulate the reader with a prize or reward claim.",
    "credential_request": "The message requests credentials, OTPs, PINs, or account verification details.",
    "payment_pressure": "The message pushes for an immediate payment, transfer, or payment channel action.",
}

RECOMMENDATION_LOOKUP = {
    "urgency": "Do not act immediately on urgent messages; verify the request through an official channel.",
    "fear": "Pause and independently verify whether the account or contact request is legitimate.",
    "impersonation": "Do not trust a message that impersonates a bank, authority, or support team.",
    "credential_request": "Never share one-time passwords, PINs, OTPs, or account-login details.",
    "payment_pressure": "Do not pay or transfer funds based on a message alone; contact the organization directly.",
    "url_present": "Do not click suspicious links or scan QR codes contained in the message.",
}


def _infer_scam_type(text: str) -> str:
    """Return a simple rule-based scam-type label when a text signals one."""
    lowered = text.lower()
    if "kyc" in lowered and ("bank" in lowered or "sbi" in lowered):
        return "KYC / Phishing"
    if "sbi" in lowered or "sbi" in lowered:
        return "Bank Impersonation"
    if "kyc" in lowered and "otp" in lowered:
        return "KYC / Phishing"
    if "lottery" in lowered or "prize" in lowered or "reward" in lowered:
        return "Lottery Scam"
    if "payment" in lowered or "upi" in lowered:
        return "Payment Scam"
    if "job" in lowered or "interview" in lowered:
        return "Job Scam"
    if "bank" in lowered or "customer support" in lowered:
        return "Bank Impersonation"
    return "Unknown"


def _build_evidence_and_recommendations(indicators: dict, entities: dict) -> tuple[list[dict[str, str]], list[str]]:
    """Create the explanation evidence and recommendations from detected NLP signals."""
    evidence = []
    for key, is_present in indicators.items():
        if not is_present:
            continue
        reason = INDICATOR_REASON_LOOKUP.get(key, f"The message contains a {key.replace('_', ' ')} signal.")
        evidence.append({
            "indicator": key.replace("_", " ").title(),
            "severity": "high" if key in {"urgency", "fear", "impersonation", "credential_request"} else "medium",
            "reason": reason,
        })

    if entities.get("urls"):
        evidence.append({
            "indicator": "URL Present",
            "severity": "high",
            "reason": "The message includes a URL or web link that may lead to a phishing destination.",
        })

    recommendations = []
    for key, is_present in indicators.items():
        if is_present:
            recommendation = RECOMMENDATION_LOOKUP.get(key)
            if recommendation:
                recommendations.append(recommendation)

    if entities.get("urls"):
        recommendations.append(RECOMMENDATION_LOOKUP["url_present"])

    # Ensure the response includes a useful default recommendation even for safe or general cases.
    if not recommendations:
        recommendations.append("Verify the message independently before responding, clicking links, or sharing account information.")

    return evidence, recommendations


def temporary_analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Use the real saved ML predictor instead of the Step 2 mock prediction."""
    cleaned_text = normalize_text(request.text)
    normalized_text = remove_extra_whitespace(cleaned_text)
    lowered_text = lowercase_text(normalized_text)

    prediction = predict_scam(lowered_text)
    scam_probability = float(prediction["scam_probability"])

    indicators = detect_indicators(lowered_text)
    entities = extract_entities(lowered_text)
    risk_score = calculate_risk_score(scam_probability, indicators, entities)

    positive_indicators = [
        key for key, value in indicators.items()
        if value is True
    ]

    evidence, recommendations = _build_evidence_and_recommendations(indicators, entities)

    scam_type = _infer_scam_type(normalized_text)
    if prediction["prediction"] == "legitimate":
        scam_type = "Legitimate"

    return AnalyzeResponse(
        investigation_id="temporary-id",
        risk_score=risk_score,
        risk_level=risk_level_from_score(risk_score),
        scam_probability=scam_probability,
        scam_type=scam_type,
        indicators=positive_indicators,
        entities=entities,
        evidence=evidence,
        recommendations=recommendations,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
