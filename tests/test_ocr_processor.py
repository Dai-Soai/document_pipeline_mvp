import pytest
from PIL import Image, ImageDraw

from document_pipeline.ocr_processor import (
    extract_text_from_image,
    process_image_document,
)


def create_test_image(path, text="RADAR OCR Pipeline"):
    image = Image.new("RGB", (800, 250), "white")
    draw = ImageDraw.Draw(image)
    draw.text((40, 100), text, fill="black")
    image.save(path)


def test_extract_text_from_image(tmp_path):
    sample = tmp_path / "sample.png"
    create_test_image(sample)

    text = extract_text_from_image(str(sample))

    assert isinstance(text, str)


def test_process_image_document(tmp_path):
    sample = tmp_path / "sample.png"
    create_test_image(sample)

    result = process_image_document(str(sample))

    assert result.ocr_used is True
    assert isinstance(result.text, str)
    assert result.characters >= 0
    assert result.words >= 0
    assert result.line_count >= 0
    assert isinstance(result.preview, str)
    assert isinstance(result.summary, str)


def test_extract_text_from_missing_image(tmp_path):
    missing = tmp_path / "missing.png"

    with pytest.raises(FileNotFoundError):
        extract_text_from_image(str(missing))
