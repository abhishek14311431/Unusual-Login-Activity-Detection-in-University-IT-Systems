# Utility functions for visualization and results management

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import joblib
from config import *

logger = logging.getLogger(__name__)

def create_output_directory():
    """Create output directory for results"""
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIRECTORY, 'models'), exist_ok=True)
    logger.info(f"✓ Output directory created: {OUTPUT_DIRECTORY}")
    return OUTPUT_DIRECTORY


def save_models(preprocessor, pca, kmeans, dbscan, output_dir=OUTPUT_DIRECTORY):
    """Save trained models"""
    models_dir = os.path.join(output_dir, 'models')
    
    joblib.dump(preprocessor, os.path.join(models_dir, 'preprocessor.pkl'))
    joblib.dump(pca, os.path.join(models_dir, 'pca.pkl'))
    joblib.dump(kmeans.model, os.path.join(models_dir, 'kmeans_model.pkl'))
    joblib.dump(dbscan.model, os.path.join(models_dir, 'dbscan_model.pkl'))
    
    logger.info("✓ Models saved:")
    logger.info(f"  - preprocessor.pkl")
    logger.info(f"  - pca.pkl")
    logger.info(f"  - kmeans_model.pkl")
    logger.info(f"  - dbscan_model.pkl")


def save_results(results_df, output_dir=OUTPUT_DIRECTORY):
    """Save anomaly detection results to CSV"""
    csv_path = os.path.join(output_dir, 'anomaly_detection_results.csv')
    results_df.to_csv(csv_path, index=False)
    logger.info(f"✓ Results saved: {csv_path}")


def save_config(config_dict, output_dir=OUTPUT_DIRECTORY):
    """Save configuration and metadata"""
    config_path = os.path.join(output_dir, 'config.json')
    with open(config_path, 'w') as f:
        json.dump(config_dict, f, indent=2)
    logger.info(f"✓ Configuration saved: {config_path}")


def save_figure(fig, filename, output_dir=OUTPUT_DIRECTORY):
    """Save matplotlib figure"""
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=DPI, bbox_inches='tight')
    logger.info(f"✓ Figure saved: {filename}")


def plot_pca_variance(pca, output_dir=OUTPUT_DIRECTORY):
    """Plot PCA variance explained"""
    cumsum_var = np.cumsum(pca.explained_variance_ratio_)
    
    fig, axes = plt.subplots(1, 2, figsize=FIGURE_SIZE_DUAL)
    
    axes[0].bar(range(1, min(21, len(pca.explained_variance_ratio_) + 1)), 
                pca.explained_variance_ratio_[:20])
    axes[0].set_xlabel('Principal Component')
    axes[0].set_ylabel('Explained Variance Ratio')
    axes[0].set_title('PCA Scree Plot')
    axes[0].grid(True, alpha=0.3)
    
    axes[1].plot(range(1, min(21, len(cumsum_var) + 1)), cumsum_var[:20], marker='o')
    axes[1].axhline(y=0.95, color='r', linestyle='--', label='95% variance')
    axes[1].set_xlabel('Number of Components')
    axes[1].set_ylabel('Cumulative Explained Variance')
    axes[1].set_title('Cumulative Variance')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    save_figure(fig, 'pca_variance_explained.png', output_dir)
    plt.close(fig)


def plot_kmeans_selection(inertias, silhouette_scores, k_range, output_dir=OUTPUT_DIRECTORY):
    """Plot K-Means selection metrics"""
    fig, axes = plt.subplots(1, 2, figsize=FIGURE_SIZE_DUAL)
    
    axes[0].plot(k_range, inertias, 'bo-', linewidth=2, markersize=8)
    axes[0].set_xlabel('Number of Clusters (K)')
    axes[0].set_ylabel('Inertia')
    axes[0].set_title('Elbow Method')
    axes[0].grid(True, alpha=0.3)
    
    axes[1].plot(k_range, silhouette_scores, 'ro-', linewidth=2, markersize=8)
    axes[1].set_xlabel('Number of Clusters (K)')
    axes[1].set_ylabel('Silhouette Score')
    axes[1].set_title('Silhouette Score by K')
    axes[1].grid(True, alpha=0.3)
    
    save_figure(fig, 'kmeans_selection.png', output_dir)
    plt.close(fig)


