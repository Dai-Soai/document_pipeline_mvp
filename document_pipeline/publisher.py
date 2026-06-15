from dataclasses import dataclass
from pathlib import Path

from document_pipeline.pipeline import PipelineResult

DEFAULT_PUBLISH_DIR = "outputs/published_documents"


@dataclass
class PublishResult:
    published_path: str
    source_path: str
    file_type: str
    status: str
    message: str


def get_publishable_text(result: PipelineResult) -> str:
    if result.text_result is not None:
        return result.text_result.text

    if result.ocr_result is not None:
        return result.ocr_result.text

    return ""


def build_publish_filename(result: PipelineResult) -> str:
    source = Path(result.source_path)
    safe_stem = source.stem.replace(" ", "_")

    return f"{safe_stem}.{result.file_type}.txt"


def publish_to_directory(
    result: PipelineResult,
    publish_dir: str = DEFAULT_PUBLISH_DIR,
) -> PublishResult:
    text = get_publishable_text(result)

    if not text.strip():
        raise ValueError(f"No publishable text found for file type: {result.file_type}")

    output_dir = Path(publish_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = build_publish_filename(result)
    output_path = output_dir / filename

    output_path.write_text(text, encoding="utf-8")

    return PublishResult(
        published_path=str(output_path),
        source_path=result.source_path,
        file_type=result.file_type,
        status="ok",
        message=f"Published document text: {output_path.name}",
    )
