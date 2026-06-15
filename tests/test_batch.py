from PIL import Image, ImageDraw

from document_pipeline.batch import (
    build_output_path,
    iter_supported_files,
    process_batch_directory,
)


def create_test_image(path, text="RADAR OCR Pipeline"):
    image = Image.new("RGB", (800, 250), "white")
    draw = ImageDraw.Draw(image)
    draw.text((40, 100), text, fill="black")
    image.save(path)


def test_iter_supported_files(tmp_path):
    (tmp_path / "sample.md").write_text("# Sample", encoding="utf-8")
    (tmp_path / "sample.txt").write_text("Plain text", encoding="utf-8")
    (tmp_path / "sample.json").write_text("{}", encoding="utf-8")
    (tmp_path / "sample.pdf").write_text("unsupported", encoding="utf-8")

    create_test_image(tmp_path / "sample.png")

    files = iter_supported_files(str(tmp_path))
    names = [path.name for path in files]

    assert "sample.md" in names
    assert "sample.txt" in names
    assert "sample.json" in names
    assert "sample.png" in names
    assert "sample.pdf" not in names


def test_build_output_path(tmp_path):
    output = build_output_path(
        "/tmp/sample document.md",
        str(tmp_path),
        "json",
    )

    assert output.endswith("sample_document.json")


def test_process_batch_directory_basic(tmp_path):
    (tmp_path / "sample.md").write_text("# Sample", encoding="utf-8")
    (tmp_path / "sample.txt").write_text("Plain text", encoding="utf-8")
    create_test_image(tmp_path / "sample.png")

    result = process_batch_directory(str(tmp_path))

    assert result.total_files == 3
    assert result.processed == 3
    assert result.failed == 0
    assert len(result.items) == 3


def test_process_batch_directory_with_json_and_markdown_exports(tmp_path):
    input_dir = tmp_path / "input"
    json_dir = tmp_path / "json"
    md_dir = tmp_path / "md"

    input_dir.mkdir()

    (input_dir / "sample.md").write_text("# Sample", encoding="utf-8")
    create_test_image(input_dir / "sample.png")

    result = process_batch_directory(
        str(input_dir),
        json_dir=str(json_dir),
        md_dir=str(md_dir),
    )

    assert result.processed == 2
    assert result.failed == 0

    assert (json_dir / "sample.json").exists()
    assert (md_dir / "sample.md").exists()


def test_process_batch_directory_with_publish(tmp_path):
    input_dir = tmp_path / "input"
    publish_dir = tmp_path / "published"

    input_dir.mkdir()

    (input_dir / "sample.md").write_text("# Sample", encoding="utf-8")
    create_test_image(input_dir / "sample.png")

    result = process_batch_directory(
        str(input_dir),
        publish=True,
        publish_dir=str(publish_dir),
    )

    assert result.processed == 2
    assert result.failed == 0

    assert (publish_dir / "sample.text.txt").exists()
    assert (publish_dir / "sample.image.txt").exists()