def plot_ensemble_comparison(X_pca_2d, kmeans_anomalies, dbscan_anomalies, 
                            ensemble_union, ensemble_intersection, output_dir=OUTPUT_DIRECTORY):
    """Plot ensemble anomaly detection comparison"""
    fig, axes = plt.subplots(2, 2, figsize=FIGURE_SIZE_QUAD)
    
    plots = [
        (kmeans_anomalies, f'K-Means: {kmeans_anomalies.sum()}'),
        (dbscan_anomalies, f'DBSCAN: {dbscan_anomalies.sum()}'),
        (ensemble_union, f'Union: {ensemble_union.sum()}'),
        (ensemble_intersection, f'Intersection: {ensemble_intersection.sum()}')
    ]
    
    for ax, (anomalies, title) in zip(axes.flat, plots):
        ax.scatter(X_pca_2d[:, 0], X_pca_2d[:, 1], c=anomalies, 
                  cmap='RdYlGn_r', s=30, alpha=0.6, edgecolors='black', linewidth=0.5)
        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
    
    save_figure(fig, 'ensemble_comparison.png', output_dir)
    plt.close(fig)


def create_summary_report(df_original, X_preprocessed, kmeans, dbscan, 
                         ensemble, output_dir=OUTPUT_DIRECTORY):
    """Create and save summary report"""
    report = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║        UNSUPERVISED LOGIN ANOMALY DETECTION - SUMMARY REPORT               ║
╚════════════════════════════════════════════════════════════════════════════╝

📊 DATASET INFORMATION
──────────────────────────────────────────────────────────────────────────────
  Original Shape:          {df_original.shape}
  After Preprocessing:     {X_preprocessed.shape}
  Features Used:           {X_preprocessed.shape[1]}

📈 K-MEANS CLUSTERING RESULTS
──────────────────────────────────────────────────────────────────────────────
  Optimal K:               {kmeans.optimal_k}
  Silhouette Score:        {kmeans.silhouette:.4f} (range: [-1, 1], higher is better)
  Davies-Bouldin Index:    {kmeans.davies_bouldin:.4f} (lower is better)
  Anomalies Detected:      {kmeans.anomalies.sum()} ({kmeans.anomalies.sum()/len(kmeans.anomalies)*100:.2f}%)

🔍 DBSCAN CLUSTERING RESULTS
──────────────────────────────────────────────────────────────────────────────
  Eps Parameter:           {dbscan.eps:.4f}
  Min Samples:             {dbscan.min_samples}
  Anomalies (Outliers):    {dbscan.anomalies.sum()} ({dbscan.anomalies.sum()/len(dbscan.anomalies)*100:.2f}%)

🎯 ENSEMBLE RESULTS
──────────────────────────────────────────────────────────────────────────────
  Union (Either):          {ensemble.anomalies_union.sum()} ({ensemble.anomalies_union.sum()/len(ensemble.anomalies_union)*100:.2f}%)
  Intersection (Both):     {ensemble.anomalies_intersection.sum()} ({ensemble.anomalies_intersection.sum()/len(ensemble.anomalies_intersection)*100:.2f}%)

💾 OUTPUT FILES
──────────────────────────────────────────────────────────────────────────────
  Models:      {os.path.join(output_dir, 'models')}
  Results:     {os.path.join(output_dir, 'anomaly_detection_results.csv')}
  Figures:     {os.path.join(output_dir, '*.png')}
  Config:      {os.path.join(output_dir, 'config.json')}

═════════════════════════════════════════════════════════════════════════════
"""
    
    report_path = os.path.join(output_dir, 'SUMMARY_REPORT.txt')
    with open(report_path, 'w') as f:
        f.write(report)
    
    logger.info(report)
    logger.info(f"✓ Summary report saved: {report_path}")
