from backend.nlp.scam_type_classifier import classify_scam_type


def test_kyc_scam() -> None:
    indicators = {'impersonation': True, 'credential_request': True, 'urgency': True,
                  'fear': False, 'reward_manipulation': False, 'payment_pressure': False}
    result = classify_scam_type('Complete your KYC verification immediately', indicators, {}, 'scam')
    assert result == 'KYC Scam'


def test_lottery_scam() -> None:
    indicators = {'reward_manipulation': True, 'urgency': False, 'fear': False,
                  'impersonation': False, 'credential_request': False, 'payment_pressure': False}
    result = classify_scam_type('Congratulations you won a lottery prize', indicators, {}, 'scam')
    assert result == 'Lottery Scam'


def test_job_scam() -> None:
    indicators = {'urgency': False, 'fear': False, 'impersonation': False,
                  'reward_manipulation': False, 'credential_request': False, 'payment_pressure': False}
    result = classify_scam_type('Great job opportunity, interview today', indicators, {}, 'scam')
    assert result == 'Job Scam'


def test_credential_theft() -> None:
    indicators = {'credential_request': True, 'urgency': False, 'fear': False,
                  'impersonation': False, 'reward_manipulation': False, 'payment_pressure': False}
    result = classify_scam_type('Please share your OTP', indicators, {}, 'scam')
    assert result == 'Credential Theft'


def test_unknown_when_no_evidence() -> None:
    indicators = {'urgency': False, 'fear': False, 'impersonation': False,
                  'reward_manipulation': False, 'credential_request': False, 'payment_pressure': False}
    result = classify_scam_type('Hello there', indicators, {}, 'scam')
    assert result == 'Unknown'


def test_legitimate_short_circuits() -> None:
    indicators = {'urgency': True, 'fear': True, 'impersonation': True,
                  'reward_manipulation': False, 'credential_request': True, 'payment_pressure': False}
    result = classify_scam_type('anything', indicators, {}, 'legitimate')
    assert result == 'Legitimate'
