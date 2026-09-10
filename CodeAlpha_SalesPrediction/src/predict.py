"""
==============================================================================
Module: src/predict.py
Description: Production inference script for Advertising Sales Volume Estimation.
Author: CodeAlpha Internship Project
==============================================================================
Video Walkthrough Highlights:
  1. Loads the serialized model artifact (`models/best_model.joblib`).
  2. Extracts the full `Pipeline` containing `ColumnTransformer` (with `StandardScaler`) and the regressor.
  3. Accepts raw advertising spend budgets in thousands of dollars ($k).
  4. Automatically predicts expected product sales volume in thousands of units.
==============================================================================
"""

from pathlib import Path
import joblib
import pandas as pd


def predict_sales(campaign_budgets: list):
    """
    Predict sales volume for given advertising channel budgets.

    Parameters:
    -----------
    campaign_budgets : list of dicts
        List of dictionaries with keys: 'tv', 'radio', 'newspaper' (in $k).

    Example:
    --------
    >>> predict_sales([{"tv": 230.1, "radio": 37.8, "newspaper": 69.2}])
    """
    model_path = Path(__file__).resolve().parent.parent / "models" / "best_model.joblib"
    if not model_path.exists():
        raise FileNotFoundError(
            f"[ERROR] Serialized model not found at {model_path}. Run `python src/train.py` first."
        )

    artifact = joblib.load(model_path)
    model_name = artifact["model_name"]
    pipeline = artifact["pipeline"]
    feature_names = artifact["feature_names"]

    df_samples = pd.DataFrame(campaign_budgets)[feature_names]
    predictions = pipeline.predict(df_samples)

    print(f"\n[MODEL LOADED]: {model_name}")
    print("=" * 65)
    for idx, (budget, pred) in enumerate(zip(campaign_budgets, predictions)):
        pred_units = max(0.0, pred)
        print(
            f"Campaign {idx+1}: TV: ${budget.get('tv'):,.1f}k | "
            f"Radio: ${budget.get('radio'):,.1f}k | Newspaper: ${budget.get('newspaper'):,.1f}k"
        )
        print(f"            => Estimated Sales: {pred_units:.2f}k Units ({pred_units*1000:,.0f} units)\n")
    print("=" * 65)


if __name__ == "__main__":
    # Test cases representing various marketing mix allocations
    sample_campaigns = [
        {"tv": 230.1, "radio": 37.8, "newspaper": 69.2},  # Expected actual ~22.1k
        {"tv": 44.5, "radio": 39.3, "newspaper": 45.1},   # Expected actual ~10.4k
        {"tv": 17.2, "radio": 45.9, "newspaper": 69.3},   # Expected actual ~9.3k
        {"tv": 280.0, "radio": 40.0, "newspaper": 10.0},  # High TV + Radio mix
    ]

    print("[EXECUTION] Running sample sales predictions with champion model...")
    predict_sales(sample_campaigns)
