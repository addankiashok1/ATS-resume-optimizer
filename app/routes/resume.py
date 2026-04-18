from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.resume.service import ResumeService
from app.resume.schemas import ResumeParseResponse

router = APIRouter()


@router.post("/upload", response_model=ResumeParseResponse)
async def upload_resume(file: UploadFile = File(...)) -> ResumeParseResponse:
    try:
        return await ResumeService.process_upload(file)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
