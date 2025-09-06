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

            /* Floating action button for My Decks */
            .fab { position: fixed; right: 24px; bottom: 24px; z-index: 1000; }
            .fab .fab-btn {
                display: inline-flex; align-items: center; justify-content: center;
                width: 52px; height: 52px; border-radius: 50%;
                background: #4F46E5; color: #fff; text-decoration: none;
                box-shadow: 0 6px 18px rgba(0,0,0,0.15);
                font-size: 28px; line-height: 1; border: 1px solid #4338CA;
            }
            .fab .fab-btn:hover { background: #4338CA; }
        </style>
        """,
        unsafe_allow_html=True,
    )
