# Configuration file for Login Anomaly Detection System

import numpy as np

# Random seed for reproducibility
RANDOM_STATE = 42

# Dataset configuration
DATA_PATH = 'rba-dataset.csv'

# Feature engineering parameters
TIMESTAMP_COLUMNS = ['timestamp', 'time', 'date', 'datetime', 'login_time']
USER_ID_COLUMNS = ['user', 'user_id', 'username', 'account', 'account_id']
IP_COLUMNS = ['source_ip', 'ip', 'ip_address', 'src_ip']
DEVICE_COLUMNS = ['device', 'browser', 'user_agent', 'device_type']
OUTCOME_COLUMNS = ['outcome', 'result', 'status', 'login_result']

# Preprocessing
NUMERIC_SCALER = 'StandardScaler'  # 'StandardScaler' or 'RobustScaler'
CATEGORICAL_ENCODER = 'OneHotEncoder'  # 'OneHotEncoder' or 'OrdinalEncoder'
IMPUTATION_STRATEGY_NUMERIC = 'median'
IMPUTATION_STRATEGY_CATEGORICAL = 'most_frequent'
MAX_CATEGORICAL_CARDINALITY = 100  # Drop high-cardinality features above this

# K-Means parameters
KMEANS_K_RANGE = range(2, 11)
KMEANS_N_INIT = 10
KMEANS_ANOMALY_PERCENTILE = 95  # Top 5% as anomalies

# DBSCAN parameters
DBSCAN_MIN_SAMPLES = None  # Will be auto-calculated as 1% of data
DBSCAN_EPS_PERCENTILE = 95  # Use 95th percentile of k-distance

# PCA parameters
PCA_VARIANCE_EXPLAINED_TARGET = 0.95

# Output configuration
OUTPUT_DIRECTORY = 'anomaly_detection_results'
SAVE_MODELS = True
SAVE_VISUALIZATIONS = True
SAVE_RESULTS_CSV = True

# Logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# Visualization
DPI = 100
FIGURE_SIZE_SINGLE = (10, 6)
FIGURE_SIZE_DUAL = (14, 5)
FIGURE_SIZE_QUAD = (14, 10)

# Pandas display options
PANDAS_MAX_COLUMNS = None
PANDAS_MAX_ROWS = 100
PANDAS_DISPLAY_WIDTH = None

print("✓ Configuration loaded successfully")
