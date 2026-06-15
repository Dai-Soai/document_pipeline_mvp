from dataclasses import dataclass
from pathlib import Path

from document_pipeline.detector import is_supported_file
from document_pipeline.exporter import export_json_report, export_markdown_report
from document_pipeline.pipeline import PipelineResult, run_pipeline
from document_pipeline.publisher import PublishResult, publish_to_directory


@dataclass
class BatchItemResult:
    source_path: str
    status: str
    message: str
    pipeline_result: PipelineResult | None = None
    json_path: str | None = None
    markdown_path: str | None = None
    publish_result: PublishResult | None = None


@dataclass
class BatchResult:
    input_dir: str
    total_files: int
    processed: int
    skipped: int
    failed: int
    items: list[BatchItemResult]


def iter_supported_files(input_dir: str) -> list[Path]:
    root = Path(input_dir).expanduser().resolve()

    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {root}")

    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    files = [
        path
        for path in root.rglob("*")
        if path.is_file() and is_supported_file(str(path))
    ]

    return sorted(files)


def build_output_path(source_path: str, output_dir: str, suffix: str) -> str:
    source = Path(source_path)
    output_root = Path(output_dir).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    safe_name = source.stem.replace(" ", "_")

    return str(output_root / f"{safe_name}.{suffix}")


def process_batch_directory(
    input_dir: str,
    json_dir: str | None = None,
    md_dir: str | None = None,
    publish: bool = False,
    publish_dir: str = "outputs/published_documents",
) -> BatchResult:
    root = Path(input_dir).expanduser().resolve()
    files = iter_supported_files(str(root))

    items: list[BatchItemResult] = []
    processed = 0
    failed = 0

    for file_path in files:
        try:
            pipeline_result = run_pipeline(str(file_path))

            json_path = None
            markdown_path = None
            publish_result = None

            if json_dir:
                json_path = build_output_path(
                    str(file_path),
                    json_dir,
                    "json",
                )
                export_json_report(pipeline_result, json_path)

            if md_dir:
                markdown_path = build_output_path(
                    str(file_path),
                    md_dir,
                    "md",
                )
                export_markdown_report(pipeline_result, markdown_path)

            if publish:
                publish_result = publish_to_directory(
                    pipeline_result,
                    publish_dir=publish_dir,
                )

            items.append(
                BatchItemResult(
                    source_path=str(file_path),
                    status="ok",
                    message=f"Processed batch item: {file_path.name}",
                    pipeline_result=pipeline_result,
                    json_path=json_path,
                    markdown_path=markdown_path,
                    publish_result=publish_result,
                )
            )

            processed += 1

        except Exception as exc:
            items.append(
                BatchItemResult(
                    source_path=str(file_path),
                    status="failed",
                    message=str(exc),
                )
            )
            failed += 1

    return BatchResult(
        input_dir=str(root),
        total_files=len(files),
        processed=processed,
        skipped=0,
        failed=failed,
        items=items,
    )
