"""Simple regex-based entity extraction for Phase 1 MVP."""

import re


def extract_entities(text: str) -> dict:
    """Extract basic structured entities such as phone numbers, UPI IDs, URLs, and emails."""
    phone_pattern = r"\b(?:\+91[-\s]?|0)?[6-9]\d{9}\b"
    upi_pattern = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\b"
    url_pattern = r"(?:https?://)?(?:www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(?:/\S*)?"
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    phones = re.findall(phone_pattern, text)
    urls = [match.group(1) for match in re.finditer(url_pattern, text)]
    emails = re.findall(email_pattern, text)
    upis = re.findall(upi_pattern, text)

    # Filter UPI-like strings and avoid duplicate email values.
    upis = [u for u in upis if "@" in u and u not in emails]

    return {
        "phone_numbers": [p.strip() for p in phones],
        "upi_ids": upis,
        "urls": urls,
        "emails": emails,
    }
