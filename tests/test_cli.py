from document_pipeline.batch import BatchItemResult, BatchResult
from document_pipeline.cli import print_result
from document_pipeline.ocr_processor import OcrDocumentResult
from document_pipeline.pipeline import PipelineResult
from document_pipeline.text_processor import TextDocumentResult


def test_print_text_result(capsys):
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

    print_result(result)

    captured = capsys.readouterr()

    assert "DOCUMENT PIPELINE MVP" in captured.out
    assert "sample.md" in captured.out
    assert "text" in captured.out
    assert "Metadata:" in captured.out
    assert "Summary:" in captured.out
    assert "Preview:" in captured.out


def test_print_ocr_result(capsys):
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

    print_result(result)

    captured = capsys.readouterr()

    assert "DOCUMENT PIPELINE MVP" in captured.out
    assert "sample.png" in captured.out
    assert "image" in captured.out
    assert "OCR:" in captured.out
    assert "Used: True" in captured.out
    assert "RADAR OCR Pipeline" in captured.out


def test_print_result_without_export_still_works(capsys):
    result = PipelineResult(
        source_path="sample.json",
        file_type="json",
        status="ok",
        message="Detected json document: sample.json",
    )

    print_result(result)

    captured = capsys.readouterr()

    assert "DOCUMENT PIPELINE MVP" in captured.out
    assert "sample.json" in captured.out
    assert "json" in captured.out


def test_print_batch_result(capsys):
    batch_result = BatchResult(
        input_dir="data/batch_docs",
        total_files=1,
        processed=1,
        skipped=0,
        failed=0,
        items=[
            BatchItemResult(
                source_path="data/batch_docs/sample.md",
                status="ok",
                message="Processed batch item: sample.md",
            )
        ],
    )

    from document_pipeline.cli import print_batch_result

    print_batch_result(batch_result)

    captured = capsys.readouterr()

    assert "DOCUMENT PIPELINE BATCH" in captured.out
    assert "Processed: 1" in captured.out
    assert "sample.md" in captured.out
