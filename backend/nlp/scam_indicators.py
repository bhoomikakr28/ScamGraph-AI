"""Rule-based scam indicator detection for Phase 1 MVP.

Six indicator categories, matching the product spec. URL detection is handled
separately by the entity extractor (a URL is an entity, not an NLP keyword
signal), so it is intentionally not one of these categories.

Impersonation is handled specially (see below): a bare institution noun like
"bank" is not enough on its own -- testing showed it produced false positives
on ordinary sentences like "what time does the bank close?". It only counts
as impersonation when an authority noun co-occurs with language that claims
to speak *as* or *for* that authority.
"""

import re


INDICATOR_PATTERNS = {
    "urgency": [
        r"immediately", r"urgent", r"act now", r"act immediately",
        r"within \d+ minutes?", r"in \d+ (minutes?|hours?)", r"respond now",
        r"right away", r"expires? (today|soon|shortly)",
    ],
    "fear": [
        r"account will be blocked", r"account suspended", r"account will be suspended",
        r"legal action", r"police action", r"penalty", r"access will be disabled",
        r"account will be disabled", r"account will be closed", r"blocked permanently",
        r"deactivated", r"lose access", r"permanently disabled",
    ],
    "reward_manipulation": [
        r"congratulations", r"\bwon\b", r"lottery", r"\bprize\b", r"\breward\b", r"cashback",
        r"lucky draw", r"gift card",
    ],
    "credential_request": [
        r"\botp\b", r"password", r"\bpin\b", r"\bcvv\b", r"verification code",
        r"login details", r"credentials", r"card number", r"aadhaar number",
        r"confirm (the |your )?code", r"share (the |your )?(code|otp)",
        r"one[- ]time password", r"the code we (just )?(texted|sent)",
    ],
    "payment_pressure": [
        r"pay now", r"transfer money", r"send payment", r"make payment",
        r"pay ₹", r"upi payment", r"pay immediately", r"complete the payment",
        r"clearance fee", r"customs (fee|duty)", r"release (the )?(parcel|package)",
    ],
}

# Authority nouns alone are not evidence of impersonation -- they need to
# co-occur with a phrase that claims to speak as/for that authority.
IMPERSONATION_AUTHORITY_NOUNS = [
    r"\bbank\b", r"\bgovernment\b", r"\bpolice\b", r"customer support",
    r"official department", r"tax department", r"income tax", r"customs department",
]
IMPERSONATION_CLAIM_MARKERS = [
    r"this is", r"we are (calling|contacting)", r"calling from", r"on behalf of",
    r"\bofficial\b", r"\bteam\b", r"\bdepartment\b", r"\balert\b", r"\bsecurity\b",
    r"notice from", r"customer support team", r"security team",
]


def _impersonation_detected(lowered: str) -> tuple[bool, list[str]]:
    noun_hits = [p for p in IMPERSONATION_AUTHORITY_NOUNS if re.search(p, lowered)]
    marker_hits = [p for p in IMPERSONATION_CLAIM_MARKERS if re.search(p, lowered)]
    if noun_hits and marker_hits:
        return True, noun_hits + marker_hits
    return False, []


def detect_indicators(text: str) -> dict:
    """Return dictionary of structured indicator booleans keyed by indicator group."""
    lowered = text.lower()
    result = {
        key: any(re.search(pattern, lowered) for pattern in patterns)
        for key, patterns in INDICATOR_PATTERNS.items()
    }
    result["impersonation"], _ = _impersonation_detected(lowered)
    return result


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

    detected, matches = _impersonation_detected(lowered)
    result["impersonation"] = {"detected": detected, "matches": matches}
    return result