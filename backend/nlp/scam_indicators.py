"""Rule-based scam indicator detection for Phase 1 MVP."""

import re


INDICATOR_PATTERNS = {
    "urgency": [r"immediately", r"urgent", r"act now", r"within 10 minutes", r"today", r"immediately verify"],
    "fear": [r"account will be blocked", r"account suspended", r"legal action", r"police action", r"penalty"],
    "impersonation": [r"bank", r"government", r"police", r"customer support", r"official department"],
    "reward_manipulation": [r"congratulations", r"won", r"lottery", r"prize", r"reward", r"cashback"],
    "credential_request": [r"otp", r"password", r"pin", r"cvv", r"verification code", r"login details"],
    "payment_pressure": [r"pay now", r"transfer money", r"send payment", r"pay ₹", r"upi payment"],
    "url_present": [r"click this link", r"link and", r"url", r"link", r"website", r"webpage", r"www\."],
}


def detect_indicators(text: str) -> dict:
    """Return dictionary of structured indicator booleans keyed by indicator group."""
    lowered = text.lower()
    return {
        "urgency": any(re.search(pattern, lowered) for pattern in INDICATOR_PATTERNS["urgency"]),
        "fear": any(re.search(pattern, lowered) for pattern in INDICATOR_PATTERNS["fear"]),
        "impersonation": any(re.search(pattern, lowered) for pattern in INDICATOR_PATTERNS["impersonation"]),
        "reward_manipulation": any(re.search(pattern, lowered) for pattern in INDICATOR_PATTERNS["reward_manipulation"]),
        "credential_request": any(re.search(pattern, lowered) for pattern in INDICATOR_PATTERNS["credential_request"]),
        "payment_pressure": any(re.search(pattern, lowered) for pattern in INDICATOR_PATTERNS["payment_pressure"]),
        "url_present": any(re.search(pattern, lowered) for pattern in INDICATOR_PATTERNS["url_present"]),
    }
