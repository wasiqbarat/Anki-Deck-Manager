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
    page_title="Anki Deck Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
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
# Add a little spacing between the header and the tabs bar
st.markdown('<div style="height: 12px"></div>', unsafe_allow_html=True)
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

# If URL has ?tab=create, click the "Create New Deck" tab via a tiny JS snippet
_tab_flag = st.query_params.get("tab", None)
_tab_flag_val = _tab_flag[0] if isinstance(_tab_flag, list) and _tab_flag else _tab_flag
if _tab_flag_val == "create":
    components.html(
        """
        <script>
        (function() {
          function clickCreateTab() {
            try {
              const doc = window.parent.document;
              const tabs = doc.querySelectorAll('button[role="tab"]');
              for (const b of tabs) {
                const txt = (b.innerText || '').trim();
                if (txt.startsWith('Create New Deck')) { b.click(); break; }
              }
              // Remove the query param to prevent repeated switching on reruns
              const url = new URL(window.parent.location);
              url.searchParams.delete('tab');
              window.parent.history.replaceState({}, '', url);
            } catch (e) {}
          }
          setTimeout(clickCreateTab, 50);
          setTimeout(clickCreateTab, 200);
        })();
        </script>
        """,
        height=0,
    )

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

# --- Enhance main tabs with animated ink bar and modern class ---
components.html(
    """
    <script>
    (function() {
      if (window.__ADG_TABS_INIT__) return; // prevent double init across reruns
      window.__ADG_TABS_INIT__ = true;
      function getDoc() {
        let doc = document;
        try {
          if (window.parent && window.parent.document) doc = window.parent.document;
        } catch (e) {
          doc = document;
        }
        return doc;
      }

      function findMainTabList() {
        const doc = getDoc();
        const lists = doc.querySelectorAll('div[data-baseweb="tab-list"]');
        for (const list of lists) {
          const btns = Array.from(list.querySelectorAll('button[role="tab"]'));
          const labels = btns.map(b => (b.innerText || '').trim());
          if (labels.some(t => t.startsWith('My Decks')) &&
              labels.some(t => t.startsWith('Create New Deck')) &&
              labels.some(t => t.startsWith('History'))) {
            return list;
          }
        }
        return null;
      }

      function ensureInk(list) {
        list.classList.add('adg-main-tabs');
        const doc = getDoc();
        if (!list.querySelector('.adg-ink')) {
          const ink = doc.createElement('div');
          ink.className = 'adg-ink';
          list.appendChild(ink);
        }
      }

      let rafScheduled = false;
      function scheduleUpdate() {
        if (rafScheduled) return;
        rafScheduled = true;
        const cb = () => { rafScheduled = false; updateInk(); };
        (window.requestAnimationFrame || function(f){ return setTimeout(f, 16); })(cb);
      }

      function updateInk() {
        try {
          const list = findMainTabList();
          if (!list) return;
          ensureInk(list);
          const ink = list.querySelector('.adg-ink');
          const active = list.querySelector('button[role="tab"][aria-selected="true"]');
          const first = list.querySelector('button[role="tab"]');
          if (!ink || !active || !first) return;
          const listRect = list.getBoundingClientRect();
          const rect = active.getBoundingClientRect();
          const left = rect.left - listRect.left + list.scrollLeft;
          const width = rect.width;
          const prevLeft = parseFloat(ink.dataset.left || 'NaN');
          const prevWidth = parseFloat(ink.dataset.width || 'NaN');
          if (!Number.isNaN(prevLeft) && !Number.isNaN(prevWidth)) {
            if (Math.abs(prevLeft - left) < 0.5 && Math.abs(prevWidth - width) < 0.5) {
              return; // no meaningful change
            }
          }
          ink.style.width = width + 'px';
          ink.style.transform = 'translateX(' + left + 'px)';
          ink.dataset.left = String(left);
          ink.dataset.width = String(width);
        } catch (e) {}
      }

      function init() {
        scheduleUpdate();
        const list = findMainTabList();
        if (!list) return;
        const mo = new MutationObserver(() => scheduleUpdate());
        mo.observe(list, { attributes: true, subtree: true, attributeFilter: ['aria-selected'] });
        window.addEventListener('resize', scheduleUpdate, { passive: true });
        list.addEventListener('scroll', scheduleUpdate, { passive: true });
        setTimeout(scheduleUpdate, 50);
        setTimeout(scheduleUpdate, 200);
        setTimeout(scheduleUpdate, 500);
      }

      if (document.readyState === 'complete') { init(); }
      else { window.addEventListener('load', init); }
    })();
    </script>
    """,
    height=0,
)
