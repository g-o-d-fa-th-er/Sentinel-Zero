import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.metrics import pairwise_distances_argmin_min

class ThreatDetector:
    def __init__(self, n_clusters=8, contamination=0.05, random_state=42):
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        self.iso_forest = IsolationForest(contamination=contamination, random_state=random_state, n_jobs=-1)
        self.kmeans_threshold = 0.0
        self.training_data = None

    def train(self, X):
        """
        Trains K-Means and Isolation Forest.
        """
        print("[*] Training Ensemble Models (K-Means + Isolation Forest)...")
        self.training_data = X.copy() if hasattr(X, 'copy') else X
        
        # Train K-Means
        self.kmeans.fit(X)
        closest, distances = pairwise_distances_argmin_min(X, self.kmeans.cluster_centers_)
        self.kmeans_threshold = np.percentile(distances, 95)
        # print(f"    > K-Means Threshold: {self.kmeans_threshold:.4f}")

        # Train Isolation Forest
        self.iso_forest.fit(X)
        print("[+] Models trained successfully.")

    def predict(self, packet):
        """
        Predicts if a packet is a threat.
        Returns: (anomaly_score, is_threat_boolean)
        """
        if len(packet.shape) == 1:
            packet = packet.reshape(1, -1)

        # 1. K-Means
        closest, distances = pairwise_distances_argmin_min(packet, self.kmeans.cluster_centers_)
        kmeans_dist = distances[0]
        kmeans_anomaly = kmeans_dist > self.kmeans_threshold

        # 2. Isolation Forest
        iso_pred = self.iso_forest.predict(packet)[0]
        iso_anomaly = iso_pred == -1

        # 3. Voting (AND Logic)
        is_threat = kmeans_anomaly and iso_anomaly
        
        # Calculate a synthetic "Anomaly Score" for visualization (0-100)
        # Normalize distance based on threshold
        score = min(100, (kmeans_dist / self.kmeans_threshold) * 50)
        if iso_anomaly:
            score += 50
        score = min(100, score)

        return score, is_threat

    def update_knowledge(self, packet):
        """
        Adaptive Learning: Adds packet to training set and retrains.
        """
        if len(packet.shape) == 1:
            packet = packet.reshape(1, -1)
            
        if isinstance(self.training_data, np.ndarray):
            self.training_data = np.vstack([self.training_data, packet])
        else:
            import pandas as pd
            packet_df = pd.DataFrame(packet, columns=self.training_data.columns)
            self.training_data = pd.concat([self.training_data, packet_df], ignore_index=True)

        self.train(self.training_data)
