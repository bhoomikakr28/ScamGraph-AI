"""Analysis endpoint and request handling for ScamGraph AI Phase 1."""

from fastapi import APIRouter, HTTPException, status

from backend.schemas.investigation import AnalyzeRequest, AnalyzeResponse
from backend.services.temporary_analysis import temporary_analyze

router = APIRouter()


@router.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Validate the supplied message and then return the ML-backed temporary service result."""
    if not request.text or not request.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text must not be empty.",
        )

    try:
        return temporary_analyze(request)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model artifacts are missing. Train the model first using: python -m backend.ml.train",
        ) from exc


@router.get("/api/investigations")
def get_investigations() -> list:
    """Return a placeholder empty investigation history list for Step 2."""
    return []
