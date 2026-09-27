from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_status_code() -> None:
    response = client.get('/health')
    assert response.status_code == 200


def test_health_project_name() -> None:
    response = client.get('/health')
    assert response.json() == {'status': 'ok', 'project': 'ScamGraph AI'}


def test_analyze_accepts_valid_text() -> None:
    response = client.post('/api/analyze', json={'text': 'Your bank account will be blocked. Complete KYC immediately.'})
    assert response.status_code == 200
    payload = response.json()
    assert 0 <= payload['risk_score'] <= 100
    assert payload['risk_level'] in {'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'}
    assert 0 < payload['scam_probability'] < 1


def test_empty_message_validation() -> None:
    response = client.post('/api/analyze', json={'text': '   '})
    assert response.status_code == 400
    assert 'Text must not be empty.' in response.json()['detail']


def test_response_contains_core_risk_fields() -> None:
    response = client.post('/api/analyze', json={'text': 'Your bank account will be blocked. Complete KYC immediately.'})
    payload = response.json()
    assert 'risk_score' in payload
    assert 'risk_level' in payload
    assert 'scam_probability' in payload


def test_analyze_response_returns_evidence_and_recommendations() -> None:
    response = client.post('/api/analyze', json={'text': 'URGENT! Your SBI account will be blocked today. Click this link and enter your OTP.'})
    assert response.status_code == 200
    payload = response.json()
    assert payload['evidence']
    assert payload['recommendations']
