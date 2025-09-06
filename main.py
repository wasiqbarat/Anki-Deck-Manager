import os
import streamlit as st
import streamlit.components.v1 as components

from ankideck import db_init
from ankideck.ui import (
    inject_base_styles,
    render_sidebar,
    render_editor_tab,
    render_mydecks_tab,
    render_preview_tab,
    render_history_tab,
)

# --- Page setup ---
st.set_page_config(
    page_title="Anki Deck Generator",
    page_icon="📑",
    layout="wide",
)

# --- Minimal CSS for a more modern look ---
inject_base_styles()

# --- Ensure directories exist ---
os.makedirs("JSONs", exist_ok=True)
os.makedirs("Decks", exist_ok=True)
os.makedirs("DeckLibrary", exist_ok=True)

# --- Initialize database (and migrate DeckLibrary JSON once) ---
db_init()

# --- Helpers moved to ankideck.ui.helpers ---

# --- Header ---
with st.container():
    st.markdown(
        """
        <div class="app-header">
            <h1 style="margin-bottom: 0.25rem; display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.8rem;">📑</span>
                <span>Anki Deck Generator</span>
            </h1>
            <div class="subtle">Paste or upload your flashcards as JSON, preview them, and export as an Anki .apkg.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Deck name input moved into the "Create New Deck" tab

# --- Sidebar ---
with st.sidebar:
    input_mode = render_sidebar()

# --- Main content ---
mydecks_tab, create_tab, history_tab = st.tabs(["My Decks", "Create New Deck", "History"])

with mydecks_tab:
    render_mydecks_tab()

with create_tab:
    deckname = st.text_input("Deck name", value=st.session_state.get("deckname", ""), key="deckname")
    editor_subtab, preview_subtab = st.tabs(["Editor", "Preview"])
    with editor_subtab:
        render_editor_tab(input_mode, deckname)
    with preview_subtab:
        render_preview_tab(deckname)

with history_tab:
    render_history_tab()

# If the editor asked to switch to My Decks, click that tab via a tiny JS snippet.
if st.session_state.get("switch_to_mydecks"):
    components.html(
        """
        <script>
        (function() {
          function clickMyDecksTab() {
            try {
              const doc = window.parent.document;
              const tabs = doc.querySelectorAll('button[role="tab"]');
              for (const b of tabs) {
                const txt = (b.innerText || '').trim();
                if (txt.startsWith('My Decks')) { b.click(); return; }
              }
            } catch (e) {}
          }
          // Try a couple times in case tabs render async
          setTimeout(clickMyDecksTab, 50);
          setTimeout(clickMyDecksTab, 200);
        })();
        </script>
        """,
        height=0,
    )
    # Clear flag so we don't keep switching on subsequent reruns
    st.session_state.pop("switch_to_mydecks", None)

# --- Footer note ---
st.markdown("\n")
st.caption("Tip: Use the sidebar to switch between paste and upload modes, and load the sample to get started quickly.")
