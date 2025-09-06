import re
from typing import List, Dict, Tuple


def validate_cards(cards):
    if not isinstance(cards, list):
        return False
    for card in cards:
        if not isinstance(card, dict):
            return False
        if 'question' not in card or 'answer' not in card:
            return False
    return True


def sanitize_filename(name: str) -> str:
    """Replace invalid filename characters with underscore."""
    return re.sub(r'[\\/*?:"<>|]', "_", name)


def _normalize_text(text: str) -> str:
    if text is None:
        return ""
    return str(text).strip().replace("\u00A0", " ").lower()


def _card_key(card: dict) -> Tuple[str, str]:
    """Return a key for deduplication based on normalized question+answer."""
    return (_normalize_text(card.get("question")), _normalize_text(card.get("answer")))


def merge_cards(existing_cards: List[Dict], new_cards: List[Dict]):
    """Merge new_cards into existing_cards, deduplicating by question+answer (case-insensitive, trimmed).
    Returns (merged_list, stats_dict).
    stats = {"before": int, "added": int, "duplicates": int, "after": int}
    """
    if not validate_cards(existing_cards):
        existing_cards = []
    if not validate_cards(new_cards):
        raise Exception("New cards JSON is not structured correctly. Must contain 'question' and 'answer'.")

    existing_keys = {_card_key(c) for c in existing_cards}
    added = 0
    duplicates = 0
    merged = list(existing_cards)
    for c in new_cards:
        k = _card_key(c)
        if k in existing_keys:
            duplicates += 1
            continue
        merged.append({"question": c["question"], "answer": c["answer"]})
        existing_keys.add(k)
        added += 1

    stats = {
        "before": len(existing_cards),
        "added": added,
        "duplicates": duplicates,
        "after": len(merged),
    }
    return merged, stats
