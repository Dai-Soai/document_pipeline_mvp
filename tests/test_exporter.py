import json

from document_pipeline.exporter import (
    export_json_report,
    export_markdown_report,
    pipeline_result_to_dict,
    pipeline_result_to_markdown,
)
from document_pipeline.ocr_processor import OcrDocumentResult
from document_pipeline.pipeline import PipelineResult
from document_pipeline.text_processor import TextDocumentResult


def test_pipeline_result_to_dict_for_text():
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

    payload = pipeline_result_to_dict(result)

    assert payload["source"]["type"] == "text"
    assert payload["metadata"]["characters"] == 17
    assert payload["summary"]["text"] == "Sample Document"
    assert payload["processing"]["ocr_used"] is False
    assert payload["content"]["text"] == "# Sample Document"


def test_pipeline_result_to_dict_for_ocr():
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

    payload = pipeline_result_to_dict(result)

    assert payload["source"]["type"] == "image"
    assert payload["metadata"]["characters"] == 18
    assert payload["summary"]["text"] == "RADAR OCR Pipeline"
    assert payload["processing"]["ocr_used"] is True
    assert payload["content"]["text"] == "RADAR OCR Pipeline"


def test_export_json_report(tmp_path):
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

    output = tmp_path / "report.json"

    exported_path = export_json_report(result, str(output))

    assert exported_path == str(output.resolve())
    assert output.exists()

    payload = json.loads(output.read_text(encoding="utf-8"))

    assert payload["source"]["type"] == "text"
    assert payload["summary"]["text"] == "Sample Document"


def test_pipeline_result_to_markdown_for_text():
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

    markdown = pipeline_result_to_markdown(result)

    assert "# Document Pipeline Report" in markdown
    assert "## Source" in markdown
    assert "`text`" in markdown
    assert "Sample Document" in markdown
    assert "## Extracted Content" in markdown


def test_export_markdown_report(tmp_path):
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

    output = tmp_path / "report.md"

    exported_path = export_markdown_report(result, str(output))

    assert exported_path == str(output.resolve())
    assert output.exists()

    markdown = output.read_text(encoding="utf-8")

    assert "# Document Pipeline Report" in markdown
    assert "Sample Document" in markdown
    assert "```text" in markdown
