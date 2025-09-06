import os
import json
import sqlite3
import datetime
from typing import List, Dict, Optional

from .config import DATA_DIR, DB_PATH, DECK_LIBRARY_DIR
from .core import validate_cards, merge_cards, _normalize_text
from .services import get_deck_library_path


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _connect() -> sqlite3.Connection:
    """Open a SQLite connection with row factory."""
    _ensure_data_dir()
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def db_init():
    """Initialize the database schema and migrate any JSON library decks once."""
    _ensure_data_dir()
    with _connect() as conn:
        cur = conn.cursor()
        # Core tables
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS decks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deck_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(deck_id) REFERENCES decks(id) ON DELETE CASCADE
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS app_meta (
                key TEXT PRIMARY KEY,
                value TEXT
            );
            """
        )
        cur.execute("CREATE INDEX IF NOT EXISTS idx_cards_deck ON cards(deck_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_cards_q ON cards(question);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_cards_a ON cards(answer);")

        # One-time migration from DeckLibrary JSONs
        cur.execute("SELECT value FROM app_meta WHERE key='json_migrated'")
        row = cur.fetchone()
        if not row or row[0] != "1":
            _migrate_json_library_to_db(conn)
            cur.execute("INSERT OR REPLACE INTO app_meta(key, value) VALUES('json_migrated', '1')")
        conn.commit()


def _migrate_json_library_to_db(conn: sqlite3.Connection):
    """Import any DeckLibrary/*.json into SQLite if those deck names don't exist yet."""
    os.makedirs(DECK_LIBRARY_DIR, exist_ok=True)
    try:
        files = [f for f in os.listdir(DECK_LIBRARY_DIR) if f.lower().endswith(".json")]
    except Exception:
        files = []
    cur = conn.cursor()
    now = datetime.datetime.now().isoformat()
    for fn in files:
        deck_name = os.path.splitext(fn)[0]
        # Skip if deck already in DB
        cur.execute("SELECT id FROM decks WHERE name = ?", (deck_name,))
        if cur.fetchone():
            continue
        # Load JSON
        try:
            with open(os.path.join(DECK_LIBRARY_DIR, fn), "r", encoding="utf-8") as f:
                cards = json.load(f)
            if not validate_cards(cards):
                continue
        except Exception:
            continue
        # Create deck and insert cards
        cur.execute(
            "INSERT INTO decks(name, created_at, updated_at) VALUES(?, ?, ?)",
            (deck_name, now, now),
        )
        deck_id = cur.lastrowid
        for c in cards:
            cur.execute(
                "INSERT INTO cards(deck_id, question, answer, created_at, updated_at) VALUES(?, ?, ?, ?, ?)",
                (deck_id, c.get("question", ""), c.get("answer", ""), now, now),
            )
    conn.commit()


def db_list_decks(search: str = "") -> List[Dict]:
    """Return a list of decks with card counts, optionally filtered by search substring (case-insensitive)."""
    with _connect() as conn:
        cur = conn.cursor()
        if search:
            like = f"%{search.lower()}%"
            cur.execute(
                """
                SELECT d.id, d.name,
                       COALESCE((SELECT COUNT(1) FROM cards c WHERE c.deck_id = d.id), 0) AS card_count,
                       d.created_at, d.updated_at
                FROM decks d
                WHERE lower(d.name) LIKE ?
                ORDER BY d.updated_at DESC
                """,
                (like,),
            )
        else:
            cur.execute(
                """
                SELECT d.id, d.name,
                       COALESCE((SELECT COUNT(1) FROM cards c WHERE c.deck_id = d.id), 0) AS card_count,
                       d.created_at, d.updated_at
                FROM decks d
                ORDER BY d.updated_at DESC
                """
            )
        rows = cur.fetchall()
        return [dict(r) for r in rows]


def db_get_deck_by_name(name: str) -> Optional[Dict]:
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, created_at, updated_at FROM decks WHERE name = ?", (name,))
        row = cur.fetchone()
        return dict(row) if row else None


def db_create_deck(name: str) -> Dict:
    name = name.strip()
    if not name:
        raise Exception("Deck name cannot be empty.")
    now = datetime.datetime.now().isoformat()
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO decks(name, created_at, updated_at) VALUES(?, ?, ?)",
            (name, now, now),
        )
        deck_id = cur.lastrowid
        conn.commit()
        return {"id": deck_id, "name": name, "created_at": now, "updated_at": now}


def db_get_deck_cards(deck_id: int) -> List[Dict]:
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, question, answer, created_at, updated_at FROM cards WHERE deck_id = ? ORDER BY id ASC",
            (deck_id,),
        )
        rows = cur.fetchall()
        return [{"id": r[0], "question": r[1], "answer": r[2]} for r in rows]


def db_get_deck_cards_by_name(name: str) -> List[Dict]:
    deck = db_get_deck_by_name(name)
    if not deck:
        return []
    return db_get_deck_cards(deck["id"])  # type: ignore[index]


def _card_key(card: dict) -> tuple:
    return (_normalize_text(card.get("question")), _normalize_text(card.get("answer")))


def db_add_cards(deck_id: int, new_cards: List[Dict]) -> Dict:
    """Merge new_cards into deck, deduplicating by normalized question+answer. Returns stats dict."""
    if not validate_cards(new_cards):
        raise Exception("New cards JSON is not structured correctly. Must contain 'question' and 'answer'.")
    now = datetime.datetime.now().isoformat()
    with _connect() as conn:
        cur = conn.cursor()
        # Load existing for dedup
        cur.execute("SELECT question, answer FROM cards WHERE deck_id = ?", (deck_id,))
        existing_rows = cur.fetchall()
        existing_cards = [{"question": r[0], "answer": r[1]} for r in existing_rows]
        merged, stats = merge_cards(existing_cards, new_cards)

        # Insert only the newly added ones
        existing_set = {_card_key(c) for c in existing_cards}
        for c in merged:
            k = _card_key(c)
            if k in existing_set:
                continue
            # newly added
            cur.execute(
                "INSERT INTO cards(deck_id, question, answer, created_at, updated_at) VALUES(?, ?, ?, ?, ?)",
                (deck_id, c["question"], c["answer"], now, now),
            )
        # Update deck timestamp
        cur.execute("UPDATE decks SET updated_at = ? WHERE id = ?", (now, deck_id))
        conn.commit()
        return stats


def db_export_deck_apkg(deck_id: int, deck_name: str) -> str:
    """Export a deck by id to .apkg and return the file path."""
    from .services import create_apkg_from_cards

    cards = db_get_deck_cards(deck_id)
    cards_qa = [{"question": c["question"], "answer": c["answer"]} for c in cards]
    return create_apkg_from_cards(cards_qa, deck_name)


def db_rename_deck(deck_id: int, new_name: str):
    new_name = new_name.strip()
    if not new_name:
        raise Exception("New deck name cannot be empty.")
    now = datetime.datetime.now().isoformat()
    with _connect() as conn:
        cur = conn.cursor()
        # Ensure uniqueness
        cur.execute("SELECT id FROM decks WHERE name = ? AND id <> ?", (new_name, deck_id))
        if cur.fetchone():
            raise Exception("Another deck with this name already exists.")
        cur.execute("UPDATE decks SET name = ?, updated_at = ? WHERE id = ?", (new_name, now, deck_id))
        conn.commit()


def db_delete_deck(deck_id: int):
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM cards WHERE deck_id = ?", (deck_id,))
        cur.execute("DELETE FROM decks WHERE id = ?", (deck_id,))
        conn.commit()


def db_update_card(card_id: int, question: str, answer: str):
    question = (question or "").strip()
    answer = (answer or "").strip()
    if not question or not answer:
        raise Exception("Question and Answer cannot be empty.")
    now = datetime.datetime.now().isoformat()
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE cards SET question = ?, answer = ?, updated_at = ? WHERE id = ?",
            (question, answer, now, card_id),
        )
        conn.commit()


def db_delete_card(card_id: int):
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM cards WHERE id = ?", (card_id,))
        conn.commit()


def db_move_deck_contents(source_deck_id: int, target_deck_id: int) -> Dict:
    """
    Move all cards from source deck to target deck with deduplication.
    - Cards that are duplicates in target (same normalized question+answer) will not be added.
    - All cards are removed from the source deck regardless, effectively emptying it.
    Returns a stats dict: { 'moved': total_in_source, 'added': added_to_target, 'duplicates': skipped, 'after_target': total_in_target_after }
    """
    if source_deck_id == target_deck_id:
        raise Exception("Source and target deck must be different.")

    # Load source cards
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT question, answer FROM cards WHERE deck_id = ?", (source_deck_id,))
        rows = cur.fetchall()
        source_cards = [{"question": r[0], "answer": r[1]} for r in rows]

    total = len(source_cards)

    # Append into target with deduplication using existing merge logic
    stats = db_add_cards(target_deck_id, source_cards)
    added = int(stats.get("added", 0))
    skipped = total - added

    # Remove everything from source and update timestamps
    now = datetime.datetime.now().isoformat()
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM cards WHERE deck_id = ?", (source_deck_id,))
        cur.execute("UPDATE decks SET updated_at = ? WHERE id IN (?, ?)", (now, source_deck_id, target_deck_id))
        conn.commit()

    return {"moved": total, "added": added, "duplicates": skipped, "after_target": int(stats.get("after", 0))}
