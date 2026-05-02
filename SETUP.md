# Fraud Detection System - Setup Guide

## Overview

AI-powered Streamlit application for real-time transaction fraud detection using machine learning.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Fix NumPy Compatibility (if needed)

```bash
python -m pip install "numpy<2" --upgrade
```

### 3. Generate Machine Learning Models

```bash
python generate_models.py
```

This creates:

- `model/fraud_model.pkl` - Random Forest classifier (1000 training samples)
- `model/scaler.pkl` - StandardScaler for feature normalization

**Note**: If you have your own trained models, replace these files. They must be scikit-learn compatible pickle files.

### 4. Run the Application

```bash
streamlit run app.py
```

The app will be available at:

- **Local**: http://localhost:8501
- **Network**: http://10.42.241.12:8501 (or your local IP)

## Project Structure

```
fintech-fraud-detection/
├── app.py                    # Main Streamlit app (home page)
├── requirements.txt          # Python dependencies
├── generate_models.py        # Script to create test models
├── test_model.py            # Diagnostic tool for model loading
│
├── model/                   # ML models (generated)
│   ├── fraud_model.pkl      # Trained classifier
│   └── scaler.pkl           # Feature scaler
│
├── data/
│   └── alerts.csv           # Transaction alerts log
│
├── utils/
│   └── helper.py            # Core ML logic & data handling
│
└── pages/                   # Streamlit multi-page app
    ├── 1_Transaction_Analyzer.py # Transaction screening interface
    ├── 2_Dashboard.py            # Analytics visualizations
    └── 3_Alerts.py               # Alerts viewer with filtering
```

## Pages Overview

### Home (app.py)

- Application introduction
- Feature overview
- Navigation guide

### Transaction Analyzer (1_Transaction_Analyzer.py)

- Input current transaction and customer average
- Get instant fraud prediction with risk score
- Actions: Block, Investigate, or Approve transaction
- Realistic banking system interface

### Alerts (2_Alerts.py)

- View all flagged transactions (sorted by timestamp)
- Filter by fraud status and risk score
- Formatted table with amounts, deviations, and risk metrics
- Pagination and statistics

### Dashboard (3_Dashboard.py)

- Fraud distribution pie chart
- Risk score histogram
- Transaction amount analysis
- Amount deviation vs risk scatter plot
- Overall fraud metrics

### About (4_About.py)

- System documentation
- How the model works
- Technical stack information

## Key Features

✓ **Real-time Predictions**

- Instantly screen transactions
- Get fraud probability and binary classification

✓ **Risk Assessment**

- Calculates amount deviation from user profile
- Assigns risk score (0-100%)
- Dynamic risk levels: CRITICAL, HIGH, MEDIUM, LOW

✓ **Professional Interface**

- Clean, minimal dashboard design
- Financial system-appropriate UI
- Clear action buttons for operators

✓ **Data Persistence**

- Automatic transaction logging
- CSV-based alerts database
- Historical transaction review

✓ **Error Handling**

- Automatic model file validation
- Corrupted file detection and re-download
- Detailed error diagnostics

## Model Information

### Features

1. **amount** - Current transaction amount
2. **avg_user_amount** - Customer's typical transaction amount
3. **amount_deviation** - Calculated as (amount - avg_user_amount)

### Model Type

- **Algorithm**: Random Forest Classifier
- **Features**: 3
- **Training Samples**: 1000
- **Output**: Binary (Fraud/Legitimate) + Probability

### Scaler

- **Type**: StandardScaler (sklearn)
- **Function**: Normalizes features for model input

## Troubleshooting

### Models won't load

```bash
# Check model integrity
python test_model.py

# Regenerate models
python generate_models.py
```

### NumPy compatibility issues

```bash
python -m pip install "numpy<2" --upgrade
```

### Port already in use

```bash
streamlit run app.py --server.port=8503
```

### CSV errors when no alerts exist

- Alerts CSV is created with header on first run
- Safe to delete `data/alerts.csv` - will be recreated
- App handles missing files gracefully

## Dependencies

Core libraries:

- **streamlit** - Web UI framework
- **pandas** - Data manipulation
- **scikit-learn** - Machine learning
- **joblib** - Model serialization
- **numpy** - Numerical computing
- **requests** - HTTP client
- **plotly** - Interactive charts
- **matplotlib** - Static visualizations

See `requirements.txt` for specific versions.

## API Reference

### helper.py Functions

```python
# Load and process prediction
prediction, risk_score = predict({"amount": 500, "avg_user_amount": 200})

# Log transaction to alerts
save_alert(
    {"amount": 500, "avg_user_amount": 200},
    prediction=1,
    risk=0.85
)
```

Returns:

- `prediction` - 1 (Fraud) or 0 (Legitimate)
- `risk_score` - Float 0-1 (fraud probability)

## Notes for Developers

- Models are lazy-loaded on first import of helper.py
- Streamlit uses session state for UI result persistence
- CSV operations check for file existence before reading
- Error messages include diagnostic information for debugging
- All user inputs are validated before passing to model

## Production Considerations

For production deployment:

1. Replace generated models with actual trained models
2. Use a proper database instead of CSV
3. Add transaction logging for audit trails
4. Implement rate limiting for API
5. Add authentication layer
6. Use environment variables for sensitive data
7. Deploy with proper SSL/TLS certificates
8. Monitor model drift and performance metrics

## License & Credits

Built with Streamlit, scikit-learn, and pandas.
