import os
import json
import streamlit as st

from ankideck import sanitize_filename, db_get_deck_by_name, db_create_deck, db_add_cards
from .helpers import parse_cards_from_text


def render_editor_tab(input_mode: str, deckname: str):
    st.markdown("### Edit or Upload")

    json_text = st.session_state.get("json_text", "")
    uploaded_file = None

    if input_mode == "Upload JSON":
        uploaded_file = st.file_uploader("Upload a JSON file", type=["json"], key="uploader")
        if uploaded_file is not None:
            try:
                json_text = uploaded_file.read().decode("utf-8")
                st.session_state["json_text"] = json_text
                st.success("File loaded into editor.")
            except Exception as e:
                st.error(f"Could not read file: {e}")
        st.text_area("JSON content", value=json_text, height=200, key="json_text_area", disabled=(uploaded_file is not None))
    else:
        json_text = st.text_area("Paste JSON here", value=json_text, height=200, key="json_text")

    # Place Validate on the left and Generate on the far right
    col_left, col_right = st.columns([4, 1])
    with col_left:
        validate_clicked = st.button("Validate & Preview", width="content")
    with col_right:
        generate_clicked = st.button("Generate Anki Deck", type="primary", width="content")

    if validate_clicked:
        cards, err = parse_cards_from_text(st.session_state.get("json_text", ""))
        if err:
            st.error(err)
        else:
            st.success("JSON looks good!")
            st.markdown("#### Quick stats")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("<div class='metric-card'>Cards</div>", unsafe_allow_html=True)
                st.metric(label="Total", value=len(cards))
            with c2:
                st.markdown("<div class='metric-card'>Fields</div>", unsafe_allow_html=True)
                st.metric(label="Per card", value="question, answer")

            st.markdown("#### Preview (first 20)")
            st.dataframe(cards[:20], height=300, width="content")

    if generate_clicked:
        # Inputs validation
        raw_text = st.session_state.get("json_text", "")
        if not raw_text.strip():
            st.error("Please paste or upload your JSON data.")
        elif not deckname.strip():
            st.error("Please enter a deck name.")
        else:
            try:
                cards, err = parse_cards_from_text(raw_text)
                if err:
                    st.error(err)
                else:
                    deck_name = sanitize_filename(deckname)
                    # Create a new deck in DB if needed, or reuse existing by name
                    deck = db_get_deck_by_name(deck_name)
                    if not deck:
                        deck = db_create_deck(deck_name)

                    # Add cards to the deck
                    stats = db_add_cards(deck["id"], cards)

                    # Select the deck in session and switch to My Decks tab on next render
                    st.session_state["selected_deck_id"] = deck["id"]
                    st.session_state["selected_deck_name"] = deck["name"]
                    st.session_state["switch_to_mydecks"] = True

                    # Optionally show a quick success before rerun (may not be visible due to rerun)
                    st.success(f"Added {stats['added']} new, {stats['duplicates']} duplicates. Now {stats['after']} total.")

                    # Rerun to apply the tab switch
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
