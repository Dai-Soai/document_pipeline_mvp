import json
from pathlib import Path

from document_pipeline.pipeline import PipelineResult


def pipeline_result_to_dict(result: PipelineResult) -> dict:
    payload = {
        "source": {
            "path": result.source_path,
            "type": result.file_type,
        },
        "status": result.status,
        "message": result.message,
    }

    if result.text_result is not None:
        payload["metadata"] = {
            "characters": result.text_result.characters,
            "words": result.text_result.words,
            "line_count": result.text_result.line_count,
        }

        payload["summary"] = {
            "text": result.text_result.summary,
            "preview": result.text_result.preview,
        }

        payload["content"] = {
            "text": result.text_result.text,
        }

        payload["processing"] = {
            "ocr_used": False,
        }

    elif result.ocr_result is not None:
        payload["metadata"] = {
            "characters": result.ocr_result.characters,
            "words": result.ocr_result.words,
            "line_count": result.ocr_result.line_count,
        }

        payload["summary"] = {
            "text": result.ocr_result.summary,
            "preview": result.ocr_result.preview,
        }

        payload["content"] = {
            "text": result.ocr_result.text,
        }

        payload["processing"] = {
            "ocr_used": result.ocr_result.ocr_used,
        }

    else:
        payload["metadata"] = {}
        payload["summary"] = {}
        payload["content"] = {}
        payload["processing"] = {
            "ocr_used": False,
        }

    return payload


def export_json_report(result: PipelineResult, output_path: str) -> str:
    path = Path(output_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = pipeline_result_to_dict(result)

    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return str(path)
