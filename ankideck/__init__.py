__version__ = "0.1.0"
"""Anki Deck Manager package.

Public API re-exports for convenience.
"""
from .config import DECK_LIBRARY_DIR, DATA_DIR, DB_PATH
from .core import (
    validate_cards,
    sanitize_filename,
    merge_cards,
)
from .services import (
    save_validated_json,
    create_apkg,
    create_apkg_from_cards,
    get_deck_library_path,
    load_deck_json,
    save_deck_json,
)
from .db import (
    db_init,
    db_list_decks,
    db_create_deck,
    db_get_deck_by_name,
    db_get_deck_cards,
    db_get_deck_cards_by_name,
    db_add_cards,
    db_export_deck_apkg,
    db_rename_deck,
    db_delete_deck,
    db_update_card,
    db_delete_card,
)
