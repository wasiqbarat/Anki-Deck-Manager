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

            /* Tabs */
            [data-baseweb="tab"] { padding: 0.5rem 0.9rem; font-size: 1rem; }

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
