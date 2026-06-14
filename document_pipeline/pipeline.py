from dataclasses import dataclass
from pathlib import Path

from document_pipeline.detector import detect_file_type


@dataclass
class PipelineResult:
    source_path: str
    file_type: str
    status: str
    message: str


def run_pipeline(file_path: str) -> PipelineResult:
    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    file_type = detect_file_type(str(path))

    return PipelineResult(
        source_path=str(path),
        file_type=file_type,
        status="ok",
        message=f"Detected {file_type} document: {path.name}",
    )
