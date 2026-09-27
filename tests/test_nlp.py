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
    text = 'Your bank account will be blocked today. Verify OTP immediately.'
    indicators = detect_indicators(text)
    assert indicators['urgency'] is True
    assert indicators['fear'] is True
    assert indicators['impersonation'] is True
    assert indicators['credential_request'] is True


def test_entity_extraction() -> None:
    text = 'Your account will be blocked. Contact 9876543210. Pay using abc@upi. Visit secure-example.com'
    entities = extract_entities(text)
    assert '9876543210' in entities['phone_numbers']
    assert 'abc@upi' in entities['upi_ids']
    assert 'secure-example.com' in entities['urls']
