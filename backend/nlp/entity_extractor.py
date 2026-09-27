"""Simple regex-based entity extraction for Phase 1 MVP."""

import re


def extract_entities(text: str) -> dict:
    """Extract basic structured entities such as phone numbers, UPI IDs, URLs, and emails.

    NOTE: A detected URL is only "URL detected" -- it is not evidence of malicious
    intent. URL reputation/intelligence is a later phase and is intentionally not
    implemented here.
    """
    phone_pattern = r"\b(?:\+91[-\s]?|0)?[6-9]\d{9}\b"
    upi_pattern = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\b"
    url_pattern = r"(?:https?://)?(?:www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(?:/\S*)?"
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    phones = re.findall(phone_pattern, text)
    emails = re.findall(email_pattern, text)

    # Find URL-shaped matches, then drop any that are actually just the domain
    # portion of an email address we already captured (e.g. "gmail.com" inside
    # "foo@gmail.com") so a single email isn't double-counted as a URL too.
    email_domains = {email.split("@")[-1] for email in emails}
    urls = []
    for match in re.finditer(url_pattern, text):
        domain = match.group(1)
        if domain in email_domains:
            continue
        urls.append(domain)

    upis = re.findall(upi_pattern, text)
    # Filter UPI-like strings: keep only ones with an "@" that are not already
    # counted as full emails (a UPI handle like "abc@upi" has no dotted TLD).
    upis = [u for u in upis if "@" in u and u not in emails]

    return {
        "phone_numbers": [p.strip() for p in phones],
        "upi_ids": upis,
        "urls": urls,
        "emails": emails,
    }
