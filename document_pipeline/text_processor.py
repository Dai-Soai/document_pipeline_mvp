from dataclasses import dataclass
from pathlib import Path


@dataclass
class TextDocumentResult:
    text: str
    characters: int
    words: int
    line_count: int
    preview: str
    summary: str


def read_text_file(file_path: str) -> str:
    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    return path.read_text(encoding="utf-8")


def build_preview(text: str, max_length: int = 200) -> str:
    normalized = " ".join(text.split())

    if len(normalized) <= max_length:
        return normalized

    return normalized[:max_length].rstrip() + "..."


def build_simple_summary(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if not lines:
        return "Empty document."

    first_line = lines[0]

    if first_line.startswith("#"):
        first_line = first_line.lstrip("#").strip()

    return first_line


def process_text_document(file_path: str) -> TextDocumentResult:
    text = read_text_file(file_path)

    words = text.split()
    lines = text.splitlines()

    return TextDocumentResult(
        text=text,
        characters=len(text),
        words=len(words),
        line_count=len(lines),
        preview=build_preview(text),
        summary=build_simple_summary(text),
    )
