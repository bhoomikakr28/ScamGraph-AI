from backend.evidence.evidence_engine import build_evidence


def test_ml_evidence_generated_for_high_probability() -> None:
    evidence = build_evidence(0.9, {}, {})
    types = [item['type'] for item in evidence]
    assert 'High Scam Probability' in types


def test_no_ml_evidence_for_low_probability() -> None:
    evidence = build_evidence(0.05, {}, {})
    types = [item['type'] for item in evidence]
    assert 'High Scam Probability' not in types
    assert 'Moderate Scam Probability' not in types


def test_nlp_evidence_only_for_detected_signals() -> None:
    indicators = {'urgency': True, 'fear': False, 'impersonation': False,
                  'reward_manipulation': False, 'credential_request': True, 'payment_pressure': False}
    evidence = build_evidence(0.5, indicators, {})
    types = {item['type'] for item in evidence}
    assert 'Urgency' in types
    assert 'Credential Request' in types
    assert 'Fear' not in types
    for item in evidence:
        assert set(item.keys()) == {'type', 'severity', 'reason', 'source'}


def test_url_evidence_only_when_url_detected() -> None:
    evidence = build_evidence(0.1, {}, {'urls': ['example.com']})
    types = [item['type'] for item in evidence]
    assert 'URL Detected' in types

    evidence_no_url = build_evidence(0.1, {}, {'urls': []})
    types_no_url = [item['type'] for item in evidence_no_url]
    assert 'URL Detected' not in types_no_url
