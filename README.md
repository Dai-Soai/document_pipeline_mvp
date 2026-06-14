# Document Pipeline MVP

A lightweight document routing pipeline for combining text processing, OCR, export, and knowledge search utilities.

## Current Status

M1 Bootstrap.

## Features

- CLI command: `doc-pipe`
- Basic pipeline placeholder
- Pytest foundation
- Ready for file type detection

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

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

Publish documents:

```bash
doc-pipe data/sample.md --publish
doc-pipe data/sample_image.png --publish
```

Index published documents:

```bash
radar-search index outputs/published_documents
```

Search:

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
