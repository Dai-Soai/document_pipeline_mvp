from document_pipeline.cli import print_result
from document_pipeline.pipeline import PipelineResult


def test_print_result(capsys):
    result = PipelineResult(
        source_path="sample.md",
        status="ok",
        message="Pipeline placeholder for: sample.md",
    )

    print_result(result)

    captured = capsys.readouterr()

    assert "DOCUMENT PIPELINE MVP" in captured.out
    assert "sample.md" in captured.out
    assert "ok" in captured.out
