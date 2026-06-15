import pytest

from document_pipeline.ocr_processor import OcrDocumentResult
from document_pipeline.pipeline import PipelineResult
from document_pipeline.publisher import (
    build_publish_filename,
    get_publishable_text,
    publish_to_directory,
)
from document_pipeline.text_processor import TextDocumentResult


def test_get_publishable_text_from_text_result():
    text_result = TextDocumentResult(
        text="# Sample Document",
        characters=17,
        words=3,
        line_count=1,
        preview="Sample Document",
        summary="Sample Document",
    )

    result = PipelineResult(
        source_path="sample.md",
        file_type="text",
        status="ok",
        message="Processed text document: sample.md",
        text_result=text_result,
    )

    assert get_publishable_text(result) == "# Sample Document"


def test_get_publishable_text_from_ocr_result():
    ocr_result = OcrDocumentResult(
        text="RADAR OCR Pipeline",
        characters=18,
        words=3,
        line_count=1,
        preview="RADAR OCR Pipeline",
        summary="RADAR OCR Pipeline",
        ocr_used=True,
    )

    result = PipelineResult(
        source_path="sample.png",
        file_type="image",
        status="ok",
        message="Processed image document with OCR: sample.png",
        ocr_result=ocr_result,
    )

    assert get_publishable_text(result) == "RADAR OCR Pipeline"


def test_get_publishable_text_empty_for_json_placeholder():
    result = PipelineResult(
        source_path="sample.json",
        file_type="json",
        status="ok",
        message="Detected json document: sample.json",
    )

    assert get_publishable_text(result) == ""


def test_build_publish_filename():
    result = PipelineResult(
        source_path="/tmp/sample document.md",
        file_type="text",
        status="ok",
        message="Processed text document: sample document.md",
    )

    assert build_publish_filename(result) == "sample_document.text.txt"


def test_publish_to_directory_text_result(tmp_path):
    text_result = TextDocumentResult(
        text="# Sample Document",
        characters=17,
        words=3,
        line_count=1,
        preview="Sample Document",
        summary="Sample Document",
    )

    result = PipelineResult(
        source_path="/tmp/sample.md",
        file_type="text",
        status="ok",
        message="Processed text document: sample.md",
        text_result=text_result,
    )

    publish_result = publish_to_directory(
        result,
        publish_dir=str(tmp_path),
    )

    assert publish_result.status == "ok"
    assert publish_result.file_type == "text"
    assert publish_result.published_path.endswith("sample.text.txt")

    published_file = tmp_path / "sample.text.txt"

    assert published_file.exists()
    assert published_file.read_text(encoding="utf-8") == "# Sample Document"


def test_publish_to_directory_ocr_result(tmp_path):
    ocr_result = OcrDocumentResult(
        text="RADAR OCR Pipeline",
        characters=18,
        words=3,
        line_count=1,
        preview="RADAR OCR Pipeline",
        summary="RADAR OCR Pipeline",
        ocr_used=True,
    )

    result = PipelineResult(
        source_path="/tmp/sample.png",
        file_type="image",
        status="ok",
        message="Processed image document with OCR: sample.png",
        ocr_result=ocr_result,
    )

    publish_result = publish_to_directory(
        result,
        publish_dir=str(tmp_path),
    )

    assert publish_result.status == "ok"
    assert publish_result.file_type == "image"
    assert publish_result.published_path.endswith("sample.image.txt")

    published_file = tmp_path / "sample.image.txt"

    assert published_file.exists()
    assert published_file.read_text(encoding="utf-8") == "RADAR OCR Pipeline"


def test_publish_to_directory_rejects_empty_content(tmp_path):
    result = PipelineResult(
        source_path="/tmp/sample.json",
        file_type="json",
        status="ok",
        message="Detected json document: sample.json",
    )

    with pytest.raises(ValueError, match="No publishable text found"):
        publish_to_directory(result, publish_dir=str(tmp_path))
