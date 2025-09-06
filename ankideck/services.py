import os
import json
import datetime
import genanki
from typing import List, Dict

from .config import DECK_LIBRARY_DIR
from .core import validate_cards, sanitize_filename


def save_validated_json(json_str: str, deck_name: str) -> str:
    """Validate and save JSON to JSONs/<deck_name>_<timestamp>.json. Return full path."""
    try:
        cards = json.loads(json_str)
    except Exception:
        raise Exception("Bad Format JSON.")

    if not validate_cards(cards):
        raise Exception("JSON is not structured correctly. It should be a list of objects with 'question' and 'answer' keys.")

    os.makedirs("JSONs", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f"{deck_name}_{timestamp}.json"
    json_path = os.path.join("JSONs", json_filename)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=4)
    return json_path


def create_apkg(file_path: str, deck_name: str) -> str:
    """Create an .apkg deck from a JSON file containing cards."""
    with open(file_path, 'r', encoding='utf-8') as f:
        cards = json.load(f)
    return create_apkg_from_cards(cards, deck_name)


def create_apkg_from_cards(cards: List[Dict], deck_name: str) -> str:
    """Create an .apkg file directly from a list of card dicts and return its path."""
    model = genanki.Model(
        1607392319,
        'Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ])

    deck = genanki.Deck(2059400110, deck_name)
    for card in cards:
        note = genanki.Note(model=model, fields=[card['question'], card['answer']])
        deck.add_note(note)

    decks_dir = "Decks"
    os.makedirs(decks_dir, exist_ok=True)
    apkg_path = os.path.join(decks_dir, deck_name + '.apkg')
    genanki.Package(deck).write_to_file(apkg_path)
    return apkg_path


def get_deck_library_path(deck_name: str) -> str:
    """Return absolute path for the persistent deck JSON in DeckLibrary/ with sanitized name."""
    os.makedirs(DECK_LIBRARY_DIR, exist_ok=True)
    safe = sanitize_filename(deck_name)
    return os.path.join(DECK_LIBRARY_DIR, f"{safe}.json")


essential_fields_msg = "Deck cards are not structured correctly. Each item must have 'question' and 'answer'."


def load_deck_json(deck_name: str):
    """Load existing deck cards list from DeckLibrary. If not exists, return empty list."""
    path = get_deck_library_path(deck_name)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if validate_cards(data):
                return data
        except Exception:
            pass
    return []


def save_deck_json(deck_name: str, cards: list) -> str:
    """Save the provided cards list as the persistent deck JSON. Return the saved path."""
    if not validate_cards(cards):
        raise Exception(essential_fields_msg)
    path = get_deck_library_path(deck_name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=4)
    return path
