import os
import json
import sys
import datetime
import streamlit as st

# Import the main program (assuming it's in the parent directory)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import create_apkg, validate_cards, save_validated_json, sanitize_filename


st.set_page_config(page_title="Anki Deck Generator", page_icon="🃏")  # Add this line

os.makedirs("JSONs", exist_ok=True)
os.makedirs("Decks", exist_ok=True)


st.title("Anki Deck Generator")

st.write("Paste your JSON flashcards below. The JSON should be a list of objects with 'question' and 'answer' keys.")

filename = st.text_input("Enter filename (without extension)", "", key="filename")
json_text = st.text_area("Paste JSON here", height=300, key="json_text")

if st.button("Generate Anki Deck"):
    if not json_text.strip():
        st.error("Please paste your JSON data.")
    elif not filename.strip():
        st.error("Please enter a filename.")
    else:
        try:
            cards = json.loads(json_text)
            if not validate_cards(cards):
                st.error(
                    "JSON is not structured correctly. "
                    "It should be a list of objects with 'question' and 'answer' keys."
                )
            else:
                deck_name = sanitize_filename(filename)

                json_path = save_validated_json(json_text, deck_name)
                apkg_path = create_apkg(json_path, deck_name)

                if os.path.exists(apkg_path):
                    with open(apkg_path, "rb") as f:
                        st.success("Deck created successfully!")
                        st.download_button(
                            label="Download Anki Deck",
                            data=f,
                            file_name=deck_name + ".apkg",
                            mime="application/octet-stream"
                        )

                    # Button to copy file path to clipboard
                    if st.button("Copy Deck File Path to Clipboard"):
                        st.code(os.path.abspath(apkg_path), language="")

                    # Clear the fields after success
                    st.session_state["json_text"] = ""
                    st.session_state["filename"] = ""
                    st.experimental_rerun()

                else:
                    st.error("Failed to create the .apkg file.")

        except Exception as e:
            st.error(f"Error: {e}")
