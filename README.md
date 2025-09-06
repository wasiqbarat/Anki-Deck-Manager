# Anki Deck Generator

A Streamlit web app to generate Anki decks (`.apkg` files) from pasted JSON flashcard data.
You can now maintain decks over time with a built‑in SQLite database and a dedicated `My Decks` workspace.

---

## Features

- Paste your flashcards as JSON (list of objects with `question` and `answer` keys)
- Enter a deck name and generate a fresh `.apkg` from the `Editor` tab
- New: `My Decks` tab for persistent deck management backed by SQLite
  - Create decks via floating “＋” button (bottom‑right)
  - Search, select, rename, and delete decks
  - Append new cards from the Editor JSON or paste directly in `My Decks`
  - Edit or delete individual cards in a selected deck
  - Export any deck to `.apkg`
- Automatic validation and helpful errors for malformed JSON or missing fields
  - Deduplication when appending (case-insensitive, trims spaces) so repeated cards are skipped
  - Legacy JSON library (`DeckLibrary/`) is migrated into the database on first run

---

## Project Structure

The app is now organized as a proper Python package for better modularity and maintainability:

```
anki-deck-generator/
├─ ankideck/                 # Application package
│  ├─ __init__.py            # Public API re-exports
│  ├─ config.py              # Paths and constants
│  ├─ core.py                # Validation, sanitization, merging logic
│  ├─ services.py            # JSON I/O and .apkg creation services
│  └─ db.py                  # SQLite persistence layer
├─ main.py                   # Streamlit UI (imports from ankideck)
├─ requirements.txt
├─ Dockerfile
├─ data/
├─ Decks/
└─ DeckLibrary/
```

Import from `ankideck` instead of `utils` in new code:

```python
from ankideck import (
  validate_cards, sanitize_filename,
  save_validated_json, create_apkg, create_apkg_from_cards,
  db_init, db_list_decks, db_create_deck, db_add_cards,
  db_get_deck_cards, db_export_deck_apkg, db_rename_deck,
)
```

The legacy `utils.py` remains for backward compatibility, but new development should use the package modules above.

---

## Usage (Locally)

1. **Install requirements**

   ```sh
   pip install -r requirements.txt
   ```

2. **Run the app**

   ```sh
   streamlit run main.py
   ```

3. **In the web interface:**
   - Paste your flashcards as JSON, e.g.:
     ```json
     [
       {"question": "What is 2+2?", "answer": "4"},
       {"question": "Capital of France?", "answer": "Paris"}
     ]
     ```
   - Enter a deck name (without extension)
   - For a one‑off deck: in `Editor`, click **Generate Anki Deck** to create a fresh `.apkg` from the pasted/uploaded JSON
   - For ongoing decks: go to `My Decks`
     - Click the floating “＋” to create a new deck, or select an existing one
     - Click “Append from current Editor JSON” to add cards from the Editor
     - Or paste JSON directly under “Append by pasting JSON here”
     - Edit or delete cards inline; export anytime to `.apkg`

---

## JSON Format

Your JSON should be a list of objects, each with `question` and `answer` keys:

```json
[
  {"question": "Question 1?", "answer": "Answer 1"},
  {"question": "Question 2?", "answer": "Answer 2"}
]
```

---

## File Output

- JSON files are saved in the `JSONs/` folder with a timestamp and sanitized deck name
- Anki decks (`.apkg`) are saved in the `Decks/` folder with a sanitized deck name
- Persistent decks are stored in a SQLite database at `data/decks.sqlite3`
- On first run, legacy JSON decks found under `DeckLibrary/` are imported into the database automatically

---

## Growing Existing Decks (My Decks)

Use `My Decks` when you want to keep a deck and grow it over time:

1. Create or open a deck in `My Decks`
2. Append new cards by:
   - Clicking “Append from current Editor JSON” (uses whatever JSON is open in the Editor)
   - Or pasting JSON in the `My Decks` tab
3. The app merges cards with deduplication (normalized `question`+`answer`)
4. Edit or delete cards inline if needed
5. Export the deck to `.apkg` anytime

---

## Docker Instructions

You can run this app in a Docker container for easy deployment.

1. **Build the Docker image**

   ```sh
   docker build -t anki-deck-generator .
   ```

2. **Run the Docker container**

   ```sh
   # persist generated decks and database locally
   docker run -p 8501:8501 \
     -v ./Decks:/code/Decks \
     -v ./data:/code/data \
     anki-deck-generator
   ```

3. Open [http://localhost:8501](http://localhost:8501) in your browser to use the app.

**Note:**  
- The provided `Dockerfile` uses Python 3.12-slim and expects a `requirements.txt` file and all source code in the build context.
- If your main file is not `main.py`, adjust the `CMD` in the Dockerfile.

---

## Troubleshooting

- **Invalid deck name:** The app will automatically sanitize deck names to remove invalid characters
- **Malformed JSON:** The app will show an error if your JSON is not valid or not in the correct structure
- **Deck not created:** If the `.apkg` file is not created, an error message will be shown
- **Where is my data?** The SQLite DB is stored at `data/decks.sqlite3`. Mount `./data` when using Docker to persist.

---

## License

MIT License

---

**Made with [Streamlit](https://streamlit.io/) and [genanki](https://github.com/kerrickstaley/genanki)**