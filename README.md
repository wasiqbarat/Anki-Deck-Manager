# Anki Deck Generator

A Streamlit web app to generate Anki decks (`.apkg` files) from pasted JSON flashcard data.

---

## Features

- Paste your flashcards as JSON (list of objects with `question` and `answer` keys)
- Enter a deck name
- Download the generated `.apkg` file for use in Anki
- Copy the generated deck file path
- Automatic validation and error messages for malformed JSON or missing fields
- Files are saved with sanitized names and timestamps

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
   - Click **Generate Anki Deck**
   - Download the `.apkg` file or copy its path

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

- JSON files are saved in the `JSONs` folder with a timestamp and sanitized deck name.
- Anki decks (`.apkg`) are saved in the `Decks` folder with a sanitized deck name.

---

## Docker Instructions

You can run this app in a Docker container for easy deployment.

1. **Build the Docker image**

   ```sh
   docker build -t anki-deck-generator .
   ```

2. **Run the Docker container**

   ```sh
   docker run -p 8501:8501 -v ./Decks:/code/Decks anki-deck-generator
   ```

3. Open [http://localhost:8501](http://localhost:8501) in your browser to use the app.

**Note:**  
- The provided `Dockerfile` uses Python 3.12-slim and expects a `requirements.txt` file and all source code in the build context.
- If your main file is not `main.py`, adjust the `CMD` in the Dockerfile.

---

## Troubleshooting

- **Invalid deck name:** The app will automatically sanitize deck names to remove invalid characters.
- **Malformed JSON:** The app will show an error if your JSON is not valid or not in the correct structure.
- **Deck not created:** If the `.apkg` file is not created, an error message will be shown.

---

## License

MIT License

---

**Made with [Streamlit](https://streamlit.io/) and [genanki](https://github.com/kerrickstaley/genanki)**