import os
import json
import sys
import streamlit as st

# Import the main program (assuming it's in the parent directory)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import create_apkg, validate_cards, save_validated_json, sanitize_filename

# --- Page setup ---
st.set_page_config(
    page_title="Anki Deck Generator",
    page_icon="📑",
    layout="wide",
)

# --- Minimal CSS for a more modern look ---
st.markdown(
    """
    <style>
        /* Compact global scaling */
        html, body {
            font-size: 13px;
        }

        /* Reduce base paddings */
        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }

        /* Sidebar width and padding */
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }
        [data-testid="stSidebar"] {
            width: 280px;
        }

        /* Header and typography */
        h1 { font-size: 1.25rem; margin: 0.25rem 0; }
        h2 { font-size: 1.05rem; margin: 0.25rem 0; }
        h3 { font-size: 1rem; margin: 0.25rem 0; }
        .subtle { color: #6b7280; font-size: 0.9rem; }

        /* Cards/containers */
        .app-header {
            padding: 0.5rem 0.75rem; 
            border-radius: 10px; 
            background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
            border: 1px solid #e5e7eb;
        }
        .section-card {
            padding: 0.6rem; 
            border-radius: 10px; 
            border: 1px solid #e5e7eb;
            background: #ffffff;
        }
        .metric-card {
            padding: 0.35rem 0.5rem; 
            border-radius: 8px; 
            border: 1px solid #e5e7eb;
            background: #fafafa;
        }

        /* Buttons and inputs */
        .stButton > button,
        .stDownloadButton > button {
            border-radius: 8px; 
            border: 1px solid #e5e7eb; 
            padding: 0.35rem 0.6rem;
            font-size: 0.9rem;
        }
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stSelectbox"] > div > div {
            font-size: 0.9rem;
        }

        /* Tabs */
        [data-baseweb="tab"] {
            padding: 0.25rem 0.5rem;
            font-size: 0.9rem;
        }

        /* Dataframe/table */
        [data-testid="stDataFrame"] div[role="grid"] * {
            font-size: 12px;
            line-height: 1.2;
        }

        /* Metrics */
        [data-testid="stMetricLabel"] { font-size: 0.8rem; }
        [data-testid="stMetricValue"] { font-size: 1.05rem; }

        /* Paragraph spacing */
        p, ul, ol { margin: 0.25rem 0; }

        /* Radio label size */
        [data-testid="stRadio"] label { font-size: 0.9rem; }

        /* Streamlit chrome */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Ensure directories exist ---
os.makedirs("JSONs", exist_ok=True)
os.makedirs("Decks", exist_ok=True)

# --- Helpers ---
def parse_cards_from_text(txt: str):
    txt = (txt or "").strip()
    if not txt:
        return None, "Please provide JSON data."
    try:
        data = json.loads(txt)
    except Exception as e:
        return None, f"Invalid JSON. {e}"
    if not validate_cards(data):
        return None, "JSON must be a list of objects with 'question' and 'answer' keys."
    return data, None

SAMPLE_JSON = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "2 + 2 = ?", "answer": "4"},
]

# --- Header ---
with st.container():
    st.markdown(
        """
        <div class="app-header">
            <h1 style="margin-bottom: 0.25rem;">📑 Anki Deck Generator</h1>
            <div class="subtle">Paste or upload your flashcards as JSON, preview them, and export as an Anki .apkg.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- Deck (moved from sidebar to main) ---
    deckname = st.text_input("Deck name", value=st.session_state.get("deckname", ""), key="deckname")

# --- Sidebar ---
with st.sidebar:
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

# --- Main content ---
editor_tab, preview_tab, history_tab = st.tabs(["Editor", "Preview", "History"])

with editor_tab:
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
        # Show text area as read-only preview when a file is uploaded
        st.text_area("JSON content", value=json_text, height=200, key="json_text_area", disabled=(uploaded_file is not None))
    else:
        json_text = st.text_area("Paste JSON here", value=json_text, height=200, key="json_text")

    col_a, col_b = st.columns([1, 1])
    with col_a:
        validate_clicked = st.button("Validate & Preview", use_container_width=True)
    with col_b:
        generate_clicked = st.button("Generate Anki Deck", type="primary", use_container_width=True)

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
            st.dataframe(cards[:20], use_container_width=True, height=300)

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
                    json_path = save_validated_json(raw_text, deck_name)
                    apkg_path = create_apkg(json_path, deck_name)

                    if os.path.exists(apkg_path):
                        st.success("Deck created successfully!")
                        with open(apkg_path, "rb") as f:
                            st.download_button(
                                label="Download Anki Deck (.apkg)",
                                data=f,
                                file_name=deck_name + ".apkg",
                                mime="application/octet-stream",
                                use_container_width=True,
                            )
                        st.caption("Saved to:")
                        st.code(os.path.abspath(apkg_path), language="")
                    else:
                        st.error("Failed to create the .apkg file.")
            except Exception as e:
                st.error(f"Error: {e}")

with preview_tab:
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
            st.dataframe(cards, use_container_width=True, height=360)

with history_tab:
    st.markdown("### Recent Files")
    col1, col2 = st.columns(2)
    # JSON history
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
                        use_container_width=True,
                    )
        except Exception as e:
            st.warning(f"Could not list JSONs: {e}")

    # Decks history
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
                            use_container_width=True,
                        )
                        st.caption(os.path.abspath(path))
                except Exception as e:
                    st.warning(f"Could not read {df}: {e}")
        except Exception as e:
            st.warning(f"Could not list Decks: {e}")

# --- Footer note ---
st.markdown("\n")
st.caption("Tip: Use the sidebar to switch between paste and upload modes, and load the sample to get started quickly.")
