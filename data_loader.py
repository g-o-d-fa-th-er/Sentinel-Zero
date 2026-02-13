import pandas as pd
import numpy as np
import os
import requests
import sys
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# Constants
DATA_DIR = "data"
TRAIN_URL = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain+.txt"
TEST_URL = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest+.txt"
TRAIN_FILE = os.path.join(DATA_DIR, "KDDTrain+.txt")
TEST_FILE = os.path.join(DATA_DIR, "KDDTest+.txt")

# Column names for NSL-KDD
COLUMNS = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins",
    "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root",
    "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds",
    "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate",
    "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate",
    "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label", "difficulty"
]

def download_file(url, filepath):
    """Downloads a file with progress indication."""
    if os.path.exists(filepath):
        print(f"[*] File already exists: {filepath}")
        return

    print(f"[*] Downloading {url}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"[+] Download complete: {filepath}")
    except Exception as e:
        print(f"[!] Error downloading {url}: {e}")
        sys.exit(1)

def get_data():
    """
    Orchestrates download, loading, and preprocessing.
    Returns: X_train, X_test, y_train, y_test
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    download_file(TRAIN_URL, TRAIN_FILE)
    download_file(TEST_URL, TEST_FILE)

    print("[*] Loading datasets...")
    df_train = pd.read_csv(TRAIN_FILE, names=COLUMNS)
    df_test = pd.read_csv(TEST_FILE, names=COLUMNS)

    # Drop 'difficulty'
    df_train.drop(columns=['difficulty'], inplace=True)
    df_test.drop(columns=['difficulty'], inplace=True)

    # Separate X and y
    X_train = df_train.drop(columns=['label'])
    y_train = df_train['label'].apply(lambda x: 0 if x == 'normal' else 1)
    
    X_test = df_test.drop(columns=['label'])
    y_test = df_test['label'].apply(lambda x: 0 if x == 'normal' else 1)

    # Preprocessing
    print("[*] Preprocessing data (Encoding & Scaling)...")
    categorical_cols = ['protocol_type', 'service', 'flag']
    numerical_cols = [col for col in X_train.columns if col not in categorical_cols]

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', MinMaxScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols)
        ]
    )

    # Fit on Train, Transform Train & Test
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    # Convert back to DataFrame for easier handling
    feature_names = numerical_cols + list(preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_cols))
    
    X_train_df = pd.DataFrame(X_train_processed, columns=feature_names)
    X_test_df = pd.DataFrame(X_test_processed, columns=feature_names)

    print(f"[+] Data loaded. Train shape: {X_train_df.shape}, Test shape: {X_test_df.shape}")
    return X_train_df, X_test_df, y_train, y_test

if __name__ == "__main__":
    get_data()
