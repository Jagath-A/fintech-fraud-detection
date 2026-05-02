#!/usr/bin/env python
"""Generate fraud detection model trained on realistic transaction data"""

import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
from utils.formatting import format_inr

# Create output directory
model_dir = os.path.join(os.path.dirname(__file__), "model")
os.makedirs(model_dir, exist_ok=True)

print("Training fraud detection model on realistic dataset...\n")

# Load the realistic fraud dataset
dataset_path = os.path.join(os.path.dirname(__file__), "data", "fraud_dataset_realistic.csv")

if not os.path.exists(dataset_path):
    print(f"Error: Dataset not found at {dataset_path}")
    print("Please ensure fraud_dataset_realistic.csv is in the data/ directory")
    exit(1)

# Read the dataset
df = pd.read_csv(dataset_path)
print(f"Dataset loaded: {len(df)} transactions")

# Feature engineering - select important features for fraud detection
features_to_use = [
    'amount',
    'avg_user_amount',
    'transaction_frequency',
    'transaction_velocity',
    'device_change',
    'location_change',
    'new_device_flag',
    'account_balance',
    'distance_from_last_transaction'
]

print(f"\nSelected features: {features_to_use}")

# Handle missing values
df_model = df[features_to_use + ['is_fraud']].copy()

# Fill missing numeric values with median
for col in features_to_use:
    if df_model[col].isnull().any():
        df_model[col].fillna(df_model[col].median(), inplace=True)
        print(f"  Filled {df_model[col].isnull().sum()} missing values in {col}")

# Prepare training data
X = df_model[features_to_use].values
y = df_model['is_fraud'].values

print(f"\nTraining data summary:")
print(f"  Total samples: {len(X)}")
print(f"  Number of features: {X.shape[1]}")
print(f"  Fraud cases: {y.sum()} ({y.sum()/len(y)*100:.1f}%)")
print(f"  Legitimate cases: {(1-y).sum()} ({(1-y).sum()/len(y)*100:.1f}%)")

# Create and train the model
print("\nTraining Random Forest classifier...")
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1,
    class_weight='balanced'  # Handle class imbalance
)
model.fit(X, y)

print("Model trained successfully!")
print(f"  Feature importances:")
for feat, imp in zip(features_to_use, model.feature_importances_):
    print(f"    {feat}: {imp:.4f}")

# Create and fit the scaler
print("\nFitting StandardScaler...")
scaler = StandardScaler()
scaler.fit(X)

print("Scaler fitted successfully!")

# Save models
model_path = os.path.join(model_dir, "fraud_model.pkl")
scaler_path = os.path.join(model_dir, "scaler.pkl")
features_path = os.path.join(model_dir, "features.pkl")

print(f"\nSaving models...")
joblib.dump(model, model_path)
joblib.dump(scaler, scaler_path)
joblib.dump(features_to_use, features_path)  # Save feature names

print(f"✓ Model saved: {model_path} ({os.path.getsize(model_path)} bytes)")
print(f"✓ Scaler saved: {scaler_path} ({os.path.getsize(scaler_path)} bytes)")
print(f"✓ Features saved: {features_path} ({os.path.getsize(features_path)} bytes)")

# Test the model with sample transactions
print("\nTesting with sample transactions...")
test_samples = [
    {
        'amount': 500,
        'avg_user_amount': 2000,
        'transaction_frequency': 8,
        'transaction_velocity': 2,
        'device_change': 0,
        'location_change': 0,
        'new_device_flag': 0,
        'account_balance': 50000,
        'distance_from_last_transaction': 2.5
    },
    {
        'amount': 10000,
        'avg_user_amount': 500,
        'transaction_frequency': 1,
        'transaction_velocity': 10,
        'device_change': 1,
        'location_change': 1,
        'new_device_flag': 1,
        'account_balance': 5000,
        'distance_from_last_transaction': 2000
    },
    {
        'amount': 2500,
        'avg_user_amount': 2000,
        'transaction_frequency': 5,
        'transaction_velocity': 3,
        'device_change': 0,
        'location_change': 0,
        'new_device_flag': 0,
        'account_balance': 75000,
        'distance_from_last_transaction': 5.5
    }
]

for idx, sample in enumerate(test_samples, 1):
    X_test = np.array([[sample[feat] for feat in features_to_use]])
    X_scaled = scaler.transform(X_test)
    pred = model.predict(X_scaled)[0]
    prob = model.predict_proba(X_scaled)[0][1]
    
    status = "⚠️ FRAUD" if pred == 1 else "✓ LEGITIMATE"
    print(f"\n  Transaction {idx}:")
    print(f"    Amount: {format_inr(sample['amount'])} (Avg: {format_inr(sample['avg_user_amount'])})")
    print(f"    Velocity: {sample['transaction_velocity']}, Device Change: {sample['device_change']}")
    print(f"    Prediction: {status} ({prob:.1%} fraud risk)")

print("\n✓ All tests passed! Models are ready for use.")
