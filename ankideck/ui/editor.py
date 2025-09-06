import os
import json
import streamlit as st
import streamlit.components.v1 as components

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
        # Marker element to target the next button via CSS and style it like the sidebar
        st.markdown('<div class="adg-generate-marker"></div>', unsafe_allow_html=True)
        generate_clicked = st.button("Generate Anki Deck", type="primary", width="content")
        # Add a class to the Generate button via JS to ensure stable styling
        components.html(
            """
            <script>
            (function() {
              function getDoc() {
                try { if (window.parent && window.parent.document) return window.parent.document; } catch (e) {}
                return document;
              }
              function applyStyles(btn) {
                if (!btn || btn.__adgStyled) return;
                btn.__adgStyled = true;
                const baseBg = 'linear-gradient(180deg, #0B1220 0%, #0A0F1A 100%)';
                const hoverBg = 'linear-gradient(180deg, #0C1524 0%, #0A0F1A 100%)';
                btn.style.background = baseBg;
                btn.style.color = '#E5E7EB';
                btn.style.border = '1px solid #111827';
                btn.style.borderRadius = '8px';
                btn.style.boxShadow = '0 6px 16px rgba(2, 6, 23, 0.25)';
                btn.style.outline = 'none';
                btn.addEventListener('mouseenter', () => { btn.style.background = hoverBg; }, { passive: true });
                btn.addEventListener('mouseleave', () => { btn.style.background = baseBg; }, { passive: true });
                btn.addEventListener('focus', () => { btn.style.boxShadow = '0 0 0 3px rgba(148, 163, 184, 0.25)'; });
                btn.addEventListener('blur', () => { btn.style.boxShadow = '0 6px 16px rgba(2, 6, 23, 0.25)'; });
              }

              function tagGenerateBtn() {
                try {
                  const doc = getDoc();
                  // Prefer matching by button text to be resilient to layout
                  const btns = Array.from(doc.querySelectorAll('button'));
                  for (const b of btns) {
                    const txt = (b.innerText || '').trim();
                    if (txt && txt.toLowerCase().includes('generate anki deck')) {
                      b.classList.add('adg-generate-btn');
                      applyStyles(b);
                    }
                  }
                } catch (e) {}
              }
              tagGenerateBtn();
              setTimeout(tagGenerateBtn, 50);
              setTimeout(tagGenerateBtn, 200);
              setTimeout(tagGenerateBtn, 500);
              // Observe DOM changes to re-apply class after rerenders
              try {
                const doc = getDoc();
                const mo = new MutationObserver(() => tagGenerateBtn());
                mo.observe(doc.body, { childList: true, subtree: true });
              } catch (e) {}
            })();
            </script>
            """,
            height=0,
        )

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

                    # Switch to My Decks tab on next render, but do not auto-open deck contents
                    # Clear any previously selected deck so My Decks shows only the list
                    st.session_state.pop("selected_deck_id", None)
                    st.session_state.pop("selected_deck_name", None)
                    st.session_state["switch_to_mydecks"] = True

                    # Optionally show a quick success before rerun (may not be visible due to rerun)
                    st.success(f"Added {stats['added']} new, {stats['duplicates']} duplicates. Now {stats['after']} total.")

                    # Rerun to apply the tab switch
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
