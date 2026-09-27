from backend.nlp.preprocessing import normalize_text, remove_unnecessary_whitespace, lowercase_text, tokenize_text
from backend.nlp.scam_indicators import detect_indicators
from backend.nlp.entity_extractor import extract_entities


def test_preprocessing_pipeline() -> None:
    text = '  URGENT Bank Account Will Be Blocked!   '
    assert normalize_text(text) == 'URGENT Bank Account Will Be Blocked!'
    assert remove_unnecessary_whitespace('  text   with   spaces  ') == 'text with spaces'
    assert lowercase_text('Bank Account') == 'bank account'
    assert 'bank' in tokenize_text('Bank Account Will Be Blocked')


def test_indicator_detection() -> None:
    # Matches the spec's own worked example exactly -- note impersonation is
    # NOT expected here, since "your bank account" alone doesn't claim to
    # speak *as* the bank (see test_impersonation_requires_claim_context below).
    text = 'Your bank account will be blocked today. Verify OTP immediately.'
    indicators = detect_indicators(text)
    assert indicators['urgency'] is True
    assert indicators['fear'] is True
    assert indicators['credential_request'] is True


def test_impersonation_requires_claim_context() -> None:
    # A genuine impersonation attempt: claims to speak *as* the bank.
    text = 'This is your bank calling. Our security team needs to verify your OTP.'
    indicators = detect_indicators(text)
    assert indicators['impersonation'] is True


def test_bare_authority_mention_is_not_impersonation() -> None:
    # Regression test: an ordinary sentence mentioning "bank" with no claim
    # of authority must NOT be flagged (this was a real false positive found
    # during manual testing).
    text = 'Hey, can you verify what time the bank branch closes today?'
    indicators = detect_indicators(text)
    assert indicators['impersonation'] is False


def test_reward_and_payment_indicators() -> None:
    text = 'Congratulations! You have won a lottery prize. Pay now to claim your reward.'
    indicators = detect_indicators(text)
    assert indicators['reward_manipulation'] is True
    assert indicators['payment_pressure'] is True


def test_safe_message_has_no_indicators() -> None:
    text = 'Your class starts at 10 AM tomorrow in Room 204.'
    indicators = detect_indicators(text)
    assert not any(indicators.values())


def test_entity_extraction() -> None:
    text = 'Your account will be blocked. Contact 9876543210. Pay using abc@upi. Visit secure-example.com'
    entities = extract_entities(text)
    assert '9876543210' in entities['phone_numbers']
    assert 'abc@upi' in entities['upi_ids']
    assert 'secure-example.com' in entities['urls']


def test_entity_extraction_does_not_double_count_email_as_url() -> None:
    text = 'Contact us at support@gmail.com for help.'
    entities = extract_entities(text)
    assert 'support@gmail.com' in entities['emails']
    assert 'gmail.com' not in entities['urls']
