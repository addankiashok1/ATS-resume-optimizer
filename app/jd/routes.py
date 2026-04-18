from fastapi import APIRouter, HTTPException, status
from app.jd.schemas import JDAnalyzeRequest, JDAnalyzeResponse
from app.jd.service import JDService

router = APIRouter()


@router.post("/analyze", response_model=JDAnalyzeResponse)
async def analyze_jd(payload: JDAnalyzeRequest) -> JDAnalyzeResponse:
    try:
        result = JDService.analyze(payload)
        return JDAnalyzeResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
