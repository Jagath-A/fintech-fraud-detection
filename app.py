import streamlit as st
from utils.ui import apply_fintech_theme

st.set_page_config(
    page_title="Indian Fintech Fraud Detection",
    layout="wide"
)

apply_fintech_theme()

# ---- MAIN PAGE ----
col1, col2 = st.columns([3, 1])

with col1:
    st.title("🛡️ Indian Fintech Fraud Detection System")

st.markdown("""
**Clean, professional transaction monitoring for Indian fintech operations.**

---

### ✨ Features:
- **Real-time Screening**: Detect fraudulent transactions using advanced Machine Learning
- **Risk Analysis**: Comprehensive fraud risk scoring for every transaction (₹ amounts)
- **Alert System**: Automatic flagging of suspicious activities for manual review
- **Analytics Dashboard**: Visual insights into fraud patterns and transaction trends
- **Indian Context**: Built specifically for Indian digital payments and banking

---

### 🚀 Quick Start:
""")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    ### 1️⃣ Analyze Transactions
    
    Use the **Transaction Analyzer** to screen transactions in real-time. Input customer details, transaction amount (₹), and behavioral indicators for immediate fraud risk assessment.
    """)

with col2:
    st.markdown("""
    ### 2️⃣ Review Alerts
    
    Check the **Alerts** page to review all flagged transactions. Filter by fraud status, risk score, and apply custom thresholds to catch suspicious patterns.
    """)

with col3:
    st.markdown("""
    ### 3️⃣ Monitor Trends
    
    View the **Dashboard** for comprehensive fraud detection metrics, transaction distribution, and risk score patterns across your platform.
    """)

st.markdown("---")

# System Information
with st.container(border=True):
    st.markdown("### 📊 System Status")
    
    import os
    model_status = "✅ Ready" if os.path.exists("model/fraud_model.pkl") else "❌ Initializing"
    data_status = "✅ Active" if os.path.exists("data/alerts.csv") else "⏳ Pending First Transaction"
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**ML Model**: {model_status}")
    with col2:
        st.info(f"**Transaction Log**: {data_status}")
