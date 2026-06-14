import pytest

from document_pipeline.pipeline import run_pipeline


def test_run_pipeline_accepts_existing_text_file(tmp_path):
    sample = tmp_path / "sample.md"
    sample.write_text("# Sample Document", encoding="utf-8")

    result = run_pipeline(str(sample))

    assert result.status == "ok"
    assert result.file_type == "text"
    assert "Detected text document" in result.message


def test_run_pipeline_accepts_existing_image_file(tmp_path):
    sample = tmp_path / "sample.png"
    sample.write_bytes(b"fake image data")

    result = run_pipeline(str(sample))

    assert result.status == "ok"
    assert result.file_type == "image"
    assert "Detected image document" in result.message


def test_run_pipeline_accepts_existing_json_file(tmp_path):
    sample = tmp_path / "sample.json"
    sample.write_text("{}", encoding="utf-8")

    result = run_pipeline(str(sample))

    assert result.status == "ok"
    assert result.file_type == "json"
    assert "Detected json document" in result.message


def test_run_pipeline_rejects_missing_file(tmp_path):
    missing = tmp_path / "missing.md"

    with pytest.raises(FileNotFoundError):
        run_pipeline(str(missing))


def test_run_pipeline_rejects_unsupported_file(tmp_path):
    sample = tmp_path / "sample.pdf"
    sample.write_text("PDF placeholder", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported file type"):
        run_pipeline(str(sample))
