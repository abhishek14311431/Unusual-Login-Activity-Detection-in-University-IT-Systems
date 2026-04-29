# Clustering module for K-Means and DBSCAN

import numpy as np
import logging
from sklearn.cluster import KMeans, DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import silhouette_score, davies_bouldin_score
from config import *

logger = logging.getLogger(__name__)

class KMeansClustering:
    """K-Means clustering with anomaly detection"""
    
    def __init__(self, k_range=KMEANS_K_RANGE, random_state=RANDOM_STATE):
        self.k_range = k_range
        self.random_state = random_state
        self.model = None
        self.labels = None
        self.silhouette = None
        self.davies_bouldin = None
        self.anomaly_scores = None
        self.anomalies = None
        self.optimal_k = None
        
    def find_optimal_k(self, X):
        """Find optimal K using elbow and silhouette score"""
        logger.info("Finding optimal K for K-Means...")
        
        inertias = []
        silhouette_scores = []
        
        for k in self.k_range:
            kmeans_temp = KMeans(n_clusters=k, random_state=self.random_state, n_init=KMEANS_N_INIT)
            labels_temp = kmeans_temp.fit_predict(X)
            inertias.append(kmeans_temp.inertia_)
            silhouette_scores.append(silhouette_score(X, labels_temp))
            logger.info(f"  K={k}: Inertia={kmeans_temp.inertia_:.2f}, Silhouette={silhouette_scores[-1]:.4f}")
        
        self.optimal_k = list(self.k_range)[np.argmax(silhouette_scores)]
        best_silhouette = max(silhouette_scores)
        logger.info(f"✓ Optimal K: {self.optimal_k} (Silhouette: {best_silhouette:.4f})")
        
        return self.optimal_k, inertias, silhouette_scores
    
    def fit(self, X):
        """Fit K-Means with optimal K"""
        if self.optimal_k is None:
            self.find_optimal_k(X)
        
        logger.info(f"Fitting K-Means with K={self.optimal_k}...")
        self.model = KMeans(n_clusters=self.optimal_k, random_state=self.random_state, n_init=KMEANS_N_INIT)
        self.labels = self.model.fit_predict(X)
        
        self.silhouette = silhouette_score(X, self.labels)
        self.davies_bouldin = davies_bouldin_score(X, self.labels)
        
        logger.info(f"✓ K-Means fitted")
        logger.info(f"  Silhouette Score: {self.silhouette:.4f}")
        logger.info(f"  Davies-Bouldin Index: {self.davies_bouldin:.4f}")
        
        return self
    
    def compute_anomaly_scores(self, X):
        """Compute anomaly scores based on distance to centroid"""
        logger.info("Computing K-Means anomaly scores...")
        
        distances = np.linalg.norm(X - self.model.cluster_centers_[self.labels], axis=1)
        self.anomaly_scores = (distances - distances.min()) / (distances.max() - distances.min())
        
        threshold = np.percentile(self.anomaly_scores, KMEANS_ANOMALY_PERCENTILE)
        self.anomalies = self.anomaly_scores >= threshold
        
        logger.info(f"✓ Anomaly scores computed")
        logger.info(f"  Anomalies detected: {self.anomalies.sum()} ({self.anomalies.sum()/len(self.anomalies)*100:.2f}%)")
        
        return self.anomaly_scores, self.anomalies


class DBSCANClustering:
    """DBSCAN clustering with anomaly detection"""
    
    def __init__(self, eps_percentile=DBSCAN_EPS_PERCENTILE, min_samples=DBSCAN_MIN_SAMPLES):
        self.eps_percentile = eps_percentile
        self.min_samples = min_samples
        self.model = None
        self.labels = None
        self.anomalies = None
        self.eps = None
        
    def select_eps(self, X):
        """Select eps using k-distance graph"""
        logger.info("Computing k-distance graph for eps selection...")
        
        if self.min_samples is None:
            self.min_samples = max(5, int(X.shape[0] * 0.01))
        
        neighbors = NearestNeighbors(n_neighbors=self.min_samples)
        neighbors.fit(X)
        distances, _ = neighbors.kneighbors(X)
        distances = np.sort(distances[:, self.min_samples - 1], axis=0)
        
        self.eps = np.percentile(distances, self.eps_percentile)
        
        logger.info(f"✓ Eps selected: {self.eps:.4f} (percentile={self.eps_percentile})")
        logger.info(f"  Min samples: {self.min_samples}")
        
        return self.eps, distances
    
    def fit(self, X):
        """Fit DBSCAN"""
        if self.eps is None:
            self.select_eps(X)
        
        logger.info(f"Fitting DBSCAN with eps={self.eps:.4f}...")
        self.model = DBSCAN(eps=self.eps, min_samples=self.min_samples)
        self.labels = self.model.fit_predict(X)
        
        n_clusters = len(set(self.labels)) - (1 if -1 in self.labels else 0)
        n_outliers = (self.labels == -1).sum()
        
        self.anomalies = self.labels == -1
        
        logger.info(f"✓ DBSCAN fitted")
        logger.info(f"  Clusters: {n_clusters}")
        logger.info(f"  Anomalies (outliers): {n_outliers} ({n_outliers/len(self.labels)*100:.2f}%)")
        
        return self
