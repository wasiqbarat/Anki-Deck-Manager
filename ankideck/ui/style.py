import streamlit as st


def inject_base_styles():
    st.markdown(
        """
        <style>
            /* Base global scaling */
            html, body { font-size: 16px; }

            /* Base paddings */
            .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }

            /* Sidebar width and padding */
            [data-testid="stSidebar"] > div:first-child { padding-top: 1rem; padding-bottom: 1rem; }
            [data-testid="stSidebar"] { width: 280px; }

            /* Header and typography */
            h1 { font-size: 2rem; margin: 1rem 0 0.5rem 0; }
            h2 { font-size: 1.25rem; margin: 0.5rem 0; }
            h3 { font-size: 1.1rem; margin: 0.5rem 0; }
            .app-header { margin-top: 1.5rem; }
            .subtle { color: #6b7280; font-size: 1rem; }

            /* Cards/containers */
            .app-header { padding: 1rem 1.25rem; border-radius: 10px; background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%); border: 1px solid #e5e7eb; }
            .section-card { padding: 1rem; border-radius: 10px; border: 1px solid #e5e7eb; background: #ffffff; }
            .metric-card { padding: 0.75rem 1rem; border-radius: 8px; border: 1px solid #e5e7eb; background: #fafafa; }

            /* Buttons and inputs */
            .stButton > button, .stDownloadButton > button { border-radius: 8px; border: 1px solid #e5e7eb; padding: 0.5rem 0.9rem; font-size: 1rem; }
            [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea, [data-testid="stSelectbox"] > div > div { font-size: 1rem; }

            /* Generate button in Create New Deck: match sidebar colors */
            .adg-generate-marker + div.stButton > button,
            .adg-generate-marker ~ div.stButton > button {
                background: linear-gradient(180deg, #0B1220 0%, #0A0F1A 100%) !important; /* sidebar gradient */
                color: #E5E7EB !important;
                border: 1px solid #111827 !important;
                box-shadow: 0 6px 16px rgba(2, 6, 23, 0.25) !important;
            }
            .adg-generate-marker + div.stButton > button:hover,
            .adg-generate-marker ~ div.stButton > button:hover {
                background: linear-gradient(180deg, #0C1524 0%, #0A0F1A 100%) !important; /* slightly brighter hover */
            }
            .adg-generate-marker + div.stButton > button:focus,
            .adg-generate-marker ~ div.stButton > button:focus {
                outline: none !important;
                box-shadow: 0 0 0 3px rgba(148, 163, 184, 0.25) !important;
            }

            /* Also target by JS-injected class for maximum reliability */
            button.adg-generate-btn {
                background: linear-gradient(180deg, #0B1220 0%, #0A0F1A 100%) !important; /* sidebar gradient */
                color: #E5E7EB !important;
                border: 1px solid #111827 !important;
                border-radius: 8px !important;
                box-shadow: 0 6px 16px rgba(2, 6, 23, 0.25) !important;
            }
            button.adg-generate-btn:hover { background: linear-gradient(180deg, #0C1524 0%, #0A0F1A 100%) !important; }
            button.adg-generate-btn:focus {
                outline: none !important;
                box-shadow: 0 0 0 3px rgba(148, 163, 184, 0.25) !important;
            }

            /* Fallback: style Streamlit primary buttons globally to match sidebar */
            .stButton > button[kind="primary"],
            .stButton > button[data-testid="baseButton-primary"],
            .stButton > button.ef3psqc12 { /* some Streamlit builds add a stable class; safe fallback */
                background: linear-gradient(180deg, #0B1220 0%, #0A0F1A 100%) !important;
                color: #E5E7EB !important;
                border: 1px solid #111827 !important;
                border-radius: 8px !important;
                box-shadow: 0 6px 16px rgba(2, 6, 23, 0.25) !important;
            }
            .stButton > button[kind="primary"]:hover,
            .stButton > button[data-testid="baseButton-primary"]:hover,
            .stButton > button.ef3psqc12:hover {
                background: linear-gradient(180deg, #0C1524 0%, #0A0F1A 100%) !important;
            }
            .stButton > button[kind="primary"]:focus,
            .stButton > button[data-testid="baseButton-primary"]:focus,
            .stButton > button.ef3psqc12:focus {
                outline: none !important;
                box-shadow: 0 0 0 3px rgba(148, 163, 184, 0.25) !important;
            }

            /* Tabs: modern, animated segmented control style */
            /* Container (tab-list) styling */
            div[data-baseweb="tab-list"] {
                display: flex;
                gap: 6px;
                padding: 8px;
                border-radius: 14px;
                background: linear-gradient(180deg, rgba(255,255,255,0.9) 0%, rgba(248,250,252,0.85) 100%);
                border: 1px solid #e5e7eb;
                box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06), inset 0 1px 0 rgba(255,255,255,0.6);
                backdrop-filter: blur(4px);
                -webkit-backdrop-filter: blur(4px);
                overflow: auto;
                scrollbar-width: none;
                animation: tabBarAppear 420ms cubic-bezier(0.18, 0.89, 0.32, 1.28) both;
            }
            div[data-baseweb="tab-list"]::-webkit-scrollbar { display: none; }

            /* Individual tabs as buttons */
            button[role="tab"] {
                position: relative;
                border: 0;
                border-radius: 10px;
                background: transparent;
                color: #334155;
                padding: 0.55rem 0.95rem;
                font-size: 1rem;
                font-weight: 600;
                letter-spacing: 0.01em;
                transition: color 160ms ease, transform 200ms ease, background 220ms ease, box-shadow 220ms ease;
                box-shadow: 0 0 0 0 rgba(0,0,0,0);
            }
            button[role="tab"]:hover {
                color: #111827;
                transform: translateY(-1px);
            }
            /* Active tab */
            button[role="tab"][aria-selected="true"] {
                background: linear-gradient(180deg, #eef2ff 0%, #e0e7ff 100%);
                color: #111827;
                box-shadow: 0 6px 16px rgba(79, 70, 229, 0.15), inset 0 1px 0 rgba(255,255,255,0.8);
            }
            /* Subtle underline indicator on active tab (per-tab) */
            button[role="tab"]::after {
                content: "";
                position: absolute;
                left: 10px; right: 10px; bottom: -6px;
                height: 3px; border-radius: 3px;
                background: linear-gradient(90deg, #818cf8 0%, #4f46e5 100%);
                opacity: 0; transform: scaleX(0.5);
                transition: opacity 220ms ease, transform 240ms ease;
            }
            button[role="tab"][aria-selected="true"]::after { opacity: 1; transform: scaleX(1); }

            /* Optional ink bar for main tabs (positioned via JS) */
            div[data-baseweb="tab-list"].adg-main-tabs { position: relative; }
            div[data-baseweb="tab-list"].adg-main-tabs .adg-ink {
                position: absolute;
                left: 0; bottom: -6px; height: 4px; width: 0px;
                border-radius: 999px;
                background: linear-gradient(90deg, #60a5fa 0%, #a78bfa 50%, #4f46e5 100%);
                box-shadow: 0 6px 18px rgba(79, 70, 229, 0.25);
                transition: transform 320ms cubic-bezier(0.22, 1, 0.36, 1), width 320ms cubic-bezier(0.22, 1, 0.36, 1);
                pointer-events: none;
            }

            /* Compact the tab content spacing a bit */
            [data-baseweb="tab"] { padding: 0.5rem 0.9rem; font-size: 1rem; }

            /* Appear animation */
            @keyframes tabBarAppear {
                0% { opacity: 0; transform: translateY(-8px) scale(0.98); }
                100% { opacity: 1; transform: translateY(0) scale(1); }
            }

            /* Dataframe/table */
            [data-testid="stDataFrame"] div[role="grid"] * { font-size: 14px; line-height: 1.4; }

            /* Metrics */
            [data-testid="stMetricLabel"] { font-size: 0.95rem; }
            [data-testid="stMetricValue"] { font-size: 1.25rem; }

            /* Paragraph spacing */
            p, ul, ol { margin: 0.5rem 0; }

            /* Radio label size */
            [data-testid="stRadio"] label { font-size: 1rem; }

            /* Streamlit chrome */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}

            /* Sidebar redesign: darker theme, improved layout, and footer */
            [data-testid="stSidebar"] {
                position: relative;
                width: 280px; /* keep explicit width to avoid regressions */
                background: linear-gradient(180deg, #0B1220 0%, #0A0F1A 100%) !important;
                border-right: 1px solid rgba(2, 6, 23, 0.6);
                box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
            }
            /* Inner padding with extra bottom room for the footer */
            [data-testid="stSidebar"] > div:first-child {
                padding-top: 14px !important;
                padding-bottom: 68px !important; /* reserve space for footer */
                padding-left: 14px !important;
                padding-right: 14px !important;
            }
            /* Typography and base colors within sidebar */
            [data-testid="stSidebar"] * { color: #E5E7EB; }
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3,
            [data-testid="stSidebar"] h4 { color: #F3F4F6; }
            [data-testid="stSidebar"] .stCaption, [data-testid="stSidebar"] .stMarkdown p { color: #CBD5E1; }
            [data-testid="stSidebar"] hr, [data-testid="stSidebar"] .stDivider { border-color: rgba(148,163,184,0.18) !important; }
            /* Tighten spacing between header and divider inside sidebar */
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3,
            [data-testid="stSidebar"] h4 { margin-top: 0.25rem !important; margin-bottom: 0.25rem !important; }
            [data-testid="stSidebar"] hr { margin-top: 0.25rem !important; margin-bottom: 0.5rem !important; }

            /* Inputs and controls on dark sidebar */
            [data-testid="stSidebar"] [data-testid="stTextInput"] input,
            [data-testid="stSidebar"] [data-testid="stTextArea"] textarea,
            [data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div,
            [data-testid="stSidebar"] [data-baseweb="input"] input {
                background: #111827 !important;
                border-color: #374151 !important;
                color: #E5E7EB !important;
            }
            [data-testid="stSidebar"] [data-testid="stRadio"] label { color: #E5E7EB !important; }
            [data-testid="stSidebar"] [data-testid="stRadio"] svg { filter: drop-shadow(0 0 0 rgba(0,0,0,0)); }
            [data-testid="stSidebar"] button {
                background: #1F2937 !important;
                color: #E5E7EB !important;
                border: 1px solid #374151 !important;
                border-radius: 8px !important;
            }
            [data-testid="stSidebar"] button:hover { background: #273447 !important; }

            /* Expander styling in sidebar */
            [data-testid="stSidebar"] .st-expander {
                border: 1px solid rgba(148,163,184,0.25) !important;
                background: rgba(17,24,39,0.65) !important;
                border-radius: 10px !important;
                overflow: hidden !important; /* prevent white corners on summary */
            }
            /* Also cover newer Streamlit structure using data-testid */
            [data-testid="stSidebar"] [data-testid="stExpander"] {
                border: 1px solid rgba(148,163,184,0.25) !important;
                background: rgba(17,24,39,0.65) !important;
                border-radius: 10px !important;
                overflow: hidden !important;
            }
            [data-testid="stSidebar"] .st-expander > summary {
                color: #E5E7EB !important;
                background: #0F172A !important; /* dark header */
                padding: 0.6rem 0.9rem !important;
                border-bottom: 1px solid rgba(148,163,184,0.18) !important;
                list-style: none !important;
                border-top-left-radius: 10px !important;
                border-top-right-radius: 10px !important;
            }
            [data-testid="stSidebar"] [data-testid="stExpander"] summary {
                color: #E5E7EB !important;
                background: #0F172A !important; /* dark header */
                padding: 0.6rem 0.9rem !important;
                border-bottom: 1px solid rgba(148,163,184,0.18) !important;
                list-style: none !important;
                border-top-left-radius: 10px !important;
                border-top-right-radius: 10px !important;
            }
            /* Cover Baseweb accordion structures that use [role="button"] inside the expander header */
            [data-testid="stSidebar"] [data-testid="stExpander"] [role="button"] {
                background: #0F172A !important;
                color: #E5E7EB !important;
                border-bottom: 1px solid rgba(148,163,184,0.18) !important;
                border-top-left-radius: 10px !important;
                border-top-right-radius: 10px !important;
            }
            [data-testid="stSidebar"] [data-testid="stExpander"] [role="button"]:hover { background: #111827 !important; }
            [data-testid="stSidebar"] [data-testid="stExpander"] [role="button"] * { background: inherit !important; color: inherit !important; }
            /* Keep header dark when expanded and on hover/focus */
            [data-testid="stSidebar"] .st-expander[open] > summary { background: #0F172A !important; }
            [data-testid="stSidebar"] [data-testid="stExpander"] details[open] > summary { background: #0F172A !important; }
            [data-testid="stSidebar"] .st-expander > summary:hover,
            [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover { background: #111827 !important; }
            [data-testid="stSidebar"] .st-expander > summary:focus,
            [data-testid="stSidebar"] [data-testid="stExpander"] summary:focus { outline: none !important; }
            /* Ensure any inner wrappers don't introduce white backgrounds */
            [data-testid="stSidebar"] .st-expander > summary *,
            [data-testid="stSidebar"] [data-testid="stExpander"] summary * { background: inherit !important; }
            [data-testid="stSidebar"] .st-expander[open],
            [data-testid="stSidebar"] [data-testid="stExpander"] [open] { background: rgba(17,24,39,0.75) !important; }
            /* Ensure chevron/icon follows text color */
            [data-testid="stSidebar"] .st-expander > summary svg,
            [data-testid="stSidebar"] [data-testid="stExpander"] summary svg { color: #CBD5E1 !important; fill: currentColor !important; }
            [data-testid="stSidebar"] code { background: #0F172A; color: #E2E8F0; }
            /* Ensure code blocks in the sidebar match dark theme */
            [data-testid="stSidebar"] pre,
            [data-testid="stSidebar"] .stCodeBlock pre {
                background: #0F172A !important;
                color: #E2E8F0 !important;
                border: 1px solid #1F2937 !important;
                border-radius: 8px !important;
            }
            [data-testid="stSidebar"] pre code,
            [data-testid="stSidebar"] .stCodeBlock code {
                color: #E2E8F0 !important;
            }
            /* Neutralize token colors so they don't clash with dark bg */
            [data-testid="stSidebar"] pre code span,
            [data-testid="stSidebar"] .stCodeBlock code span {
                color: inherit !important;
            }

            /* Footer text at the bottom of the sidebar */
            [data-testid="stSidebar"]::after {
                content: "By Wasiq Barat";
                position: absolute;
                left: 16px;
                right: 16px;
                text-align: center;
                bottom: 14px;
                color: #94A3B8;
                font-size: 0.95rem;
                letter-spacing: 0.01em;
                border-top: 1px solid rgba(148,163,184,0.18);
                padding-top: 10px;
            }

            /* Floating action button for My Decks */
            .fab { position: fixed; right: 24px; bottom: 24px; z-index: 1000; }
            .fab .fab-btn {
                display: inline-flex; align-items: center; justify-content: center;
                width: 56px; height: 56px; border-radius: 50%;
                background: #0B1220; color: #fff; text-decoration: none;
                box-shadow: 0 6px 18px rgba(2,6,23,0.5);
                font-size: 28px; line-height: 1; border: 1px solid #111827;
            }
            .fab .fab-btn:hover { background: #0A0F1A; }
        </style>
        """,
        unsafe_allow_html=True,
    )
