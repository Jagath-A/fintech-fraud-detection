import streamlit as st

from utils.formatting import format_inr


def apply_fintech_theme():
    st.markdown(
        """
        <style>
        :root {
            --fintech-primary: #1e40af;
            --fintech-text: #0f172a;
            --fintech-muted: #475569;
            --fintech-card: #f8fafc;
            --fintech-border: #e2e8f0;
            --fintech-success: #059669;
            --fintech-warning: #d97706;
            --fintech-danger: #dc2626;
        }

        .stApp {
            background: #ffffff;
            color: var(--fintech-text);
        }

        [data-testid="stSidebar"] {
            background: #f1f5f9;
            border-right: 1px solid var(--fintech-border);
        }

        h1, h2, h3, h4, h5, h6 {
            color: var(--fintech-text);
            font-weight: 600;
        }

        p, label, span {
            color: var(--fintech-text);
        }

        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid var(--fintech-border);
            border-radius: 10px;
            padding: 16px 18px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }

        [data-testid="stMetric"] > div {
            font-weight: 500;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: #ffffff;
            border: 1px solid var(--fintech-border);
            border-color: var(--fintech-border);
            border-radius: 10px;
            padding: 18px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }

        div.stButton > button[kind="primary"] {
            background: var(--fintech-primary);
            border-color: var(--fintech-primary);
            color: #ffffff;
            border-radius: 8px;
            font-weight: 600;
            padding: 10px 24px;
        }

        div.stButton > button[kind="primary"]:hover {
            background: #1e3a8a;
            border-color: #1e3a8a;
        }

        div.stButton > button {
            border-radius: 8px;
            font-weight: 500;
        }

        .stDivider {
            margin: 24px 0;
        }

        .stTabs [data-baseweb="tab-list"] button {
            border-bottom: 2px solid transparent;
        }

        .stTabs [aria-selected="true"] {
            border-bottom-color: var(--fintech-primary);
            color: var(--fintech-primary);
        }

        [data-testid="stAlertContainer"] > div {
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
