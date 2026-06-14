from dataclasses import dataclass
from pathlib import Path


@dataclass
class PipelineResult:
    source_path: str
    status: str
    message: str


def run_pipeline(file_path: str) -> PipelineResult:
    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    return PipelineResult(
        source_path=str(path),
        status="ok",
        message=f"Pipeline placeholder for: {path.name}",
    )
