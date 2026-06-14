from pathlib import Path

TEXT_EXTENSIONS = {".md", ".txt"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
JSON_EXTENSIONS = {".json"}


SUPPORTED_EXTENSIONS = TEXT_EXTENSIONS | IMAGE_EXTENSIONS | JSON_EXTENSIONS


def detect_file_type(file_path: str) -> str:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix in TEXT_EXTENSIONS:
        return "text"

    if suffix in IMAGE_EXTENSIONS:
        return "image"

    if suffix in JSON_EXTENSIONS:
        return "json"

    raise ValueError(f"Unsupported file type: {suffix or 'no extension'}")


def is_supported_file(file_path: str) -> bool:
    path = Path(file_path)
    return path.suffix.lower() in SUPPORTED_EXTENSIONS
