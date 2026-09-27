"""The permanent Step 4 analysis orchestrator.

    API Route -> Analysis Service
                   |- ML Predictor
                   |- NLP Indicator Detector
                   |- Entity Extractor
                   |- Evidence Engine
                   |- Risk Engine
                   |- Scam Type Classifier
                   `- Recommendation Engine

This replaces the Step 2/3 "temporary_analysis" wrapper now that Step 4's
evidence-based pipeline is in place. The route and response schema are
unchanged, so nothing upstream of this module needed to change.
"""

import uuid
from datetime import datetime, timezone

from backend.evidence.evidence_engine import build_evidence
from backend.ml.predictor import predict_scam
from backend.nlp.entity_extractor import extract_entities
from backend.nlp.preprocessing import normalize_text, lowercase_text, remove_extra_whitespace
from backend.nlp.scam_indicators import detect_indicators
from backend.nlp.scam_type_classifier import classify_scam_type
from backend.risk.risk_engine import calculate_risk_score, risk_level_from_score
from backend.schemas.investigation import AnalyzeRequest, AnalyzeResponse
from backend.services.recommendation_engine import build_recommendations


def analyze_message(request: AnalyzeRequest) -> AnalyzeResponse:
    """Run the full evidence-based investigation pipeline on one message."""
    cleaned_text = normalize_text(request.text)
    normalized_text = remove_extra_whitespace(cleaned_text)
    lowered_text = lowercase_text(normalized_text)

    prediction = predict_scam(lowered_text)
    scam_probability = float(prediction["scam_probability"])

    indicators = detect_indicators(lowered_text)
    entities = extract_entities(lowered_text)

    risk_score = calculate_risk_score(scam_probability, indicators, entities)
    risk_level = risk_level_from_score(risk_score)

    evidence = build_evidence(scam_probability, indicators, entities)
    recommendations = build_recommendations(indicators, entities)
    scam_type = classify_scam_type(normalized_text, indicators, entities, prediction["prediction"])

    positive_indicators = [
        key.replace("_", " ").title() for key, value in indicators.items() if value
    ]

    return AnalyzeResponse(
        investigation_id=str(uuid.uuid4()),
        risk_score=risk_score,
        risk_level=risk_level,
        scam_probability=scam_probability,
        scam_type=scam_type,
        indicators=positive_indicators,
        entities=entities,
        evidence=evidence,
        recommendations=recommendations,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# Backward-compatible alias for the old Step 2/3 name.
temporary_analyze = analyze_message
