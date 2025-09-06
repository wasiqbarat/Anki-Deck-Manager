import os
import streamlit as st


def render_history_tab():
    st.markdown("### Recent Files")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("JSONs")
        try:
            json_files = sorted(
                [f for f in os.listdir("JSONs") if f.lower().endswith(".json")],
                reverse=True,
            )[:20]
            if not json_files:
                st.caption("No saved JSONs yet.")
            for jf in json_files:
                path = os.path.join("JSONs", jf)
                with open(path, "r", encoding="utf-8") as fh:
                    st.download_button(
                        label=f"⬇️ {jf}",
                        data=fh.read(),
                        file_name=jf,
                        mime="application/json",
                        key=f"json_{jf}",
                        width="content",
                    )
        except Exception as e:
            st.warning(f"Could not list JSONs: {e}")

    with col2:
        st.subheader("Decks (.apkg)")
        try:
            deck_files = sorted(
                [f for f in os.listdir("Decks") if f.lower().endswith(".apkg")],
                reverse=True,
            )[:20]
            if not deck_files:
                st.caption("No decks generated yet.")
            for df in deck_files:
                path = os.path.join("Decks", df)
                try:
                    with open(path, "rb") as fh:
                        st.download_button(
                            label=f"⬇️ {df}",
                            data=fh,
                            file_name=df,
                            mime="application/octet-stream",
                            key=f"deck_{df}",
                            width="content",
                        )
                        st.caption(os.path.abspath(path))
                except Exception as e:
                    st.warning(f"Could not read {df}: {e}")
        except Exception as e:
            st.warning(f"Could not list Decks: {e}")

    st.markdown("---")
    st.subheader("Database Decks (persistent)")
    try:
        from ankideck import db_list_decks
        decks = db_list_decks("")
        if not decks:
            st.caption("No decks in the database yet.")
        for d in decks:
            st.markdown(f"- {d['name']} — {d['card_count']} cards")
    except Exception as e:
        st.warning(f"Could not list database decks: {e}")
