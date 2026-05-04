import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helper import predict, save_alert
from utils.ui import apply_fintech_theme, format_inr

st.set_page_config(page_title="Transaction Analyzer", layout="wide")

apply_fintech_theme()

st.title("🔍 Transaction Analyzer")
st.markdown("""
**Real-time fraud detection for Indian digital payments and banking transactions.**

Analyze any transaction in seconds. Get instant risk assessment based on behavioral patterns, 
device changes, location anomalies, and more.
""")

# Check model status
try:
    import joblib
    model_status = "Ready"
    model_ready = os.path.exists("model/fraud_model.pkl") and os.path.exists("model/scaler.pkl")
except Exception as e:
    model_status = f"Error: {str(e)}"
    model_ready = False

# Display model status in sidebar
status_indicator = "✅" if model_ready else "⏳"
st.sidebar.markdown(f"**{status_indicator} System Status**: {model_status}")

if not model_ready:
    st.warning("⏳ System initializing. Models will be available in a moment.")

st.markdown("---")

st.markdown("### 📋 Transaction Information")

# Create tabs for better organization
tab1, tab2, tab3 = st.tabs(["Amount & Profile", "Behavior Indicators", "Account Details"])

with tab1:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("**Current Transaction**")
        amount = st.number_input(
            "Transaction Amount (₹)",
            min_value=0.0,
            step=100.0,
            key="amount",
            help="The transaction amount to be screened"
        )
    
    with col2:
        st.markdown("**Customer Profile**")
        avg_user_amount = st.number_input(
            "Customer Average Transaction (₹)",
            min_value=0.0,
            step=100.0,
            key="avg_amount",
            help="Typical transaction amount for this customer"
        )

with tab2:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        transaction_frequency = st.number_input(
            "Transaction Frequency",
            min_value=0,
            step=1,
            key="freq",
            help="Number of transactions made by this customer (monthly average)"
        )
        
        transaction_velocity = st.number_input(
            "Transaction Velocity",
            min_value=0,
            step=1,
            key="velocity",
            help="Number of transactions in last hour"
        )
    
    with col2:
        device_change = st.selectbox(
            "Device Change",
            [0, 1],
            format_func=lambda x: "No" if x == 0 else "Yes",
            key="device_change",
            help="Is this transaction from a different device than usual?"
        )
        
        location_change = st.selectbox(
            "Transaction Location Type",
            [0, 1],
            format_func=lambda x: "Domestic Transaction" if x == 0 else "Out-of-State Transaction",
            key="location_change",
            help="Is this transaction domestic or from a different state than usual?"
        )

with tab3:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        account_balance = st.number_input(
            "Account Balance (₹)",
            min_value=0.0,
            step=100.0,
            key="balance",
            help="Current account balance"
        )
        
        new_device_flag = st.selectbox(
            "New Device Flag",
            [0, 1],
            format_func=lambda x: "No" if x == 0 else "Yes",
            key="new_device",
            help="Is this a newly registered device?"
        )
    
    with col2:
        distance_from_last_transaction = st.number_input(
            "Distance from Last Transaction (km)",
            min_value=0.0,
            step=1.0,
            key="distance",
            help="Geographic distance from last transaction location"
        )

# Input validation and model check
if not model_ready:
    st.warning("System files are initializing. The model will be downloaded on first use.")

st.markdown("---")

if st.button("Screen Transaction", type="primary", use_container_width=True):
    # Validate inputs
    if amount == 0 and avg_user_amount == 0:
        st.warning("Please enter at least one non-zero amount to proceed")
    else:
        try:
            # Prepare data in the format expected by the model
            data = {
                "amount": float(amount),
                "avg_user_amount": float(avg_user_amount),
                "transaction_frequency": int(transaction_frequency),
                "transaction_velocity": int(transaction_velocity),
                "device_change": int(device_change),
                "location_change": int(location_change),
                "new_device_flag": int(new_device_flag),
                "account_balance": float(account_balance),
                "distance_from_last_transaction": float(distance_from_last_transaction)
            }
            
            # Make prediction using the helper function
            prediction, risk_score = predict(data)
            
            # Store results in session state
            st.session_state.last_prediction = prediction
            st.session_state.last_risk = risk_score
            st.session_state.input_data = data
            st.session_state.has_prediction = True
            
        except ValueError as ve:
            st.error(f"Input Error: {str(ve)}")
            st.info("Please ensure all fields are filled with valid numbers")
            
        except FileNotFoundError as fe:
            st.error("Model files not found")
            st.info("The model files are being downloaded. This may take a moment. Try again in a few seconds.")
            
        except Exception as e:
            st.error(f"Analysis Error: {str(e)}")
            st.caption(f"Details: {type(e).__name__}")

