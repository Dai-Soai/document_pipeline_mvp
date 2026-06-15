import argparse

from document_pipeline.batch import process_batch_directory
from document_pipeline.exporter import export_json_report, export_markdown_report
from document_pipeline.pipeline import run_pipeline
from document_pipeline.publisher import publish_to_directory


def print_text_report(text_result):
    print("Metadata:")
    print(f"  Characters: {text_result.characters}")
    print(f"  Words: {text_result.words}")
    print(f"  Lines: {text_result.line_count}")
    print()
    print("Summary:")
    print(text_result.summary)
    print()
    print("Preview:")
    print(text_result.preview)
    print()


def print_ocr_report(ocr_result):
    print("OCR:")
    print(f"  Used: {ocr_result.ocr_used}")
    print()
    print("Metadata:")
    print(f"  Characters: {ocr_result.characters}")
    print(f"  Words: {ocr_result.words}")
    print(f"  Lines: {ocr_result.line_count}")
    print()
    print("Summary:")
    print(ocr_result.summary)
    print()
    print("Preview:")
    print(ocr_result.preview)
    print()


def print_result(result):
    print("=" * 60)
    print("DOCUMENT PIPELINE MVP")
    print("=" * 60)
    print(f"Source: {result.source_path}")
    print(f"Type: {result.file_type}")
    print(f"Status: {result.status}")
    print()

    if result.text_result is not None:
        print_text_report(result.text_result)

    if result.ocr_result is not None:
        print_ocr_report(result.ocr_result)

    print(result.message)


def print_batch_result(batch_result):
    print("=" * 60)
    print("DOCUMENT PIPELINE BATCH")
    print("=" * 60)
    print(f"Input: {batch_result.input_dir}")
    print(f"Total: {batch_result.total_files}")
    print(f"Processed: {batch_result.processed}")
    print(f"Failed: {batch_result.failed}")
    print()

    for item in batch_result.items:
        print(f"- [{item.status}] {item.source_path}")
        print(f"  {item.message}")

        if item.json_path:
            print(f"  JSON: {item.json_path}")

        if item.markdown_path:
            print(f"  Markdown: {item.markdown_path}")

        if item.publish_result:
            print(f"  Published: {item.publish_result.published_path}")


def main():
    parser = argparse.ArgumentParser(
        prog="doc-pipe",
        description="Document Pipeline MVP",
    )

    parser.add_argument("--batch", help="Process all supported files in a directory")
    parser.add_argument("--json-dir", help="Export batch JSON reports to directory")
    parser.add_argument("--md-dir", help="Export batch Markdown reports to directory")
    parser.add_argument("file", nargs="?", help="Path to input document")
    parser.add_argument("--json", help="Export pipeline report to JSON file")
    parser.add_argument("--md", help="Export pipeline report to Markdown file")
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Publish extracted text to Knowledge Search input directory",
    )

    parser.add_argument(
        "--publish-dir",
        default="outputs/published_documents",
        help="Directory for published text documents",
    )

    args = parser.parse_args()

    if args.batch:
        batch_result = process_batch_directory(
            args.batch,
            json_dir=args.json_dir,
            md_dir=args.md_dir,
            publish=args.publish,
            publish_dir=args.publish_dir,
        )

        print_batch_result(batch_result)
        return

    if not args.file:
        parser.error("file is required unless --batch is used")

    result = run_pipeline(args.file)

    print_result(result)

    if args.json:
        output_path = export_json_report(result, args.json)
        print()
        print(f"JSON report exported: {output_path}")

    if args.md:
        output_path = export_markdown_report(result, args.md)
        print()
        print(f"Markdown report exported: {output_path}")

    if args.publish:
        publish_result = publish_to_directory(result, args.publish_dir)
        print()
        print(f"Published document: {publish_result.published_path}")


if __name__ == "__main__":
    main()
