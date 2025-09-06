# Anki Deck Manager — Project Documentation

A Streamlit-based web application to generate and manage Anki decks (.apkg) from JSON flashcard data. The app supports one-off deck generation and long-term deck maintenance backed by SQLite.

---

## 1) Overview

- Purpose: Turn simple JSON card data into reviewable Anki decks, while providing a workflow to grow and maintain decks over time.
- Tech stack:
  - UI: Streamlit
  - Persistence: SQLite (via Python standard library)
  - Deck export: genanki
  - Packaging: Python package `ankideck/` used by `main.py`
- Run modes: Local (Streamlit) and Docker container.

---

## 2) Features

- Paste or upload flashcards in JSON (list of `{question, answer}`)
- Validate and preview JSON before generating
- Create a new deck and append cards using two flows:
  - Editor: Generate and route to My Decks
  - My Decks: Create/rename/delete decks; append JSON; edit/delete individual cards
- Deduplication on append (case-insensitive, trimmed, normalizing non‑breaking space)
- Export any deck to `.apkg` on demand
- History tab for quick download of recent JSONs and generated `.apkg` files
- Automatic migration of legacy JSON files in `DeckLibrary/` to SQLite on first run
- Modern, clean UI styling and light theme via `.streamlit/config.toml`

---

## 3) Repository Layout

```
anki-deck-generator/
├─ ankideck/                     # Application package
│  ├─ __init__.py                # Public API re-exports
│  ├─ config.py                  # Paths and constants
│  ├─ core.py                    # Validation, sanitization, merge/dedup logic
│  ├─ db.py                      # SQLite persistence layer and migrations
│  ├─ services.py                # JSON I/O and .apkg creation (genanki)
│  └─ ui/                        # Streamlit UI modules
│     ├─ __init__.py
│     ├─ editor.py               # Editor (paste/upload) + Generate actions
│     ├─ mydecks.py              # My Decks management, modals, CRUD
│     ├─ preview.py              # Live preview for pasted JSON and saved deck snapshot
│     ├─ history.py              # Recent JSONs and Decks (.apkg)
│     ├─ sidebar.py              # Sidebar controls, sample loader
│     ├─ helpers.py              # JSON parsing helper, sample JSON
│     └─ style.py                # Global style injection
├─ .streamlit/
│  └─ config.toml                # Theme and browser settings
├─ data/
│  └─ decks.sqlite3              # SQLite DB (created at runtime)
├─ Decks/                        # Output .apkg files (created at runtime)
├─ DeckLibrary/                  # Legacy JSON library (optional, migrated on first run)
├─ JSONs/                        # Saved/validated JSON snapshots (created at runtime)
├─ main.py                       # App entry, tabs, and page setup
├─ requirements.txt              # streamlit, genanki
├─ Dockerfile                    # Containerized execution
└─ README.md                     # Quick-start guide
```

---

## 4) Application Architecture

- Entry point `main.py`:
  - Sets page config and injects base styles (`ankideck.ui.style.inject_base_styles()`)
  - Ensures output directories
  - Initializes the SQLite DB via `ankideck.db.db_init()` (also migrates legacy JSON)
  - Renders sidebar and three tabs: `My Decks`, `Create New Deck` (Editor + Preview), `History`
- UI split into modular renderers:
  - `ankideck/ui/editor.py: render_editor_tab()`
  - `ankideck/ui/mydecks.py: render_mydecks_tab()`
  - `ankideck/ui/preview.py: render_preview_tab()`
  - `ankideck/ui/history.py: render_history_tab()`
  - `ankideck/ui/sidebar.py: render_sidebar()`
  - `ankideck/ui/style.py: inject_base_styles()`
- Business logic:
  - `ankideck/core.py`: validation, sanitization, and dedup/merge logic
  - `ankideck/services.py`: JSON persistence helpers, `.apkg` creation with genanki
  - `ankideck/db.py`: SQLite schema, CRUD for decks and cards, dedup-aware append

Data primarily lives in SQLite (`data/decks.sqlite3`). Some auxiliary files are written to `JSONs/` and `Decks/` for user convenience.

---

## 5) Data Model (SQLite Schema)

