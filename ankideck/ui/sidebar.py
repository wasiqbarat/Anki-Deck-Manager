import json
import streamlit as st

from .helpers import SAMPLE_JSON


def render_sidebar() -> str:
    st.header("Deck settings")

    st.divider()
    st.subheader("Input mode")
    input_mode = st.radio(
        "Choose how to provide cards",
        ["Paste JSON", "Upload JSON"],
        index=0,
        label_visibility="collapsed",
        key="input_mode",
    )

    st.caption("JSON structure: a list of objects with 'question' and 'answer' keys.")
    with st.expander("JSON format guide", expanded=False):
        st.write("Example:")
        st.code(json.dumps(SAMPLE_JSON, ensure_ascii=False, indent=2), language="json")
        if st.button("Load sample into editor"):
            st.session_state["json_text"] = json.dumps(SAMPLE_JSON, ensure_ascii=False, indent=2)
            st.success("Loaded sample into editor.")

    return input_mode
