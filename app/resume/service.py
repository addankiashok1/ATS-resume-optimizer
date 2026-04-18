from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
from app.resume.extractor import ResumeExtractor
from app.resume.parser import ResumeParser


class ResumeService:
    UPLOAD_DIR = Path("uploads")

    @classmethod
    async def process_upload(cls, file: UploadFile) -> dict:
        path = await cls._save_file(file)
        text = ResumeExtractor.extract_text(path)
        parsed_data = ResumeParser.parse(text)
        return {"status": "success", "parsed_data": parsed_data}

    @classmethod
    async def _save_file(cls, file: UploadFile) -> Path:
        cls.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        filename = Path(file.filename or "resume").name
        suffix = Path(filename).suffix.lower()
        allowed = {".pdf", ".docx"}
        if suffix not in allowed:
            raise ValueError("Unsupported file type. Only PDF and DOCX are accepted.")

        destination = cls.UPLOAD_DIR / f"resume_{uuid4().hex}{suffix}"

        content = await file.read()
        if not content:
            raise ValueError("Uploaded file is empty.")

        destination.write_bytes(content)
        return destination
