"""Recommendation engine: turns detected evidence into concrete safety advice.

Recommendations are only ever generated for signals actually present in the
message. For low-risk/no-signal content, we give one calm, generic tip rather
than alarming language -- we never encourage engaging with a suspected scammer.
"""

RECOMMENDATION_LOOKUP = {
    "urgency": "Do not act immediately on urgent messages; verify the request through an official channel.",
    "fear": "Pause and independently verify whether the account or contact request is legitimate.",
    "impersonation": "Do not trust a message that impersonates a bank, authority, or support team without verifying it independently.",
    "reward_manipulation": "Be skeptical of unexpected prizes or rewards; legitimate organizations don't ask you to act to claim them.",
    "credential_request": "Never share one-time passwords, PINs, OTPs, CVVs, or account-login details with anyone.",
    "payment_pressure": "Do not pay or transfer funds based on a message alone; contact the organization directly using a verified number.",
}

URL_RECOMMENDATION = "Do not click suspicious links or scan QR codes contained in the message."

DEFAULT_RECOMMENDATION = "Verify the message independently before responding, clicking links, or sharing account information."


def build_recommendations(indicators: dict, entities: dict) -> list[str]:
    """Build a de-duplicated, ordered list of safe-action recommendations."""
    recommendations = []
    for key, is_present in indicators.items():
        if is_present and key in RECOMMENDATION_LOOKUP:
            recommendations.append(RECOMMENDATION_LOOKUP[key])

    if entities.get("urls"):
        recommendations.append(URL_RECOMMENDATION)

    if not recommendations:
        recommendations.append(DEFAULT_RECOMMENDATION)

    return recommendations
