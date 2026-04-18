from fastapi import APIRouter, HTTPException, status
from app.optimizer.schemas import OptimizeRequest, OptimizeResponse
from app.optimizer.service import OptimizerService

router = APIRouter()


@router.post("/optimize", response_model=OptimizeResponse)
async def optimize_resume(payload: OptimizeRequest) -> OptimizeResponse:
    try:
        result = OptimizerService.optimize(payload)
        return OptimizeResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
