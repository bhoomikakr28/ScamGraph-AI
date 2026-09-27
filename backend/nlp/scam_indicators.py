"""Rule-based scam indicator detection for Phase 1 MVP.

Six indicator categories, matching the product spec. URL detection is handled
separately by the entity extractor (a URL is an entity, not an NLP keyword
signal), so it is intentionally not one of these categories.
"""

import re


INDICATOR_PATTERNS = {
    "urgency": [
        r"immediately", r"urgent", r"act now", r"act immediately",
        r"within \d+ minutes?", r"respond now", r"right away", r"expire[sd]? today",
    ],
    "fear": [
        r"account will be blocked", r"account suspended", r"account will be suspended",
        r"legal action", r"police action", r"penalty", r"access will be disabled",
        r"account will be disabled", r"account will be closed", r"blocked permanently",
    ],
    "impersonation": [
        r"\bbank\b", r"\bgovernment\b", r"\bpolice\b", r"customer support",
        r"official department", r"tax department", r"income tax", r"customs department",
    ],
    "reward_manipulation": [
        r"congratulations", r"\bwon\b", r"lottery", r"\bprize\b", r"\breward\b", r"cashback",
        r"lucky draw", r"gift card",
    ],
    "credential_request": [
        r"\botp\b", r"password", r"\bpin\b", r"\bcvv\b", r"verification code",
        r"login details", r"credentials", r"card number", r"aadhaar number",
    ],
    "payment_pressure": [
        r"pay now", r"transfer money", r"send payment", r"make payment",
        r"pay ₹", r"upi payment", r"pay immediately", r"complete the payment",
    ],
}


def detect_indicators(text: str) -> dict:
    """Return dictionary of structured indicator booleans keyed by indicator group."""
    lowered = text.lower()
    return {
        key: any(re.search(pattern, lowered) for pattern in patterns)
        for key, patterns in INDICATOR_PATTERNS.items()
    }


def detect_indicator_matches(text: str) -> dict:
    """Return, per category, whether it was detected and which phrases matched.

    Used by the evidence engine so evidence reasons can reference what was
    actually found in the message rather than a generic description.
    """
    lowered = text.lower()
    result = {}
    for key, patterns in INDICATOR_PATTERNS.items():
        matches = [p for p in patterns if re.search(p, lowered)]
        result[key] = {"detected": bool(matches), "matches": matches}
    return result
