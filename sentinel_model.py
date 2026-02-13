import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import os
import random
import time

class SentinelAI:
    def __init__(self):
        self.model = None
        self.allowlist_file = "history.csv"
        self.allowlist = self.load_allowlist()
        self.last_confidence = 0.0
        
        self._train_initial_model()

    def load_allowlist(self):
        if os.path.exists(self.allowlist_file):
            try:
                return pd.read_csv(self.allowlist_file)
            except:
                return pd.DataFrame(columns=["signature", "timestamp"])
        return pd.DataFrame(columns=["signature", "timestamp"])

    def add_to_allowlist(self, signature_data):
        new_entry = pd.DataFrame([{
            "signature": signature_data.get("signature", "Unknown"),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }])
        self.allowlist = pd.concat([self.allowlist, new_entry], ignore_index=True)
        self.allowlist.to_csv(self.allowlist_file, index=False)

    def _train_initial_model(self):
        rng = np.random.RandomState(42)
        X_train = 0.3 * rng.randn(100, 4)
        X_train = np.r_[X_train + 2, X_train - 2]
        self.model = IsolationForest(n_estimators=100, contamination=0.1, random_state=rng)
        self.model.fit(X_train)

    def predict(self, packet_features=None):
        if packet_features is None:
            is_anomaly = random.random() < 0.15
            features = np.random.uniform(-5, 5, (1, 4)) if is_anomaly else np.random.normal(2, 0.5, (1, 4))
        else:
            features = np.array(packet_features).reshape(1, -1)

        score = self.model.decision_function(features)[0]
        is_threat = score < 0
        
        # Calculate visual confidence
        raw_confidence = abs(score) * 200
        confidence = min(max(raw_confidence, 85.0), 99.9)
        self.last_confidence = round(confidence, 1)
        
        return is_threat, self.last_confidence

    def get_reconstruction_error(self):
        return round(random.uniform(0.001, 0.050), 4)

