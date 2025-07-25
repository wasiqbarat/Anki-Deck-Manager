import os
import json
import genanki
import datetime
import re


def validate_cards(cards):
    if not isinstance(cards, list):
        return False
    for card in cards:
        if not isinstance(card, dict):
            return False
        if 'question' not in card or 'answer' not in card:
            return False
    return True


def save_validated_json(json_str: str, deck_name: str):
    """
    Validates the JSON string and saves it as a timestamped file in the JSONs folder.
    Returns the full path to the saved file.
    Raises Exception if JSON is invalid or not structured as required.
    """
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


def create_apkg(file_path: str, deck_name: str):
    # Load cards from JSON file
    with open(file_path, 'r', encoding='utf-8') as f:
        cards = json.load(f)

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

    deck = genanki.Deck(
        2059400110,
        deck_name)

    for card in cards:
        note = genanki.Note(model=model, fields=[card['question'], card['answer']])
        deck.add_note(note)

    # Create .apkg file with the same name as the JSON file
    apkg_filename = deck_name + '.apkg'

    decks_dir = "Decks"
    os.makedirs(decks_dir, exist_ok=True)
    apkg_path = os.path.join(decks_dir, apkg_filename)
    genanki.Package(deck).write_to_file(apkg_path)

    return apkg_path


def sanitize_filename(name: str) -> str:
    # Replace invalid filename characters with underscore
    return re.sub(r'[\\/*?:"<>|]', "_", name)
