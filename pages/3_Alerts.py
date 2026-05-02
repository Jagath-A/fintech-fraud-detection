import streamlit as st
import pandas as pd
import os
from utils.ui import apply_fintech_theme, format_inr

st.set_page_config(page_title="Alerts", layout="wide")
apply_fintech_theme()

# Page header
st.title("Transaction Alerts")
st.markdown("Monitor and review all flagged transactions")

alerts_path = "data/alerts.csv"

if os.path.exists(alerts_path) and os.path.getsize(alerts_path) > 0:
    try:
        df = pd.read_csv(alerts_path)
        
        # Parse timestamp column if it exists
        if 'time' in df.columns:
            try:
                df['time'] = pd.to_datetime(df['time'])
                # Sort by timestamp in descending order (latest first)
                df = df.sort_values('time', ascending=False).reset_index(drop=True)
            except Exception:
                # If parsing fails, keep original order
                pass
        
        if not df.empty and len(df) > 0:
            # Statistics Section
            st.markdown("### Overview")
            
            col1, col2, col3, col4 = st.columns(4, gap="medium")
            
            fraud_count = (df['prediction'] == 1).sum() if 'prediction' in df.columns else 0
            total_count = len(df)
            legitimate_count = total_count - fraud_count
            avg_risk = df['risk'].mean() if 'risk' in df.columns else 0
            
            with col1:
                st.metric(label="Total Records", value=total_count)
            
            with col2:
                st.metric(label="Flagged as Fraud", value=fraud_count)
            
            with col3:
                st.metric(label="Legitimate", value=legitimate_count)
            
            with col4:
                st.metric(label="Average Risk", value=f"{avg_risk:.2%}")
            
            st.divider()
            
            # Filter Section
            st.markdown("### Filter & Display")
            
            filter_container = st.container()
            with filter_container:
                col1, col2, col3 = st.columns(3, gap="medium")
                
                with col1:
                    show_fraud_only = st.checkbox(
                        "Fraudulent Transactions Only",
                        value=False,
                        help="When checked, shows only transactions flagged as fraud"
                    )
                
                with col2:
                    risk_threshold = st.slider(
                        "Minimum Risk Score",
                        min_value=0.0,
                        max_value=1.0,
                        value=0.0,
                        step=0.05,
                        help="Filter alerts by minimum risk threshold"
                    )
                
                with col3:
                    max_results = st.number_input(
                        "Results to Display",
                        min_value=1,
                        max_value=len(df),
                        value=min(50, len(df)),
                        step=10,
                        help="Limit the number of results displayed"
                    )
            
            st.divider()
            
            # Apply filters
            filtered_df = df.copy()
            
            if show_fraud_only and 'prediction' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['prediction'] == 1]
            
            if 'risk' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['risk'] >= risk_threshold]
            
            # Limit results
            filtered_df = filtered_df.head(max_results)
            
            # Display table
            if not filtered_df.empty:
                st.markdown(f"### Results ({len(filtered_df)} of {len(df)} records)")
                
                # Format display dataframe
                display_df = filtered_df.copy()
                
                # Format columns for better readability
                if 'time' in display_df.columns:
                    display_df['time'] = display_df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
                
                if 'amount' in display_df.columns:
                    display_df['amount'] = display_df['amount'].apply(format_inr)
                
                if 'avg_user_amount' in display_df.columns:
                    display_df['avg_user_amount'] = display_df['avg_user_amount'].apply(format_inr)
                
                if 'account_balance' in display_df.columns:
                    display_df['account_balance'] = display_df['account_balance'].apply(format_inr)
                
                if 'distance_from_last_transaction' in display_df.columns:
                    display_df['distance_from_last_transaction'] = display_df['distance_from_last_transaction'].apply(lambda x: f"{x:.1f}km")
                
                if 'risk' in display_df.columns:
                    display_df['risk'] = display_df['risk'].apply(lambda x: f"{x:.2%}")
                
                if 'prediction' in display_df.columns:
                    display_df['prediction'] = display_df['prediction'].map({1: 'Fraud', 0: 'Legitimate'})
                
                # Device and location changes
                if 'device_change' in display_df.columns:
                    display_df['device_change'] = display_df['device_change'].map({1: 'Yes', 0: 'No'})
                
                if 'location_change' in display_df.columns:
                    display_df['location_change'] = display_df['location_change'].map({1: 'Out-of-State Transaction', 0: 'Domestic Transaction'})
                
                if 'new_device_flag' in display_df.columns:
                    display_df['new_device_flag'] = display_df['new_device_flag'].map({1: 'Yes', 0: 'No'})
                
                # Reorder columns for better display - show key fraud indicators
                column_order = [
                    'time', 'amount', 'avg_user_amount', 'account_balance',
                    'transaction_velocity', 'device_change', 'location_change',
                    'distance_from_last_transaction', 'risk', 'prediction'
                ]
                available_cols = [col for col in column_order if col in display_df.columns]
                display_df = display_df[available_cols]
                
                # Rename columns for cleaner display
                display_df = display_df.rename(columns={
                    'time': 'Time',
                    'amount': 'Transaction Amount (₹)',
                    'avg_user_amount': 'Customer Average Transaction (₹)',
                    'account_balance': 'Account Balance (₹)',
                    'transaction_velocity': 'Transaction Velocity',
                    'device_change': 'Device Change',
                    'location_change': 'Transaction Type',
                    'distance_from_last_transaction': 'Distance From Last Transaction',
                    'risk': 'Risk',
                    'prediction': 'Prediction',
                })
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Time": st.column_config.TextColumn(width="small"),
                        "Transaction Amount (₹)": st.column_config.TextColumn(width="small"),
                        "Customer Average Transaction (₹)": st.column_config.TextColumn(width="small"),
                        "Account Balance (₹)": st.column_config.TextColumn(width="small"),
                        "Transaction Velocity": st.column_config.TextColumn(width="small"),
                        "Device Change": st.column_config.TextColumn(width="small"),
                        "Transaction Type": st.column_config.TextColumn(width="medium"),
                        "Distance From Last Transaction": st.column_config.TextColumn(width="small"),
                        "Risk": st.column_config.TextColumn(width="small"),
                        "Prediction": st.column_config.TextColumn(width="small"),
                    }
                )
            else:
                st.info("No alerts match the selected filters. Adjust your filter criteria and try again.")
        else:
            st.info("No alerts have been recorded yet. Start by using Transaction Analyzer to generate transaction records.")
            
    except pd.errors.ParserError as e:
        st.error(f"Error parsing CSV file: {str(e)}")
        st.caption("The alerts.csv file may be corrupted. Try making new predictions to regenerate the file.")
        
    except Exception as e:
        st.error(f"Error loading alerts: {str(e)}")
        st.caption(f"Error type: {type(e).__name__}")
else:
    st.warning("Alerts file not found or is empty.")
    st.info("Start by using Transaction Analyzer to create alert records.")
