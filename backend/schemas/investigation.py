"""Pydantic schemas for the ScamGraph AI Phase 1 API."""

from typing import Any

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Request body for the analysis endpoint."""

    text: str = Field(..., min_length=1, description="Suspicious message text to analyze.")


class AnalyzeResponse(BaseModel):
    """Structured result returned after message analysis."""

    investigation_id: str
    risk_score: int
    risk_level: str
    scam_probability: float
    scam_type: str
    indicators: list[str]
    entities: dict[str, Any]
    evidence: list[dict[str, str]]
    recommendations: list[str]
    timestamp: str


# Backward-compatible aliases for any older imports.
AnalysisRequest = AnalyzeRequest
InvestigationResult = AnalyzeResponse
