
# Document Pipeline MVP

A lightweight document processing pipeline for routing text and image documents through reusable RADAR utility services.

The pipeline supports:

* Text document processing
* Image OCR processing
* JSON report export
* Markdown report export
* Publish bridge to Knowledge Search
* Batch processing for mixed document folders

---

## Current Status

M8 Batch Pipeline complete.

### Completed

* M1 Bootstrap
* M2 File Type Detector
* M3 Text Pipeline
* M4 Image OCR Pipeline
* M5 JSON Export Layer
* M6 Markdown Export Layer
* M7 Publish Layer
* M8 Batch Pipeline

### Test Status

```text
43 passed
```

---

## Features

* CLI command: `doc-pipe`
* Detect supported file types
* Process `.md` and `.txt` text documents
* OCR image files with Tesseract
* Export structured JSON reports
* Export readable Markdown reports
* Publish extracted text into a Knowledge Search input directory
* Batch process mixed folders
* Skip unsupported files during batch processing
* Pytest coverage

---

## Supported File Types

### Text

* `.md`
* `.txt`

### Image OCR

* `.png`
* `.jpg`
* `.jpeg`
* `.webp`

### Placeholder

* `.json`

### Unsupported

Files such as `.pdf` are not processed in the current version.

---

## Requirements

### System Package

Tesseract is required for image OCR.

```bash
sudo apt install tesseract-ocr tesseract-ocr-eng
```

### Python

```text
Python >= 3.11
```

---

## Installation

```bash
git clone git@github.com:Dai-Soai/document_pipeline_mvp.git

cd document_pipeline_mvp

python3 -m venv .venv

source .venv/bin/activate

pip install -e ".[dev]"
```

---

## Optional: Knowledge Search Integration

This project can publish extracted document text into a folder that can be indexed by `radar-search`.

If `radar_knowledge_search` is available locally beside this repository:

```bash
cd ~/RADAR/RADAR_SERVICE/document_pipeline_mvp

source .venv/bin/activate

pip install -e ../radar_knowledge_search
```

Verify:

```bash
which radar-search

radar-search --help
```

Expected local layout:

```text
RADAR_SERVICE/
├── radar_knowledge_search/
└── document_pipeline_mvp/
```

---

## Usage

### Process a Text Document

```bash
doc-pipe data/sample.md
```

### Process an Image with OCR

```bash
doc-pipe data/sample_image.png
```

### Export JSON Report

```bash
doc-pipe data/sample.md --json outputs/sample_text.json
```

### Export Markdown Report

```bash
doc-pipe data/sample.md --md outputs/sample_text.md
```

### Export JSON and Markdown Together

```bash
doc-pipe data/sample.md \
  --json outputs/sample_text.json \
  --md outputs/sample_text.md
```

---

## Publish to Knowledge Search

Publish extracted text:

```bash
doc-pipe data/sample.md --publish

doc-pipe data/sample_image.png --publish
```

Published files are written to:

```text
outputs/published_documents/
```

Index published documents:

```bash
radar-search index outputs/published_documents
```

Search indexed documents:

```bash
radar-search search "RADAR"

radar-search search "Pipeline"
```

Expected bridge:

```text
Document Pipeline
    ↓
outputs/published_documents/*.txt
    ↓
radar-search index
    ↓
radar-search search
```

---

## Batch Processing

Create a mixed document folder:

```text
data/batch_docs/
├── note.md
├── plain.txt
├── scan.png
└── ignore.pdf
```

Run batch processing:

```bash
doc-pipe --batch data/batch_docs
```

Export batch JSON and Markdown reports:

```bash
doc-pipe --batch data/batch_docs \
  --json-dir outputs/batch_json \
  --md-dir outputs/batch_md
```

Publish batch output:

```bash
doc-pipe --batch data/batch_docs --publish
```

Index and search batch output:

```bash
radar-search index outputs/published_documents

radar-search search "Batch"
```

---

## Example JSON Report

```json
{
  "source": {
    "path": "data/sample.md",
    "type": "text"
  },
  "status": "ok",
  "message": "Processed text document: sample.md",
  "metadata": {
    "characters": 99,
    "words": 13,
    "line_count": 3
  },
  "summary": {
    "text": "Sample Document",
    "preview": "# Sample Document RADAR Document Pipeline MVP routes documents through reusable utility services."
  },
  "content": {
    "text": "# Sample Document\n\nRADAR Document Pipeline MVP routes documents through reusable utility services.\n"
  },
  "processing": {
    "ocr_used": false
  }
}
```

---

## Example Markdown Report

````md
# Document Pipeline Report

## Source

- Path: `data/sample.md`
- Type: `text`
- Status: `ok`
- Message: Processed text document: sample.md

## Processing

- OCR Used: `False`

## Metadata

- Characters: `99`
- Words: `13`
- Line Count: `3`

## Summary

Sample Document

## Preview

# Sample Document RADAR Document Pipeline MVP routes documents through reusable utility services.

## Extracted Content

```text
# Sample Document

RADAR Document Pipeline MVP routes documents through reusable utility services.
````

````

---

## Project Structure

```text
document_pipeline_mvp/
├── data/
├── document_pipeline/
│   ├── batch.py
│   ├── cli.py
│   ├── detector.py
│   ├── exporter.py
│   ├── ocr_processor.py
│   ├── pipeline.py
│   ├── publisher.py
│   └── text_processor.py
├── tests/
├── pyproject.toml
├── README.md
└── .gitignore
````

---

## Tests

```bash
pytest
```

Expected:

```text
43 passed
```

---

## Roadmap

* [x] M1 Bootstrap
* [x] M2 File Type Detector
* [x] M3 Text Pipeline
* [x] M4 Image OCR Pipeline
* [x] M5 JSON Export Layer
* [x] M6 Markdown Export Layer
* [x] M7 Publish Layer
* [x] M8 Batch Pipeline
* [ ] M9 Packaging & README Finalization
* [ ] M10 v0.1.0 Release

---

## Notes

* OCR quality depends on input image clarity and Tesseract recognition.
* PDF processing is not supported in this MVP.
* Knowledge Search integration is optional and requires the local `radar_knowledge_search` package.
* Batch mode skips unsupported files.
