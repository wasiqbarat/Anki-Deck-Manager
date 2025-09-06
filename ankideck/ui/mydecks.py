import os
import json
import streamlit as st
import streamlit.components.v1 as components


from ankideck import (
    db_list_decks, db_create_deck, db_export_deck_apkg, db_delete_deck,
    db_get_deck_cards, db_add_cards, db_update_card, db_get_deck_by_name, db_rename_deck,
)


def render_mydecks_tab():
    st.markdown("### My Decks")
    st.markdown(
        """
        <style>
        :root {
          --primary: #4F46E5;
          --bg: #F8FAFC;
          --card: #FFFFFF;
          --text: #0F172A;
          --muted: #64748B;
          --success: #10B981;
          --danger: #EF4444;
        }
        .deck-title { font-weight: 700; font-size: 1.05rem; color: var(--text); }
        .deck-meta { color: var(--muted); font-size: 0.9rem; margin-top: 2px; display: flex; gap: 0.5rem; align-items: center; }
        /* Style the next Streamlit horizontal block as a card */
        .deck-start + div[data-testid="stHorizontalBlock"] {
          background: var(--card);
          border: 1px solid rgba(2,6,23,0.06);
          border-radius: 14px;
          padding: 16px;
          margin: 8px 0 12px;
          box-shadow: 0 1px 2px rgba(2,6,23,0.04), 0 8px 24px rgba(2,6,23,0.06);
        }
        /* Base buttons inside each card */
        .deck-start + div[data-testid="stHorizontalBlock"] .stButton > button,
        .deck-start + div[data-testid="stHorizontalBlock"] [data-testid='stDownloadButton'] > button {
          border-radius: 999px;
          padding: 0.5rem 0.9rem;
          transition: all .2s ease;
          box-shadow: 0 1px 1px rgba(0,0,0,0.02);
          width: 100%;
          border: 1px solid rgba(2,6,23,0.08);
          background: #fff;
          color: var(--text);
        }
        .deck-start + div[data-testid="stHorizontalBlock"] .stButton > button:hover,
        .deck-start + div[data-testid="stHorizontalBlock"] [data-testid='stDownloadButton'] > button:hover {
          transform: translateY(-1px);
          box-shadow: 0 8px 20px rgba(2,6,23,0.08);
        }
        /* Action colors by position (Manage, Export, Delete) */
        /* Manage - neutral (already base) */
        /* Export - success outline */
        .deck-start + div[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button,
        .deck-start + div[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid='stDownloadButton'] > button {
          border-color: rgba(16,185,129,0.35) !important;
          color: var(--success) !important;
        }
        .deck-start + div[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button:hover,
        .deck-start + div[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid='stDownloadButton'] > button:hover {
          background: rgba(16,185,129,0.08) !important;
        }
        /* Delete - danger */
        .deck-start + div[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stHorizontalBlock"] > div:nth-child(3) .stButton > button {
          border-color: rgba(239,68,68,0.35) !important;
          color: var(--danger) !important;
        }
        .deck-start + div[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stHorizontalBlock"] > div:nth-child(3) .stButton > button:hover {
          background: rgba(239,68,68,0.08) !important;
        }
        .fab { position: fixed; right: 24px; bottom: 24px; z-index: 1000; }
        .fab .fab-btn {
          display: inline-flex; width: 56px; height: 56px; border-radius: 50%;
          align-items: center; justify-content: center; background: var(--primary);
          color: #fff; text-decoration: none; font-size: 28px;
          box-shadow: 0 10px 30px rgba(79,70,229,0.35);
          transition: transform .15s ease, box-shadow .15s ease;
        }
        .fab .fab-btn:hover { transform: translateY(-2px) scale(1.03); box-shadow: 0 16px 36px rgba(79,70,229,0.45); }
        /* Compact Manage dialog spacing */
        .manage-dialog h5, .manage-dialog h6, .manage-dialog p { margin: 0.25rem 0; }
        .manage-dialog [data-testid="stVerticalBlock"] { gap: 0.35rem !important; }
        .manage-dialog .stDataFrame { margin: 0.25rem 0; }
        .manage-dialog .st-expander { margin: 0.25rem 0; }
        .manage-dialog .stButton > button { padding: 0.35rem 0.7rem; }
        /* Also narrow spacing when inside a Streamlit dialog */
        div[role="dialog"] h5, div[role="dialog"] h6, div[role="dialog"] p { margin: 0.25rem 0; }
        div[role="dialog"] [data-testid="stVerticalBlock"] { gap: 0.35rem !important; }
        div[role="dialog"] .stDataFrame { margin: 0.25rem 0; }
        div[role="dialog"] .st-expander { margin: 0.25rem 0; }
        div[role="dialog"] .stButton > button { padding: 0.35rem 0.7rem; }
        /* Make Streamlit dialog wider */
        div[role="dialog"] {
          width: min(1100px, 95vw) !important;
          max-width: none !important;
        }
        div[role="dialog"] > div {
          width: 100% !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    # URL param flow for opening the create deck dialog from the floating button
    qp_obj = st.query_params

    # Note: Open button removed; no primary button helper needed.

    colL = st.container()
    with colL:
        search = st.text_input("Search decks", value="", placeholder="Type to filter by name…")
        decks = db_list_decks(search)
        if not decks:
            st.info("No decks yet. Use the + button to create one.")
        else:
            for d in decks:
                # Marker to style the following horizontal block as a card
                st.markdown(f"<div class='deck-start' id='deck-{d['id']}'></div>", unsafe_allow_html=True)
                info_col, actions_col = st.columns([6, 4])
                with info_col:
                    st.markdown(f"<div class='deck-title'>{d['name']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='deck-meta'>🗂️ <span>{d['card_count']} cards</span></div>", unsafe_allow_html=True)
                with actions_col:
                    b1, b2, b3 = st.columns([1, 1, 1])
                    with b1:
                        if st.button("Manage ⚙️", key=f"manage_{d['id']}", help="Rename or append cards"):
                            st.session_state['manage_deck_id'] = d['id']
                    with b2:
                        if st.button("Export ⬇️", key=f"export_{d['id']}", help="Export as Anki .apkg"):
                            path = db_export_deck_apkg(d['id'], d['name'])
                            if os.path.exists(path):
                                with open(path, 'rb') as f:
                                    st.download_button(
                                        label=f"Download {os.path.basename(path)}",
                                        data=f,
                                        file_name=os.path.basename(path),
                                        mime="application/octet-stream",
                                        key=f"dl_{d['id']}",
                                    )
                                    st.caption(os.path.abspath(path))
                            else:
                                st.error("Failed to export deck.")
                    with b3:
                        if st.button("Delete 🗑️", key=f"del_{d['id']}", help="Delete this deck"):
                            st.session_state['confirm_delete_deck_id'] = d['id']
            did = st.session_state.get("confirm_delete_deck_id")
            if did:
                st.warning("Are you sure you want to delete this deck? This cannot be undone.")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Yes, delete", key="confirm_delete_yes"):
                        db_delete_deck(did)
                        st.session_state.pop("confirm_delete_deck_id", None)
                        if st.session_state.get("selected_deck_id") == did:
                            st.session_state.pop("selected_deck_id", None)
                            st.session_state.pop("selected_deck_name", None)
                        st.rerun()
                with c2:
                    if st.button("Cancel", key="confirm_delete_no"):
                        st.session_state.pop("confirm_delete_deck_id", None)

    # Right column removed: content now uses full container width.

    # Modal dialog for managing a deck (rename and append operations)
    manage_id = st.session_state.get("manage_deck_id")
    if manage_id:
        # Find the deck object from current list for display
        target = next((x for x in decks if x["id"] == manage_id), None)
        if target:
            _dlg_factory = getattr(st, "dialog", None) or getattr(st, "experimental_dialog", None)
            if _dlg_factory:
                @_dlg_factory(f"Manage Deck: {target['name']}")
                def _manage_deck_dialog():
                    st.markdown(f"##### {target['name']} — {target.get('card_count', 0)} cards")
                    st.markdown("<div class='manage-dialog'>", unsafe_allow_html=True)

                    # Rename section moved to bottom
                    # Append cards (collapsed to reduce space)
                    with st.expander("Append cards", expanded=True):
                        pasted = st.text_area("Cards JSON", value="", height=100, key=f"manage_paste_append_{target['id']}")
                        if st.button("Append pasted JSON", key=f"manage_append_paste_btn_{target['id']}"):
                            try:
                                new_cards = json.loads(pasted or "[]")
                                stats = db_add_cards(target["id"], new_cards)
                                st.success(f"Added {stats['added']} new, {stats['duplicates']} duplicates, now {stats['after']} total.")
                                st.rerun()
                            except Exception as e:
                                st.error(str(e))

                    # Deck contents (compact, paginated)
                    cards = db_get_deck_cards(target["id"])
                    total = len(cards)
                    page_size = 10
                    max_page = max(1, (total + page_size - 1) // page_size)
                    page = st.number_input(
                        "Page",
                        min_value=1,
                        max_value=max_page,
                        value=1,
                        step=1,
                        key=f"manage_cards_page_{target['id']}"
                    )
                    start = (page - 1) * page_size
                    end = min(start + page_size, total)
                    view_rows = [{"Question": c["question"], "Answer": c["answer"]} for c in cards[start:end]]
                    st.dataframe(view_rows, use_container_width=True, hide_index=True, height=260)

                    # Rename deck (moved to bottom)
                    st.markdown("###### Rename deck")
                    new_name = st.text_input("New name", value=target["name"], key=f"manage_rename_{target['id']}")
                    if st.button("Save name", key=f"manage_rename_btn_{target['id']}"):
                        try:
                            db_rename_deck(target["id"], new_name)
                            # Update selected deck name if it's the same deck
                            if st.session_state.get("selected_deck_id") == target["id"]:
                                st.session_state["selected_deck_name"] = new_name
                            st.success("Deck renamed.")
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
                    st.markdown("</div>", unsafe_allow_html=True)

                _manage_deck_dialog()
                # Clear the flag so the dialog doesn't reopen on every rerun
                st.session_state.pop("manage_deck_id", None)
            else:
                st.warning("Your Streamlit version does not support modal dialogs. Please update Streamlit to use the Manage dialog.")

    sel_id = st.session_state.get("selected_deck_id")
    sel_name = st.session_state.get("selected_deck_name", "")
    if sel_id:
        cards = db_get_deck_cards(sel_id)
        total = len(cards)
        st.markdown(f"#### Deck: {sel_name} — {total} cards")
        page_size = 20
        max_page = max(1, (total + page_size - 1) // page_size)
        page = st.number_input("Page", min_value=1, max_value=max_page, value=1, step=1, key="cards_page")
        start = (page - 1) * page_size
        end = min(start + page_size, total)
        if total == 0:
            st.info("This deck is empty. Append some cards.")
        else:
            for c in cards[start:end]:
                with st.container():
                    q_col, a_col, act_col = st.columns([3, 3, 1])
                    new_q = q_col.text_input("Question", value=c["question"], key=f"q_{c['id']}")
                    new_a = a_col.text_input("Answer", value=c["answer"], key=f"a_{c['id']}")
                    if act_col.button("Save", key=f"save_{c['id']}"):
                        try:
                            db_update_card(c["id"], new_q, new_a)
                            st.success("Saved")
                        except Exception as e:
                            st.error(str(e))
                    if act_col.button("Delete", key=f"del_card_{c['id']}"):
                        from ankideck import db_delete_card
                        db_delete_card(c["id"])
                        st.warning("Deleted")
                        st.rerun()

    components.html(
        """
        <script>
        (function() {
          try {
            const doc = window.parent.document;
            // Avoid duplicating the FAB across reruns
            if (doc.getElementById('fab-create-global')) return;
            const wrap = doc.createElement('div');
            wrap.id = 'fab-create-global';
            wrap.className = 'fab';
            const a = doc.createElement('button');
            a.type = 'button';
            a.className = 'fab-btn';
            a.title = 'Create new deck';
            a.innerText = '＋';
            a.addEventListener('click', function(e) {
              e.preventDefault();
              try {
                const tabs = doc.querySelectorAll('button[role="tab"]');
                for (const b of tabs) {
                  const txt = (b.innerText || '').trim();
                  if (txt.startsWith('Create New Deck')) { b.click(); break; }
                }
              } catch (err) {}
            });
            wrap.appendChild(a);
            doc.body.appendChild(wrap);
          } catch (e) {}
        })();
        </script>
        """,
        height=0,
    )

    # Old inline create flow removed in favor of switching to the "Create New Deck" tab.
