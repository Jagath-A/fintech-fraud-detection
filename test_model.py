#!/usr/bin/env python
"""Test script to diagnose model loading issues"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.helper import model, scaler, MODEL_PATH, SCALER_PATH

print("\n=== Model Loading Diagnostic ===\n")

print(f"Model loaded: {model is not None}")
print(f"Scaler loaded: {scaler is not None}")

print(f"\nModel path: {MODEL_PATH}")
print(f"Model exists: {os.path.exists(MODEL_PATH)}")
if os.path.exists(MODEL_PATH):
    print(f"Model size: {os.path.getsize(MODEL_PATH)} bytes")

print(f"\nScaler path: {SCALER_PATH}")
print(f"Scaler exists: {os.path.exists(SCALER_PATH)}")
if os.path.exists(SCALER_PATH):
    print(f"Scaler size: {os.path.getsize(SCALER_PATH)} bytes")

if model is None:
    print("\n⚠️  WARNING: Model failed to load!")
    print("The fraud_model.pkl file may be:")
    print("  - Corrupted or incomplete")
    print("  - Not a valid Python pickle file")
    print("  - Downloaded incorrectly from Google Drive")

if scaler is None:
    print("\n⚠️  WARNING: Scaler failed to load!")

if model and scaler:
    print("\n✓ Both model and scaler loaded successfully!")
    
    # Test a prediction
    try:
        from utils.helper import predict
        test_data = {"amount": 500, "avg_user_amount": 200}
        pred, risk = predict(test_data)
        print(f"\n✓ Test prediction successful!")
        print(f"  Input: {test_data}")
        print(f"  Prediction: {pred}")
        print(f"  Risk Score: {risk:.2%}")
    except Exception as e:
        print(f"\n✗ Test prediction failed: {e}")
