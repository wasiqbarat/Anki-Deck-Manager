"""UI module for Streamlit rendering.

Provides tab renderers to keep main.py lean.
"""
from .helpers import parse_cards_from_text, SAMPLE_JSON
from .style import inject_base_styles
from .editor import render_editor_tab
from .mydecks import render_mydecks_tab
from .preview import render_preview_tab
from .history import render_history_tab
from .sidebar import render_sidebar
