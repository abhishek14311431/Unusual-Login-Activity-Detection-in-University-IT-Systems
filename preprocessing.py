import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


DATA_PATH = Path("rba-dataset.csv")


def load_rba_dataset(csv_path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the RBA dataset from CSV."""
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found at {csv_path}")
    return pd.read_csv(csv_path, low_memory=False)


def summarize_dataset(df: pd.DataFrame) -> None:
    """Print requested dataset summary for quick inspection."""
    print("\nFirst 5 rows:")
    print(df.head(5))

    print("\nShape:")
    print(df.shape)

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing value count per column:")
    print(df.isna().sum())

    print("\nBasic statistics (describe):")
    print(df.describe(include="all").transpose())


def plot_login_success_failure(df: pd.DataFrame, output_path: Path = Path("login_success_vs_failure.png")) -> None:
    """Plot and save bar chart for login success vs failure counts."""
    if "Login Successful" not in df.columns:
        raise KeyError("Expected column 'Login Successful' not found in dataset")

    counts = df["Login Successful"].fillna(False).value_counts()
    counts = counts.rename(index={True: "Success", False: "Failure"})

    plt.figure(figsize=(7, 4))
    bars = plt.bar(counts.index.astype(str), counts.values, color=["#2ca02c", "#d62728"])
    plt.title("Login Success vs Failure")
    plt.xlabel("Login Outcome")
    plt.ylabel("Count")
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f"{int(height)}", ha="center", va="bottom")
    plt.tight_layout()
    plt.savefig(output_path, dpi=120)
    plt.show()


def build_scaled_features(df: pd.DataFrame):
    """
    Build feature matrix for clustering from rba-dataset.csv.

    Steps implemented exactly as requested:
    1. Drop non-useful columns for clustering.
    2. Extract hour_of_day and day_of_week from timestamp.
    3. Create is_night_login.
    4. Label-encode categorical columns.
    5. Fill missing values (median for numeric, mode for categorical).
    6. Standard-scale numerical features.
    7. Save cleaned and scaled dataframe as X_scaled.
    """
    work = df.copy()

    if "Login Timestamp" not in work.columns:
        raise KeyError("Expected column 'Login Timestamp' not found in dataset")

    # Convert timestamp first.
    work["Login Timestamp"] = pd.to_datetime(work["Login Timestamp"], errors="coerce")

    # Drop columns not useful for clustering (identifiers and raw free-text fields).
    drop_cols = [
        "index",
        "User ID",
        "IP Address",
        "User Agent String",
        "Region",
        "City",
        "Login Timestamp",
    ]
    existing_drop_cols = [c for c in drop_cols if c in work.columns]

    # Time-derived features from timestamp.
    work["hour_of_day"] = pd.to_datetime(df["Login Timestamp"], errors="coerce").dt.hour
    work["day_of_week"] = pd.to_datetime(df["Login Timestamp"], errors="coerce").dt.dayofweek
    work["is_night_login"] = work["hour_of_day"].between(0, 6, inclusive="both").astype(int)

    # Remove target-like and evaluation columns from clustering features.
    for maybe_label in ["Login Successful", "Is Attack IP", "Is Account Takeover"]:
        if maybe_label in work.columns:
            existing_drop_cols.append(maybe_label)

    work = work.drop(columns=existing_drop_cols)

    categorical_cols = work.select_dtypes(include=["object", "category", "bool", "string", "str"]).columns.tolist()
    numeric_cols = work.select_dtypes(include=[np.number]).columns.tolist()

    # Fill missing values.
    for col in numeric_cols:
        work[col] = work[col].fillna(work[col].median())

    for col in categorical_cols:
        mode_val = work[col].mode(dropna=True)
        fill_val = mode_val.iloc[0] if not mode_val.empty else "unknown"
        work[col] = work[col].fillna(fill_val)

    # Label encode categorical columns.
    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        work[col] = le.fit_transform(work[col].astype(str))
        label_encoders[col] = le

    # Normalize all numerical features using StandardScaler.
    all_numeric_cols = work.select_dtypes(include=[np.number]).columns.tolist()
    scaler = StandardScaler()
    work[all_numeric_cols] = scaler.fit_transform(work[all_numeric_cols])

    # Required output artifact for clustering.
    X_scaled = work.copy()

    logger.info("Preprocessing complete")
    logger.info("X_scaled shape: %s", X_scaled.shape)
    return X_scaled, label_encoders, scaler


def run_pipeline(csv_path: Path = DATA_PATH):
    """End-to-end utility to load, summarize, plot, and produce X_scaled."""
    df = load_rba_dataset(csv_path)
    summarize_dataset(df)
    plot_login_success_failure(df)
    X_scaled, label_encoders, scaler = build_scaled_features(df)
    return df, X_scaled, label_encoders, scaler


if __name__ == "__main__":
    df, X_scaled, label_encoders, scaler = run_pipeline(DATA_PATH)
    output_pickle = Path("X_scaled.pkl")
    X_scaled.to_pickle(output_pickle)
    print(f"\nSaved scaled features to: {output_pickle}")
    print("\nX_scaled preview:")
    print(X_scaled.head())
