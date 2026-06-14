import argparse

from document_pipeline.pipeline import run_pipeline


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


def main():
    parser = argparse.ArgumentParser(
        prog="doc-pipe",
        description="Document Pipeline MVP",
    )

    parser.add_argument("file", help="Path to input document")

    args = parser.parse_args()

    result = run_pipeline(args.file)

    print_result(result)


if __name__ == "__main__":
    main()
