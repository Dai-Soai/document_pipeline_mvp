from dataclasses import dataclass
from pathlib import Path

from document_pipeline.detector import detect_file_type
from document_pipeline.ocr_processor import OcrDocumentResult, process_image_document
from document_pipeline.text_processor import TextDocumentResult, process_text_document


@dataclass
class PipelineResult:
    source_path: str
    file_type: str
    status: str
    message: str
    text_result: TextDocumentResult | None = None
    ocr_result: OcrDocumentResult | None = None


def run_pipeline(file_path: str) -> PipelineResult:
    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    file_type = detect_file_type(str(path))

    if file_type == "text":
        text_result = process_text_document(str(path))

        return PipelineResult(
            source_path=str(path),
            file_type=file_type,
            status="ok",
            message=f"Processed text document: {path.name}",
            text_result=text_result,
        )

    if file_type == "image":
        ocr_result = process_image_document(str(path))

        return PipelineResult(
            source_path=str(path),
            file_type=file_type,
            status="ok",
            message=f"Processed image document with OCR: {path.name}",
            ocr_result=ocr_result,
        )

    return PipelineResult(
        source_path=str(path),
        file_type=file_type,
        status="ok",
        message=f"Detected {file_type} document: {path.name}",
    )
