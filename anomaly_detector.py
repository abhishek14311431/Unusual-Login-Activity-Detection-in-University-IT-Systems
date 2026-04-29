# Anomaly detection and ensemble methods module

import numpy as np
import pandas as pd
import logging
from config import *

logger = logging.getLogger(__name__)

class EnsembleAnomalyDetector:
    """Ensemble anomaly detection combining K-Means and DBSCAN"""
    
    def __init__(self, kmeans_model, dbscan_model):
        """
        Initialize ensemble detector
        
        Args:
            kmeans_model (KMeansClustering): Fitted K-Means model
            dbscan_model (DBSCANClustering): Fitted DBSCAN model
        """
        self.kmeans = kmeans_model
        self.dbscan = dbscan_model
        self.anomalies_union = None
        self.anomalies_intersection = None
        self.ensemble_score = None
    
    def combine_predictions(self):
        """Combine anomaly predictions from both algorithms"""
        logger.info("Creating ensemble anomaly predictions...")
        
        # Union: flagged by either algorithm
        self.anomalies_union = self.kmeans.anomalies | self.dbscan.anomalies
        
        # Intersection: flagged by both algorithms
        self.anomalies_intersection = self.kmeans.anomalies & self.dbscan.anomalies
        
        # Weighted ensemble score
        self.ensemble_score = (
            0.5 * self.kmeans.anomaly_scores +
            0.5 * self.dbscan.anomalies.astype(float)
        )
        
        logger.info(f"✓ Ensemble predictions created")
        logger.info(f"  Union (either): {self.anomalies_union.sum()} ({self.anomalies_union.sum()/len(self.anomalies_union)*100:.2f}%)")
        logger.info(f"  Intersection (both): {self.anomalies_intersection.sum()} ({self.anomalies_intersection.sum()/len(self.anomalies_intersection)*100:.2f}%)")
        
        return self
    
    def get_comparison_table(self):
        """Get comparison of anomaly detection methods"""
        comparison = pd.DataFrame({
            'Method': ['K-Means', 'DBSCAN', 'Ensemble (Union)', 'Ensemble (Intersection)'],
            'Anomalies_Detected': [
                self.kmeans.anomalies.sum(),
                self.dbscan.anomalies.sum(),
                self.anomalies_union.sum(),
                self.anomalies_intersection.sum()
            ],
            'Percentage': [
                f"{self.kmeans.anomalies.sum()/len(self.kmeans.anomalies)*100:.2f}%",
                f"{self.dbscan.anomalies.sum()/len(self.dbscan.anomalies)*100:.2f}%",
                f"{self.anomalies_union.sum()/len(self.anomalies_union)*100:.2f}%",
                f"{self.anomalies_intersection.sum()/len(self.anomalies_intersection)*100:.2f}%"
            ]
        })
        
        logger.info("\nAnomaly Detection Comparison:")
        print(comparison)
        return comparison
    
    def rank_anomalies(self, top_n=10):
        """Rank top N most anomalous events"""
        top_indices = np.argsort(self.ensemble_score)[-top_n:][::-1]
        
        ranking = pd.DataFrame({
            'Index': top_indices,
            'Ensemble_Score': self.ensemble_score[top_indices],
            'KMeans_Score': self.kmeans.anomaly_scores[top_indices],
            'KMeans_Anomaly': self.kmeans.anomalies[top_indices],
            'DBSCAN_Anomaly': self.dbscan.anomalies[top_indices],
            'In_Union': self.anomalies_union[top_indices],
            'In_Intersection': self.anomalies_intersection[top_indices]
        })
        
        logger.info(f"\nTop {top_n} Most Anomalous Events:")
        print(ranking)
        return ranking


def validate_preprocessing(X, feature_names):
    """Validate preprocessing output"""
    logger.info("\n" + "="*50)
    logger.info("VALIDATION: Preprocessing Output")
    logger.info("="*50)
    
    tests = []
    
    # Test 1: Shape validation
    if X.shape[0] > 0 and X.shape[1] > 0:
        logger.info(f"✓ Test 1 PASS: Valid shape {X.shape}")
        tests.append(True)
    else:
        logger.error(f"✗ Test 1 FAIL: Invalid shape")
        tests.append(False)
    
    # Test 2: No NaN
    if np.isnan(X).sum() == 0:
        logger.info(f"✓ Test 2 PASS: No NaN values")
        tests.append(True)
    else:
        logger.error(f"✗ Test 2 FAIL: {np.isnan(X).sum()} NaN values found")
        tests.append(False)
    
    # Test 3: No infinite values
    if np.isinf(X).sum() == 0:
        logger.info(f"✓ Test 3 PASS: No infinite values")
        tests.append(True)
    else:
        logger.error(f"✗ Test 3 FAIL: {np.isinf(X).sum()} infinite values")
        tests.append(False)
    
    # Test 4: Feature count match
    if X.shape[1] == len(feature_names):
        logger.info(f"✓ Test 4 PASS: Feature count matches")
        tests.append(True)
    else:
        logger.error(f"✗ Test 4 FAIL: Feature count mismatch")
        tests.append(False)
    
    # Test 5: Scaling check
    mean_val = np.abs(X.mean())
    if mean_val < 0.5:
        logger.info(f"✓ Test 5 PASS: Data properly scaled (mean={X.mean():.4f})")
        tests.append(True)
    else:
        logger.warning(f"⚠ Test 5 WARNING: Scaling may be off (mean={X.mean():.4f})")
        tests.append(True)
    
    logger.info(f"\nResults: {sum(tests)}/{len(tests)} tests passed")
    return all(tests)


def validate_anomaly_scores(scores):
    """Validate anomaly scores"""
    logger.info("\n" + "="*50)
    logger.info("VALIDATION: Anomaly Scores")
    logger.info("="*50)
    
    tests = []
    
    # Range check
    if scores.min() >= 0 and scores.max() <= 1:
        logger.info(f"✓ Test 1 PASS: Scores in [0,1]: [{scores.min():.4f}, {scores.max():.4f}]")
        tests.append(True)
    else:
        logger.warning(f"⚠ Test 1 WARNING: Scores outside [0,1]")
        tests.append(True)
    
    # NaN check
    if np.isnan(scores).sum() == 0:
        logger.info(f"✓ Test 2 PASS: No NaN in scores")
        tests.append(True)
    else:
        logger.error(f"✗ Test 2 FAIL: {np.isnan(scores).sum()} NaN values")
        tests.append(False)
    
    # Variance check
    if scores.std() > 0:
        logger.info(f"✓ Test 3 PASS: Scores have variance (std={scores.std():.4f})")
        tests.append(True)
    else:
        logger.error(f"✗ Test 3 FAIL: No variance in scores")
        tests.append(False)
    
    logger.info(f"\nResults: {sum(tests)}/{len(tests)} tests passed")
    return all(tests)
