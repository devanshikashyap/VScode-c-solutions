"""
==============================================================================
Module: src/load_data.py
Description: Data loading, cleaning, and feature engineering for the Advertising Sales dataset.
Author: CodeAlpha Internship Project
==============================================================================
Video Walkthrough Highlights:
  1. Data Ingestion: Loads marketing and advertising spend records from `data/advertising.csv`.
  2. Index Column Sanitization: Automatically identifies and drops unnamed raw index columns.
  3. Standardization: Converts feature column names into clean, lowercase snake_case
     (`tv`, `radio`, `newspaper`, `sales`).
  4. Feature Engineering:
     - Derives `total_spend` ($TV + Radio + Newspaper$) to evaluate overall budget impact.
     - Derives channel budget allocation percentages (`tv_share`, `radio_share`, `newspaper_share`).
==============================================================================
"""

from pathlib import Path
import pandas as pd


def load_sales_dataframe(file_path: str = "data/advertising.csv") -> pd.DataFrame:
    """
    Load advertising sales dataset, clean column names, and engineer aggregate spend features.

    Parameters:
    -----------
    file_path : str, default="data/advertising.csv"
        Path to the CSV dataset file.

    Returns:
    --------
    pd.DataFrame
        Formatted DataFrame containing channel advertising expenditures, derived metrics, and sales.
    """
    # -------------------------------------------------------------------------
    # Step 1: Verify file existence and load dataset
    # -------------------------------------------------------------------------
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"[ERROR] Sales dataset CSV not found at {path.resolve()}")

    df = pd.read_csv(path)

    # -------------------------------------------------------------------------
    # Step 2: Drop unnamed index columns if present
    # -------------------------------------------------------------------------
    unnamed_cols = [c for c in df.columns if "unnamed" in c.lower() or c.strip() == ""]
    if unnamed_cols:
        df.drop(columns=unnamed_cols, inplace=True)

    # -------------------------------------------------------------------------
    # Step 3: Standardize column names to lowercase
    # -------------------------------------------------------------------------
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # -------------------------------------------------------------------------
    # Step 4: Feature Engineering - Total Ad Spend & Channel Proportions
    # -------------------------------------------------------------------------
    if all(col in df.columns for col in ["tv", "radio", "newspaper"]):
        df["total_spend"] = df["tv"] + df["radio"] + df["newspaper"]
        # Calculate percentage contribution of each channel
        df["tv_share"] = (df["tv"] / df["total_spend"]) * 100
        df["radio_share"] = (df["radio"] / df["total_spend"]) * 100
        df["newspaper_share"] = (df["newspaper"] / df["total_spend"]) * 100

    return df


if __name__ == "__main__":
    # Test execution of data loader
    print("[EXECUTION] Loading Advertising Sales dataset...")
    df = load_sales_dataframe()
    print(f"[INFO] Successfully loaded dataset: {df.shape[0]} records x {df.shape[1]} columns.")
    print("\n--- Columns ---")
    print(df.columns.tolist())
    print("\n--- Summary Statistics ---")
    print(df.describe().T.round(2))
    print("\n--- Sample 5 Records ---")
    print(df.head())
