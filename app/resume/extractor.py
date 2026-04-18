from pathlib import Path
from typing import Union
import fitz
import docx


class ResumeExtractor:
    @staticmethod
    def extract_text(file_path: Union[str, Path]) -> str:
        path = Path(file_path)
        if not path.exists():
            raise ValueError("Uploaded file was not found on disk.")

        suffix = path.suffix.lower()
        if suffix == ".pdf":
            return ResumeExtractor._extract_pdf_text(path)
        if suffix == ".docx":
            return ResumeExtractor._extract_docx_text(path)

        raise ValueError("Unsupported resume format. Only PDF and DOCX are accepted.")

    @staticmethod
    def _extract_pdf_text(path: Path) -> str:
        try:
            with fitz.open(path) as document:
                text = [page.get_text("text") for page in document]
        except Exception as exc:
            raise ValueError(f"Unable to parse PDF file: {exc}") from exc

        combined = "\n".join(text).strip()
        if not combined:
            raise ValueError("Uploaded PDF contains no readable text.")
        return combined

    @staticmethod
    def _extract_docx_text(path: Path) -> str:
        try:
            document = docx.Document(path)
        except Exception as exc:
            raise ValueError(f"Unable to parse DOCX file: {exc}") from exc

        paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
        combined = "\n".join(paragraphs).strip()
        if not combined:
            raise ValueError("Uploaded DOCX contains no readable text.")
        return combined
