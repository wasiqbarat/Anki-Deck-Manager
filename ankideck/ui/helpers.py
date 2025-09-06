import json
from typing import Tuple, List, Dict

from ankideck import validate_cards

SAMPLE_JSON: List[Dict[str, str]] = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "2 + 2 = ?", "answer": "4"},
]


def parse_cards_from_text(txt: str) -> Tuple[List[Dict[str, str]] | None, str | None]:
    txt = (txt or "").strip()
    if not txt:
        return None, "Please provide JSON data."
    try:
        data = json.loads(txt)
    except Exception as e:
        return None, f"Invalid JSON. {e}"
    if not validate_cards(data):
        return None, "JSON must be a list of objects with 'question' and 'answer' keys."
    return data, None
