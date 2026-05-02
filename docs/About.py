import streamlit as st

st.set_page_config(page_title="About", layout="wide")

st.title("ℹ️ About This Application")

st.markdown("""
## AI-Powered Fraud Detection System

This application demonstrates a real-world transaction monitoring system 
that uses machine learning to detect potentially fraudulent transactions.

---

### 🎯 Purpose
The system analyzes financial transactions and assigns a fraud risk score 
to help identify suspicious activity in real-time.

### 🔬 How It Works

1. **Data Input**: Enter transaction amount and user's average transaction amount
2. **Preprocessing**: Calculate deviation metrics and scale features
3. **Model Prediction**: ML model analyzes the transaction
4. **Risk Scoring**: Returns fraud probability and binary prediction
5. **Alert System**: Saves flagged transactions for review

### 📊 Key Features

- **Real-time Predictions**: Instant fraud detection on any transaction
- **Risk Scoring**: Probability-based fraud risk (0-100%)
- **Alert Management**: Track all flagged transactions
- **Dashboard**: Visual analytics of fraud patterns
- **Historical Analysis**: Review past predictions and alerts

### 🧠 Machine Learning Model

- **Algorithm**: Trained classification model (model file provided via download)
- **Features**: Amount, average user amount, and calculated deviations
- **Scaling**: StandardScaler for feature normalization
- **Output**: Binary classification (Fraud/Legitimate) + probability score

### 📈 Navigation

| Page | Purpose |
|------|---------|
| **Transaction Analyzer** | Test new transactions and get instant fraud analysis |
| **Alerts** | View all flagged transactions with filtering options |
| **Dashboard** | Analyze fraud patterns and trends |
| **About** | Learn more about the system |

### 🔒 Data & Privacy

- Predictions are processed locally
- Alerts are saved to local CSV storage
- No external API calls for predictions (model downloaded on first run)

### ⚙️ Technical Stack

- **Frontend**: Streamlit (Python web framework)
- **ML Framework**: Scikit-learn
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib

---

### 📝 Version Info
- **Version**: 1.0
- **Last Updated**: 2024
- **Status**: Active

For questions or improvements, refer to the project README.
""")

st.divider()

st.subheader("Quick Start")
st.markdown("""
1. Go to **Transaction Analyzer**
2. Enter a transaction amount (e.g., ₹500)
3. Enter the user's average transaction amount (e.g., ₹200)
4. Click "Screen Transaction" to see the fraud risk assessment
5. Review alerts and dashboard for insights
""")
