from document_pipeline.text_processor import (
    build_preview,
    build_simple_summary,
    process_text_document,
    read_text_file,
)


def test_read_text_file(tmp_path):
    sample = tmp_path / "sample.md"
    sample.write_text("# Sample Document", encoding="utf-8")

    text = read_text_file(str(sample))

    assert text == "# Sample Document"


def test_build_preview_short_text():
    text = "This is a short document."

    preview = build_preview(text)

    assert preview == "This is a short document."


def test_build_preview_long_text():
    text = "word " * 100

    preview = build_preview(text, max_length=30)

    assert preview.endswith("...")
    assert len(preview) <= 33


def test_build_simple_summary_from_heading():
    text = "# Sample Document\n\nThis is the body."

    summary = build_simple_summary(text)

    assert summary == "Sample Document"


def test_build_simple_summary_from_plain_text():
    text = "This is the first sentence.\nThis is another line."

    summary = build_simple_summary(text)

    assert summary == "This is the first sentence."


def test_build_simple_summary_empty_document():
    text = ""

    summary = build_simple_summary(text)

    assert summary == "Empty document."


def test_process_text_document(tmp_path):
    sample = tmp_path / "sample.md"
    sample.write_text("# Sample Document\n\nThis is a test document.", encoding="utf-8")

    result = process_text_document(str(sample))

    assert result.characters > 0
    assert result.words > 0
    assert result.line_count == 3
    assert result.summary == "Sample Document"
    assert "Sample Document" in result.preview
