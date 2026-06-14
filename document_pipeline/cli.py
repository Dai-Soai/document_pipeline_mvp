import argparse

from document_pipeline.pipeline import run_pipeline


def print_result(result):
    print("=" * 60)
    print("DOCUMENT PIPELINE MVP")
    print("=" * 60)
    print(f"Source: {result.source_path}")
    print(f"Type: {result.file_type}")
    print(f"Status: {result.status}")
    print()

    if result.text_result is not None:
        print("Metadata:")
        print(f"  Characters: {result.text_result.characters}")
        print(f"  Words: {result.text_result.words}")
        print(f"  Lines: {result.text_result.line_count}")
        print()
        print("Summary:")
        print(result.text_result.summary)
        print()
        print("Preview:")
        print(result.text_result.preview)
        print()

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
