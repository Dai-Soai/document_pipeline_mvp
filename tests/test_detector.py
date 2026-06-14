import pytest

from document_pipeline.detector import detect_file_type, is_supported_file


def test_detect_text_files():
    assert detect_file_type("note.md") == "text"
    assert detect_file_type("note.txt") == "text"


def test_detect_image_files():
    assert detect_file_type("scan.png") == "image"
    assert detect_file_type("scan.jpg") == "image"
    assert detect_file_type("scan.jpeg") == "image"
    assert detect_file_type("scan.webp") == "image"


def test_detect_json_files():
    assert detect_file_type("report.json") == "json"


def test_detect_is_case_insensitive():
    assert detect_file_type("NOTE.MD") == "text"
    assert detect_file_type("SCAN.PNG") == "image"
    assert detect_file_type("REPORT.JSON") == "json"


def test_reject_unsupported_file():
    with pytest.raises(ValueError, match="Unsupported file type"):
        detect_file_type("archive.zip")


def test_reject_file_without_extension():
    with pytest.raises(ValueError, match="Unsupported file type"):
        detect_file_type("README")


def test_is_supported_file():
    assert is_supported_file("note.md") is True
    assert is_supported_file("scan.png") is True
    assert is_supported_file("report.json") is True
    assert is_supported_file("archive.zip") is False
