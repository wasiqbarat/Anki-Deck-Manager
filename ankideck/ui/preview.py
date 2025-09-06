import streamlit as st

from ankideck import db_get_deck_cards_by_name, sanitize_filename
from .helpers import parse_cards_from_text


def render_preview_tab(deckname: str):
    st.markdown("### Live Preview")
    txt = st.session_state.get("json_text", "").strip()
    if not txt:
        st.info("Paste or upload JSON in the Editor tab to see a preview here.")
    else:
        cards, err = parse_cards_from_text(txt)
        if err:
            st.warning(err)
        else:
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Cards", len(cards))
            with c2:
                st.metric("Fields", "question, answer")

            st.markdown("#### Data")
            st.dataframe(cards, height=360, width="content")

    st.markdown("---")
    st.markdown("### Current Database Deck Snapshot")
    if deckname.strip():
        db_cards = db_get_deck_cards_by_name(deckname)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Saved cards", len(db_cards))
        with c2:
            st.metric("Deck name", sanitize_filename(deckname))
        if db_cards:
            st.markdown("#### First 20 from saved deck")
            st.dataframe(db_cards[:20], height=300, width="content")
        else:
            st.info("No saved deck with this name in the database yet. Create one from My Decks.")
    else:
        st.info("Enter a deck name to preview its current saved deck.")