Defined in `ankideck/db.py` within `db_init()`:

- Table `decks`:
  - `id INTEGER PRIMARY KEY AUTOINCREMENT`
  - `name TEXT NOT NULL UNIQUE`
  - `created_at TEXT NOT NULL`
  - `updated_at TEXT NOT NULL`
- Table `cards`:
  - `id INTEGER PRIMARY KEY AUTOINCREMENT`
  - `deck_id INTEGER NOT NULL` (FK → `decks.id`, `ON DELETE CASCADE`)
  - `question TEXT NOT NULL`
  - `answer TEXT NOT NULL`
  - `created_at TEXT NOT NULL`
  - `updated_at TEXT NOT NULL`
- Table `app_meta`:
  - `key TEXT PRIMARY KEY`
  - `value TEXT`
- Indexes:
  - `idx_cards_deck` on `cards(deck_id)`
  - `idx_cards_q` on `cards(question)`
  - `idx_cards_a` on `cards(answer)`

One-time migration (`_migrate_json_library_to_db`) imports any `DeckLibrary/*.json` as decks if not already present.

---

## 6) Public Python API (`ankideck/__init__.py`)

- Config
  - `DECK_LIBRARY_DIR`, `DATA_DIR`, `DB_PATH`
- Core
  - `validate_cards(cards) -> bool`
  - `sanitize_filename(name: str) -> str`
  - `merge_cards(existing_cards, new_cards) -> (merged: list, stats: dict)`
- Services
  - `save_validated_json(json_str, deck_name) -> str`
  - `create_apkg(file_path, deck_name) -> str`
  - `create_apkg_from_cards(cards, deck_name) -> str`
  - `get_deck_library_path(deck_name) -> str`
  - `load_deck_json(deck_name) -> list`
  - `save_deck_json(deck_name, cards) -> str`
- DB
  - `db_init()`
  - `db_list_decks(search: str = "") -> list[dict]`
  - `db_create_deck(name: str) -> dict`
  - `db_get_deck_by_name(name: str) -> dict | None`
  - `db_get_deck_cards(deck_id: int) -> list[dict]`
  - `db_get_deck_cards_by_name(name: str) -> list[dict]`
  - `db_add_cards(deck_id: int, new_cards: list[dict]) -> dict`
  - `db_export_deck_apkg(deck_id: int, deck_name: str) -> str`
  - `db_rename_deck(deck_id: int, new_name: str)`
  - `db_delete_deck(deck_id: int)`
  - `db_update_card(card_id: int, question: str, answer: str)`
  - `db_delete_card(card_id: int)`

---

## 7) UI Walkthrough

- Sidebar (`ankideck/ui/sidebar.py`)
  - Choose input mode: Paste JSON / Upload JSON
  - View a sample JSON and load it into the editor
- Tab: My Decks (`ankideck/ui/mydecks.py`)
  - Search decks; for each deck show name, card count, and actions (Open, Manage, Export .apkg, Delete)
  - Manage dialog (modal): rename deck; append from current Editor JSON; append by pasting JSON
  - Selected deck panel: edit or delete individual cards with pagination
  - Floating + button to open the Create Deck dialog
- Tab: Create New Deck → Editor (`ankideck/ui/editor.py`)
  - Paste/upload JSON; validate and preview; generate and add to DB
  - On generate, the app ensures a deck exists (create if missing), adds cards with dedup, selects it, and switches to My Decks
- Tab: Create New Deck → Preview (`ankideck/ui/preview.py`)
  - Shows live stats for the current editor JSON
  - Shows a snapshot of saved cards for the current deck name (if any)
- Tab: History (`ankideck/ui/history.py`)
  - Quick download of recent `JSONs/` and `Decks/` files; lists decks in DB

---

## 8) Validation and Deduplication

- Validation (`ankideck/core.py: validate_cards`) ensures the JSON is a list of objects each with `question` and `answer` keys.
- Deduplication uses a normalized key `(_normalize_text(q), _normalize_text(a))` where normalization:
  - trims whitespace
  - replaces non‑breaking space with regular space
  - lowercases
