import streamlit as st
from utils.ui import apply_fintech_theme

st.set_page_config(
    page_title="Indian Fintech Fraud Detection",
    layout="wide"
)

apply_fintech_theme()

# ---- MAIN PAGE ----
st.title("Indian Fintech Fraud Detection System")

st.markdown("""
Clean, professional transaction monitoring for Indian fintech operations.

### Features:
- Detect fraudulent transactions using Machine Learning
- Risk scoring for each transaction
- Alert system for suspicious activity
- Transaction monitoring dashboard

---

### How to use:
1. Go to **Transaction Analyzer** to screen transactions  
2. Check **Alerts** page for flagged fraud cases  
3. View **Dashboard** for insights  
""")

st.info("Use the sidebar to navigate between pages")
