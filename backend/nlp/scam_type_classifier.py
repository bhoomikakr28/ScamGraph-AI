"""Scam type identification based on actual detected evidence.

This is deliberately a set of ordered rules over the indicators/entities that
were already detected -- it never introduces new detection logic of its own,
and it never claims certainty it doesn't have: anything that doesn't clearly
match a known pattern falls through to "Other" or "Unknown".
"""

SUPPORTED_TYPES = [
    "Phishing", "KYC Scam", "Bank Impersonation", "Job Scam", "Investment Scam",
    "Payment Scam", "Lottery Scam", "Customer Support Scam", "Credential Theft",
    "Other", "Unknown",
]


def classify_scam_type(text: str, indicators: dict, entities: dict, prediction: str) -> str:
    """Return a best-effort scam type label from actual detected evidence.

    `text` is only used for a small set of domain keywords (kyc/job/invest)
    that the six formal NLP indicators don't capture on their own.
    """
    if prediction == "legitimate":
        return "Legitimate"

    lowered = text.lower()
    urgency = indicators.get("urgency")
    fear = indicators.get("fear")
    impersonation = indicators.get("impersonation")
    reward = indicators.get("reward_manipulation")
    credential = indicators.get("credential_request")
    payment = indicators.get("payment_pressure")
    has_url = bool(entities.get("urls"))
    has_upi = bool(entities.get("upi_ids"))

    is_kyc = "kyc" in lowered
    is_job = any(word in lowered for word in ("job", "interview", "hiring", "vacancy"))
    is_investment = any(word in lowered for word in ("invest", "trading", "returns", "stock tip"))
    is_customer_support = "customer support" in lowered

    # Ordered from most specific to least specific so a message matching
    # several patterns gets the most informative label.
    if is_kyc and (impersonation or credential):
        return "KYC Scam"
    if impersonation and credential and (fear or urgency):
        return "Bank Impersonation"
    if reward and any(word in lowered for word in ("lottery", "prize")):
        return "Lottery Scam"
    if is_job:
        return "Job Scam"
    if is_investment:
        return "Investment Scam"
    if credential and has_url and not impersonation:
        return "Phishing"
    if credential:
        return "Credential Theft"
    if impersonation and is_customer_support:
        return "Customer Support Scam"
    if payment or has_upi:
        return "Payment Scam"
    if any([urgency, fear, impersonation, reward, credential, payment]):
        return "Other"
    return "Unknown"
