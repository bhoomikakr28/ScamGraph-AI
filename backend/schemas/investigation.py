"""Pydantic schemas for the ScamGraph AI Phase 1 API."""

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Request body for the analysis endpoint."""

    text: str = Field(..., min_length=1, description="Suspicious message text to analyze.")


class EvidenceItem(BaseModel):
    """A single piece of explainable evidence behind a risk assessment."""

    type: str
    severity: str
    reason: str
    source: str


class Entities(BaseModel):
    """Structured entities extracted from the message."""

    urls: list[str] = Field(default_factory=list)
    phone_numbers: list[str] = Field(default_factory=list)
    emails: list[str] = Field(default_factory=list)
    upi_ids: list[str] = Field(default_factory=list)


class AnalyzeResponse(BaseModel):
    """Structured result returned after message analysis."""

    investigation_id: str
    risk_score: int
    risk_level: str
    scam_probability: float
    scam_type: str
    indicators: list[str]
    entities: Entities
    evidence: list[EvidenceItem]
    recommendations: list[str]
    timestamp: str


# Backward-compatible aliases for any older imports.
AnalysisRequest = AnalyzeRequest
InvestigationResult = AnalyzeResponse
