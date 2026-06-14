from dataclasses import dataclass
from pathlib import Path

import pytesseract
from PIL import Image

from document_pipeline.text_processor import build_preview, build_simple_summary


@dataclass
class OcrDocumentResult:
    text: str
    characters: int
    words: int
    line_count: int
    preview: str
    summary: str
    ocr_used: bool = True


def extract_text_from_image(file_path: str) -> str:
    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with Image.open(path) as image:
        return pytesseract.image_to_string(image, lang="eng")


def process_image_document(file_path: str) -> OcrDocumentResult:
    text = extract_text_from_image(file_path)

    words = text.split()
    lines = text.splitlines()

    return OcrDocumentResult(
        text=text,
        characters=len(text),
        words=len(words),
        line_count=len(lines),
        preview=build_preview(text),
        summary=build_simple_summary(text),
        ocr_used=True,
    )
