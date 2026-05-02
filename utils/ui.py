import streamlit as st

from utils.formatting import format_inr


def apply_fintech_theme():
    st.markdown(
        """
        <style>
        :root {
            --fintech-text: #111827;
            --fintech-muted: #4b5563;
            --fintech-card: #f3f4f6;
            --fintech-border: #e5e7eb;
            --fintech-accent: #0f766e;
        }

        .stApp {
            background: #ffffff;
            color: var(--fintech-text);
        }

        [data-testid="stSidebar"] {
            background: #f8fafc;
            border-right: 1px solid var(--fintech-border);
        }

        h1, h2, h3, h4, h5, h6, p, label, span {
            color: var(--fintech-text);
        }

        [data-testid="stMetric"] {
            background: var(--fintech-card);
            border: 1px solid var(--fintech-border);
            border-radius: 8px;
            padding: 14px 16px;
            box-shadow: none;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: #f9fafb;
            border-color: var(--fintech-border);
            border-radius: 8px;
        }

        div.stButton > button[kind="primary"] {
            background: var(--fintech-accent);
            border-color: var(--fintech-accent);
            color: #ffffff;
            border-radius: 8px;
            font-weight: 600;
        }

        div.stButton > button {
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
