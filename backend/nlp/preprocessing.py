"""Text preprocessing functions for ScamGraph AI Phase 1.

This module intentionally stays lightweight for the baseline Phase 1 ML workflow:
- normalize whitespace
- lowercase the text
- remove unnecessary punctuation while preserving useful token clues
- expose a reusable preprocessing entry point for training and prediction
"""

import re


def remove_extra_whitespace(text: str) -> str:
    """Collapse multiple whitespace characters into a single space."""
    return re.sub(r"\s+", " ", text).strip()


def normalize_text(text: str) -> str:
    """Normalize the input message by trimming and collapsing whitespace."""
    return remove_extra_whitespace(text)


def remove_unnecessary_whitespace(text: str) -> str:
    """Backward-compatible alias used by existing file imports."""
    return remove_extra_whitespace(text)


def lowercase_text(text: str) -> str:
    """Convert input text to lowercase for consistent downstream processing."""
    return text.lower()


def remove_unnecessary_characters(text: str) -> str:
    """Remove characters that are not useful for the baseline text model.

    We keep useful URL, email, UPI, currency, and number-like tokens visible
    rather than over-aggressively stripping them.
    """
    # Keep letters, numbers, spaces, useful punctuation and common scam evidence signs.
    text = re.sub(r"[^a-zA-Z0-9\s@._:/%+₹\-]", " ", text)
    return remove_extra_whitespace(text)


def preprocess_text(text: str) -> str:
    """Return a clean, small text representation for the ML classifier."""
    text = normalize_text(text)
    text = lowercase_text(text)
    text = remove_unnecessary_characters(text)
    return remove_extra_whitespace(text)


def tokenize_text(text: str) -> list[str]:
    """Tokenize text into simple whitespace-aware token units."""
    return re.findall(r"\b[\w@./+-]+\b", text.lower())
