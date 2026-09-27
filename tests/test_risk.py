from backend.risk.risk_engine import calculate_risk_score, risk_level_from_score


def test_risk_score_boundaries() -> None:
    score = calculate_risk_score(0.99, {'urgency': True, 'fear': True, 'impersonation': True, 'credential_request': True, 'payment_pressure': False}, {'urls': ['https://example.com']})
    assert 0 <= score <= 100


def test_risk_level_from_scores() -> None:
    assert risk_level_from_score(12) == 'LOW'
    assert risk_level_from_score(31) == 'MEDIUM'
    assert risk_level_from_score(61) == 'HIGH'
    assert risk_level_from_score(81) == 'CRITICAL'
