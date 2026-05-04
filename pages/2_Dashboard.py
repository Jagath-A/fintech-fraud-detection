import streamlit as st
import pandas as pd
import plotly.express as px
import os
from utils.ui import apply_fintech_theme, format_inr

st.set_page_config(page_title="Dashboard", layout="wide")
apply_fintech_theme()

st.title("📊 Analytics Dashboard")

st.markdown("""
**Comprehensive visualization of fraud detection metrics and patterns.**

Track key performance indicators, fraud trends, transaction volumes, and risk distribution 
across your Indian fintech operations.
""")

st.markdown("---")

alerts_path = "data/alerts.csv"

if os.path.exists(alerts_path):
    try:
        df = pd.read_csv(alerts_path)
        
        if not df.empty:
            # Overall metrics
            st.subheader("Overall Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            total_transactions = len(df)
            fraud_count = (df['prediction'] == 1).sum() if 'prediction' in df.columns else 0
            fraud_rate = (fraud_count / total_transactions * 100) if total_transactions > 0 else 0
            avg_amount = df['amount'].mean() if 'amount' in df.columns else 0
            
            with col1:
                st.metric("Total Transactions", total_transactions)
            
            with col2:
                st.metric("Fraudulent", fraud_count)
            
            with col3:
                st.metric("Fraud Rate", f"{fraud_rate:.1f}%")
            
            with col4:
                st.metric("Average Transaction Amount", format_inr(avg_amount))
            
            st.divider()
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Fraud Distribution")
                if 'prediction' in df.columns:
                    fraud_dist = df['prediction'].value_counts().reset_index()
                    fraud_dist.columns = ['Status', 'Count']
                    fraud_dist['Status'] = fraud_dist['Status'].map({1: 'Fraud', 0: 'Legitimate'})
                    
                    fig = px.pie(fraud_dist, values='Count', names='Status', 
                                title="Transaction Status", color='Status',
                                color_discrete_map={'Fraud': '#ff4444', 'Legitimate': '#44ff44'})
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Risk Score Distribution")
                if 'risk' in df.columns:
                    fig = px.histogram(df, x='risk', nbins=20,
                                      title="Risk Score Distribution",
                                      labels={'risk': 'Risk Score', 'count': 'Frequency'})
                    fig.update_traces(marker_color='#ff8844')
                    st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Transaction Amount Analysis")
                if 'amount' in df.columns:
                    fig = px.box(df, y='amount', 
                                title="Transaction Amount Distribution",
                                labels={'amount': 'Transaction Amount (₹)'})
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Amount Deviation vs Risk")
                if 'amount_deviation' in df.columns and 'risk' in df.columns:
                    if 'prediction' in df.columns:
                        df['Status'] = df['prediction'].map({1: 'Fraud', 0: 'Legitimate'})
                        fig = px.scatter(df, x='amount_deviation', y='risk',
                                        color='Status',
                                        title="Amount Deviation vs Risk Score",
                                        labels={'amount_deviation': 'Deviation (₹)', 'risk': 'Risk Score'},
                                        color_discrete_map={'Fraud': '#ff4444', 'Legitimate': '#44ff44'})
                        st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available yet. Use Transaction Analyzer to see dashboard visualizations.")
            
    except Exception as e:
        st.error(f"Error loading dashboard data: {str(e)}")
else:
    st.warning("Data file not found. Use Transaction Analyzer to generate data.")
