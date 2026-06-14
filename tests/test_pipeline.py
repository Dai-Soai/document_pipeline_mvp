import pytest

from document_pipeline.pipeline import run_pipeline


def test_run_pipeline_accepts_existing_file(tmp_path):
    sample = tmp_path / "sample.md"
    sample.write_text("# Sample Document", encoding="utf-8")

    result = run_pipeline(str(sample))

    assert result.status == "ok"
    assert "sample.md" in result.message


def test_run_pipeline_rejects_missing_file(tmp_path):
    missing = tmp_path / "missing.md"

    with pytest.raises(FileNotFoundError):
        run_pipeline(str(missing))
