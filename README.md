# Anki Deck Manager
 
 A Streamlit web app to generate Anki decks (`.apkg` files) from pasted JSON flashcard data.
 You can now maintain decks over time with a built‑in SQLite database and a dedicated `My Decks` workspace.
 
 [![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
 [![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
 [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#license)
 
 ---
 
 ## Features
 
  - Add more cards over time in `My Decks` (persistent, SQLite-backed)
    - Create decks via the floating “＋” button; search, select, rename, and delete
    - Append new cards from the current Editor JSON or paste JSON directly in `My Decks`
    - Edit or delete individual cards inline with pagination
    - Smart deduplication when appending (case-insensitive, trims spaces) so repeated cards are skipped
  - Export to `.apkg` anytime
    - One‑click export for any deck from `My Decks` (also available in `History`)
  - Fast new deck flow
    - Paste or upload JSON in `Editor`, enter a deck name, click **Generate Anki Deck**
    - The app creates/updates the deck, adds cards with dedup, and auto-switches to `My Decks`
  - Live validation, preview, and helpful error messages for malformed JSON or missing fields
  - Offline by default: data is stored locally in SQLite (`data/decks.sqlite3`)
  - First run migrates any legacy JSONs from `DeckLibrary/` into the database
 
 ---
 
 ## Quick Start
 
 1. Install dependencies
    
    ```bash
    pip install -r requirements.txt
    ```
 
 2. Run the app
    
    ```bash
    streamlit run main.py
    ```
 
 3. Create a deck and export
    
    - Go to `Create New Deck → Editor`, paste/upload your JSON, enter a deck name, then click **Generate Anki Deck**.
    - Switch to `My Decks` to add more cards later and click **Export .apkg** anytime.
 
 ## Export to .apkg (in 10 seconds)
 
 1. Open `My Decks` and select your deck.
 2. Click **Export .apkg**.
 3. Find the file at `Decks/<deck_name>.apkg` and import it in Anki.
 
 ## Add more cards to an existing deck
 
 - Flow A — From Editor JSON
   1. Go to `Create New Deck → Editor`, paste/upload JSON and validate.
   2. Enter the same deck name you want to grow.
   3. Click **Generate Anki Deck** → the app deduplicates and switches to `My Decks`.
 
 - Flow B — From My Decks
   1. Open `My Decks` and select your deck.
   2. Use “Append from current Editor JSON” or paste JSON directly in the append box.
   3. Review inline; edit or delete cards as needed.
 
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


## License

MIT License

---
 
 **Made with [Streamlit](https://streamlit.io/) and [genanki](https://github.com/kerrickstaley/genanki)**