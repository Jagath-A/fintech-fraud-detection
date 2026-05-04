import os
import joblib
import pandas as pd
import requests

MODEL_URL = "https://drive.google.com/uc?id=1wrIDqdhWv-dknioFARl6p1wG5Jpjjnvr"
SCALER_URL = "https://drive.google.com/uc?id=171YO0-wl0SWQzeh1atrf8o5a_OFpZKte"

# Get absolute paths relative to this script location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "fraud_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "model", "scaler.pkl")

# Global variables for model and scaler
model = None
scaler = None


def download_file(url, path, timeout=30):
    """
    Download a file from URL if it doesn't exist locally.
    
    Args:
        url: File URL to download from
        path: Local path to save the file
        timeout: Request timeout in seconds
        
    Returns:
        bool: True if file exists (either already existed or was downloaded), False if download failed
    """
    if os.path.exists(path):
        # Verify file is not empty
        file_size = os.path.getsize(path)
        if file_size > 100:  # Pickle files should be at least 100 bytes
            print(f"OK: File already exists: {os.path.basename(path)} ({file_size} bytes)")
            return True
        else:
            print(f"Warning: File exists but is too small ({file_size} bytes). Removing and re-downloading...")
            os.remove(path)
    
    # File doesn't exist, try to download it
    try:
        print(f"Downloading {os.path.basename(path)}...")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        response = requests.get(url, timeout=timeout, stream=True, allow_redirects=True)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Get total file size from headers
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        
        # Write file in chunks
        with open(path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
        
        # Verify downloaded file
        final_size = os.path.getsize(path)
        
        if final_size > 100:  # Pickle files should be at least 100 bytes
            print(f"OK: Successfully downloaded: {os.path.basename(path)} ({final_size} bytes)")
            return True
        else:
            print(f"Error: Downloaded file is too small ({final_size} bytes): {os.path.basename(path)}")
            os.remove(path)
            return False
            
    except requests.exceptions.Timeout:
        print(f"Error: Download timeout for {os.path.basename(path)}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error: Download error for {os.path.basename(path)}: {str(e)}")
        return False
    except IOError as e:
        print(f"Error: File write error: {str(e)}")
        return False


def load_models():
    """
    Load model and scaler from disk. Download if necessary.
    Returns tuple of (model, scaler) or (None, None) if loading fails.
    """
    global model, scaler
    
    try:
        # Download files if missing
        model_ok = download_file(MODEL_URL, MODEL_PATH)
        scaler_ok = download_file(SCALER_URL, SCALER_PATH)
        
        if not model_ok or not scaler_ok:
            print("Error: Failed to obtain required model files")
            return None, None
        
        # Try to load the models with better error diagnostics
        model = None
        scaler = None
        
        try:
            print(f"Loading model from {os.path.basename(MODEL_PATH)}...")
            model_file_size = os.path.getsize(MODEL_PATH)
            print(f"  File size: {model_file_size} bytes")
            
            model = joblib.load(MODEL_PATH)
            print("OK: Model loaded successfully")
        except EOFError as e:
            print("Error: Failed to load model: File appears corrupted (EOFError)")
            print(f"  The downloaded file may be incomplete. Removing and retrying...")
            if os.path.exists(MODEL_PATH):
                os.remove(MODEL_PATH)
            model = None
        except Exception as e:
            print(f"Error: Failed to load model: {type(e).__name__}: {str(e)}")
            print(f"  File location: {MODEL_PATH}")
            print(f"  File exists: {os.path.exists(MODEL_PATH)}")
            if os.path.exists(MODEL_PATH):
                print(f"  File size: {os.path.getsize(MODEL_PATH)} bytes")
            model = None
        
        try:
            print(f"Loading scaler from {os.path.basename(SCALER_PATH)}...")
            scaler_file_size = os.path.getsize(SCALER_PATH)
            print(f"  File size: {scaler_file_size} bytes")
            
            scaler = joblib.load(SCALER_PATH)
            print("OK: Scaler loaded successfully")
        except EOFError as e:
            print("Error: Failed to load scaler: File appears corrupted (EOFError)")
            print(f"  The downloaded file may be incomplete. Removing and retrying...")
            if os.path.exists(SCALER_PATH):
                os.remove(SCALER_PATH)
            scaler = None
        except Exception as e:
            print(f"Error: Failed to load scaler: {type(e).__name__}: {str(e)}")
            scaler = None
        
        # If model failed to load, try downloading again
        if model is None:
            print("\nAttempting to re-download the model...")
            if os.path.exists(MODEL_PATH):
                os.remove(MODEL_PATH)
            
            model_ok = download_file(MODEL_URL, MODEL_PATH)
            if model_ok:
                try:
                    print("Retrying model load...")
                    model = joblib.load(MODEL_PATH)
                    print("OK: Model loaded successfully on retry")
                except Exception as e:
                    print(f"Error: Still unable to load model: {type(e).__name__}: {str(e)}")
        
        return model, scaler
        
    except Exception as e:
        print(f"Error: Unexpected error during model loading: {type(e).__name__}: {str(e)}")
        return None, None


# Initialize models on import
model, scaler = load_models()


def preprocess_input(data):
    """Preprocess input data to match the model's expected features."""
    df = pd.DataFrame([data])
    
    # Expected features from the trained model
    required_features = [
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
    
    # Check that all required columns exist
    missing = [f for f in required_features if f not in df.columns]
    if missing:
        raise ValueError(f"Input data must contain: {', '.join(required_features)}")
    
    return df[required_features]


def predict(data):
    """Make a fraud prediction on input data.
    
    Args:
        data: dict with keys: amount, avg_user_amount, transaction_frequency,
              transaction_velocity, device_change, location_change, new_device_flag,
              account_balance, distance_from_last_transaction
    
    Returns:
        tuple: (prediction: 0 or 1, fraud_probability: float 0-1)
    """
    if model is None or scaler is None:
        raise RuntimeError("Model or scaler failed to load. Check that model files exist and are valid.")
    
    try:
        df = preprocess_input(data)
        scaled = scaler.transform(df)
        pred = model.predict(scaled)[0]
        prob = model.predict_proba(scaled)[0][1]
        return pred, prob
    except Exception as e:
        raise ValueError(f"Prediction failed: {str(e)}")


def save_alert(data, prediction, risk):
    """Save a transaction alert to the alerts CSV file."""
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Read existing alerts
    if os.path.exists("data/alerts.csv"):
        df = pd.read_csv("data/alerts.csv")
    else:
        df = pd.DataFrame()

    new_entry = {
        "transaction_id": data.get("transaction_id", ""),
        "amount": data["amount"],
        "avg_user_amount": data["avg_user_amount"],
        "transaction_frequency": data["transaction_frequency"],
        "transaction_velocity": data["transaction_velocity"],
        "device_change": data["device_change"],
        "location_change": data["location_change"],
        "new_device_flag": data["new_device_flag"],
        "account_balance": data["account_balance"],
        "distance_from_last_transaction": data["distance_from_last_transaction"],
        "prediction": prediction,
        "risk": risk,
        "time": pd.Timestamp.now()
    }

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv("data/alerts.csv", index=False)
