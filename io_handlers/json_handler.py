"""
Handler per la persistenza in formato JSON.
Il JSON è il formato canonico dell'assessment.
"""
from __future__ import annotations
import json
from models.schema import AssessmentData


def save_to_json(data: AssessmentData) -> str:
    """Serializza l'assessment in JSON string."""
    data.touch()
    return data.to_json(indent=2)


def load_from_json(json_str: str) -> AssessmentData:
    """Deserializza un assessment da JSON string."""
    return AssessmentData.from_json(json_str)


def save_to_json_bytes(data: AssessmentData) -> bytes:
    """Serializza in bytes per il download Streamlit."""
    return save_to_json(data).encode("utf-8")


def load_from_json_file(file_obj) -> AssessmentData:
    """Carica da un file-like object (Streamlit UploadedFile)."""
    content = file_obj.read()
    if isinstance(content, bytes):
        content = content.decode("utf-8")
    return load_from_json(content)