- Merge behavior (`merge_cards`): returns `merged` list and stats `{before, added, duplicates, after}`
- DB append (`db_add_cards`): loads existing, merges, inserts only new entries, and updates `decks.updated_at`.

---

## 9) Deck Export (.apkg)

- Implemented in `ankideck/services.py: create_apkg_from_cards`
- Uses genanki with a simple model and a single card template
- Writes `.apkg` to `Decks/<deck_name>.apkg`

---

## 10) Configuration

- Paths/constants in `ankideck/config.py`:
  - `DECK_LIBRARY_DIR = "DeckLibrary"`
  - `DATA_DIR = "data"`
  - `DB_PATH = os.path.join(DATA_DIR, "decks.sqlite3")`
- Streamlit theme and browser options in `.streamlit/config.toml` (light theme, indigo accent, disabled usage stats)
- UI base CSS in `ankideck/ui/style.py`

---

## 11) Installation & Running

- Requirements (`requirements.txt`):
  - `streamlit`
  - `genanki`
  - SQLite is part of Python standard library

- Local
  1. `pip install -r requirements.txt`
  2. `streamlit run main.py`

- Docker
  1. `docker build -t anki-deck-generator .`
  2. `docker run -p 8501:8501 -v ./Decks:/code/Decks -v ./data:/code/data anki-deck-generator`
  3. Open http://localhost:8501

---

## 12) JSON Format

Example valid JSON:

```json
[
  {"question": "What is 2+2?", "answer": "4"},
  {"question": "Capital of France?", "answer": "Paris"}
]
```

---

## 13) Error Handling & Troubleshooting

- Malformed JSON: user-friendly messages in Editor and Preview
- Empty deck name or fields: validations in UI and DB functions
- Duplicate cards: silently skipped and reported in stats
- Where is my data? SQLite DB at `data/decks.sqlite3`; `.apkg` in `Decks/`; JSON snapshots in `JSONs/`
- Legacy JSON migration: runs once; set via `app_meta` key `json_migrated`

---

## 14) Development Guide

- Code organization: keep business logic in `ankideck/`, UI only calls exported APIs
- Add a new UI feature:
  - Create a new module under `ankideck/ui/` and add an entry in `ankideck/ui/__init__.py`
  - Import and invoke it from `main.py` (e.g., add a new tab)
- Extend deck model or card fields:
  - Update `services.create_apkg_from_cards` with new fields and templates
  - Update validation in `core.validate_cards` and DB schema in `db_init()` if needed
  - Add proper migration logic for existing data if changing schema
- Styling: update `ankideck/ui/style.py` or `.streamlit/config.toml`
- Testing: (none included). Suggested to add unit tests for `core.py` and `db.py`

---

## 15) Roadmap Ideas

- Multi-field notes and richer card templates (front/back + extra fields)
- Tags and deck hierarchies
- Bulk importers (CSV, Google Sheets)
- Conflict resolution UI when editing cards concurrently (multi-user scenario)
- Backup/restore DB, export/import deck JSON snapshots
- Internationalization (i18n) and RTL support
- Theming toggle (light/dark) from UI

---

## 16) Security & Privacy

- The app is local by default; data stays on your machine
- If deployed, consider access control and HTTPS
- Avoid uploading sensitive content when using remote hosting

---

## 17) License

MIT (see `README.md`).

---

## 18) Quick API Usage Examples

Python shell examples using the public API:

```python
from ankideck import (
    validate_cards, db_init, db_create_deck, db_add_cards, db_get_deck_cards,
    db_export_deck_apkg
)

# Initialize DB
db_init()

# Create a deck and add cards
cards = [
    {"question": "Q1?", "answer": "A1"},
    {"question": "Q2?", "answer": "A2"},
]
assert validate_cards(cards)

deck = db_create_deck("My Deck")
stats = db_add_cards(deck["id"], cards)
print(stats)  # {before, added, duplicates, after}

# Export to .apkg
path = db_export_deck_apkg(deck["id"], deck["name"])
print("Exported:", path)
```

---

## 19) Maintainers Notes

- Keep `__init__.py` re-exports updated when adding new functionality
- Ensure DB migrations are idempotent and versioned if schema evolves
- Consider pinning `requirements.txt` for reproducible builds