# Display results if prediction was made
if st.session_state.get("has_prediction", False):
    st.markdown("---")
    
    pred = st.session_state.last_prediction
    risk = st.session_state.last_risk
    data = st.session_state.input_data
    
    # Determine risk level
    if risk >= 0.8:
        risk_level = "CRITICAL"
        risk_color = "red"
    elif risk >= 0.6:
        risk_level = "HIGH"
        risk_color = "orange"
    elif risk >= 0.4:
        risk_level = "MEDIUM"
        risk_color = "yellow"
    else:
        risk_level = "LOW"
        risk_color = "green"
    
    # Header with status
    st.markdown("### Transaction Review")
    
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        if pred == 1:
            st.metric("Status", "FLAGGED")
        else:
            st.metric("Status", "APPROVED")
    
    with status_col2:
        st.metric("Risk Level", risk_level)
    
    with status_col3:
        st.metric("Risk Score", f"{risk:.1%}")
    
    st.divider()
    
    # Main assessment section
    st.markdown("### Transaction Details")
    
    detail_col1, detail_col2, detail_col3 = st.columns(3)
    
    with detail_col1:
        st.metric("Transaction Amount", format_inr(data['amount']))
        st.metric("Customer Average", format_inr(data['avg_user_amount']))
    
    with detail_col2:
        deviation = data['amount'] - data['avg_user_amount']
        st.metric("Deviation", format_inr(abs(deviation)), f"{('Above' if deviation > 0 else 'Below')} average")
        percentage_diff = (abs(deviation) / data['avg_user_amount'] * 100) if data['avg_user_amount'] > 0 else 0
        st.metric("% Difference", f"{percentage_diff:.0f}%")
    
    with detail_col3:
        st.metric("Account Balance", format_inr(data['account_balance']))
        st.metric("Frequency", f"{data['transaction_frequency']} txns/month")
    
    st.divider()
    
    # Risk factors summary
    st.markdown("### Risk Factors")
    
    risk_factors = []
    if data['transaction_velocity'] > 5:
        risk_factors.append(f"High velocity: {data['transaction_velocity']} transactions in last hour")
    if data['device_change'] == 1:
        risk_factors.append("Device changed from typical pattern")
    if data['location_change'] == 1:
        risk_factors.append("Out-of-state transaction compared with typical pattern")
    if data['new_device_flag'] == 1:
        risk_factors.append("Transaction from newly registered device")
    if abs(data['amount'] - data['avg_user_amount']) > data['avg_user_amount']:
        risk_factors.append("Amount significantly deviates from customer profile")
    if data['distance_from_last_transaction'] > 500:
        risk_factors.append(f"Large geographic distance: {data['distance_from_last_transaction']:.0f} km")
    
    if risk_factors:
        with st.container(border=True):
            for i, factor in enumerate(risk_factors, 1):
                st.markdown(f"- {factor}")
    else:
        st.success("No major risk factors detected")
    
    st.divider()
    
    # Fraud detected flow
    if pred == 1:
        st.markdown("### Alert: Suspicious Transaction Detected")
        
        alert_container = st.container(border=True)
        with alert_container:
            col_risk, col_msg = st.columns([1, 3])
            
            with col_risk:
                st.markdown(f"**Risk: {risk_level}**")
                st.markdown(f"*{risk:.1%}*")
            
            with col_msg:
                if risk >= 0.8:
                    st.markdown("**Critical Alert**: Strong indicators of fraudulent activity. Immediate action recommended.")
                elif risk >= 0.6:
                    st.markdown("**High Alert**: Multiple suspicious indicators detected. Manual review advised.")
                else:
                    st.markdown("**Warning**: Some unusual patterns detected. Consider additional verification.")
        
        st.markdown("### Recommended Actions")
        
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            block_btn = st.button(
                "Block Transaction",
                key="block_btn",
                use_container_width=True,
                help="Immediately decline this transaction"
            )
            if block_btn:
                st.info("Transaction has been blocked. Customer may contact support to verify.")
        
        with action_col2:
            investigate_btn = st.button(
                "Flag for Review",
                key="investigate_btn",
                use_container_width=True,
                help="Flag for further review by fraud team"
            )
            if investigate_btn:
                try:
                    save_alert(data, pred, risk)
                    st.success("Transaction flagged for investigation. Added to alerts queue.")
                except Exception as e:
                    st.error(f"Failed to flag transaction: {str(e)}")
        
        with action_col3:
            review_btn = st.button(
                "Override & Approve",
                key="approve_btn",
                use_container_width=True,
                help="Override and approve transaction after verification"
            )
            if review_btn:
                try:
                    data["transaction_id"] = "manual_override"
                    save_alert(data, 0, 0.0)  # Log as legitimate
                    st.success("Transaction approved and logged.")
                except Exception as e:
                    st.error(f"Failed to approve: {str(e)}")
    
    # Safe transaction flow
    else:
        st.markdown("### Confirmation: Transaction Approved")
        
        approval_container = st.container(border=True)
        with approval_container:
            col_check, col_msg = st.columns([1, 3])
            
            with col_check:
                st.markdown("**Status: CLEAR**")
                st.markdown(f"*{risk:.1%} risk*")
            
            with col_msg:
                if risk < 0.2:
                    st.markdown("Excellent match with customer profile. Low fraud risk.")
                else:
                    st.markdown("Transaction characteristics are consistent with customer behavior.")
        
        st.markdown("### Summary")
        
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.markdown("- Amount within typical range")
            st.markdown("- Customer profile match")
            st.markdown("- No suspicious patterns")
        
        with summary_col2:
            st.markdown(f"**Confidence**: {(1-risk)*100:.0f}%")
            st.markdown(f"**Recommendation**: Process normally")
        
        st.divider()
        
        log_col1, log_col2 = st.columns([4, 1])
        
        with log_col1:
            st.caption("Optionally log this transaction for record-keeping")
        
        with log_col2:
            if st.button("Log Transaction", use_container_width=True):
                try:
                    save_alert(data, pred, risk)
                    st.success("Transaction logged to system.")
                except Exception as e:
                    st.error(f"Failed to log: {str(e)}")
else:
    st.info("Enter transaction details above and click 'Screen Transaction' to analyze")
