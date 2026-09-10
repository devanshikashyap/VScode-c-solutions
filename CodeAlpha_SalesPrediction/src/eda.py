"""
==============================================================================
Module: src/eda.py
Description: Comprehensive Exploratory Data Analysis (EDA) for Advertising Sales dataset.
Author: CodeAlpha Internship Project
==============================================================================
Video Walkthrough Highlights:
  1. Data Quality & Completeness: Validates dimensions (200 rows, 4 core features)
     and confirms 0 missing values.
  2. Summary Statistics: Analyzes mean, variance, min, median, and IQR across all ad mediums.
  3. Target Analysis (Sales Distribution): Normal distribution with mild right skew;
     mean sales = 14.02k units.
  4. Correlation Heatmap: Highlights that TV advertising has the strongest linear correlation
     with Sales (r = 0.78), followed by Radio (r = 0.58), while Newspaper shows weak correlation (r = 0.23).
  5. Scatter Plots with Trendlines: Illustrates linear and non-linear relationships
     between each marketing channel budget and resultant product sales.
  6. Pairplots & Budget Breakdown: Visualizes channel spend allocation and multi-channel dynamics.
  7. Automated Export: Saves all publication-ready visual figures to `results/`.
==============================================================================
"""

import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Ensure project root is in python path
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.load_data import load_sales_dataframe


def set_plotting_style():
    """Apply modern aesthetic Seaborn and Matplotlib theme styling."""
    sns.set_theme(style="whitegrid", palette="deep")
    plt.rcParams.update({
        "font.sans-serif": "Arial",
        "font.family": "sans-serif",
        "figure.titlesize": 15,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "figure.autolayout": False,
    })


def perform_eda(df: pd.DataFrame, output_dir: str = "results"):
    """
    Execute complete EDA pipeline and export visual plots.

    Parameters:
    -----------
    df : pd.DataFrame
        Formatted advertising sales DataFrame.
    output_dir : str, default="results"
        Directory where visualization images and text reports are saved.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    set_plotting_style()

    core_channels = ["tv", "radio", "newspaper"]
    all_numeric = ["tv", "radio", "newspaper", "total_spend", "sales"]

    # =========================================================================
    # STEP 1: Statistical Summary & Data Integrity Profiling
    # =========================================================================
    print("=" * 65)
    print("            SALES PREDICTION - EXPLORATORY DATA ANALYSIS           ")
    print("=" * 65)

    # 1.1 Dataset Shape
    shape = df.shape
    print(f"\n1. Dataset Dimensions: {shape[0]} records x {shape[1]} columns")

    # 1.2 Data Types & Null Values
    dtypes_df = df.dtypes.reset_index()
    dtypes_df.columns = ["Column Name", "Data Type"]
    missing_df = df.isnull().sum().reset_index()
    missing_df.columns = ["Column Name", "Missing Count"]
    profile_df = pd.merge(dtypes_df, missing_df, on="Column Name")
    profile_df["Missing (%)"] = (profile_df["Missing Count"] / len(df)) * 100
    print("\n2. Data Schema & Integrity Check:")
    print(profile_df.to_string(index=False))

    # 1.3 Summary Statistics
    desc_stats = df[all_numeric].describe().T
    print("\n3. Descriptive Statistics:")
    print(desc_stats.round(2).to_string())

    # Save summary report to text file
    summary_file = out_path / "eda_summary.txt"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("=" * 65 + "\n")
        f.write("            SALES PREDICTION - EXPLORATORY DATA ANALYSIS REPORT    \n")
        f.write("=" * 65 + "\n\n")
        f.write(f"1. Dataset Shape: {shape[0]} records x {shape[1]} columns\n\n")
        f.write("2. Data Profile & Missing Values:\n" + profile_df.to_string(index=False) + "\n\n")
        f.write("3. Numerical Descriptive Statistics:\n" + desc_stats.round(2).to_string() + "\n\n")
        f.write("4. Channel Spend Summary (Totals & Averages):\n")
        for ch in core_channels:
            f.write(f"   - {ch.upper()}: Total Spend = ${df[ch].sum():,.2f}k | Mean = ${df[ch].mean():.2f}k\n")
        f.write(f"   - SALES: Total Units = {df['sales'].sum():,.1f}k | Mean = {df['sales'].mean():.2f}k units\n")
    print(f"\n[SAVED] Text summary report saved to: {summary_file.resolve()}")

    # =========================================================================
    # STEP 2: Distribution of Target Variable (Sales)
    # =========================================================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 2.1 Sales Histogram + KDE
    sns.histplot(df["sales"], kde=True, color="#1f77b4", ax=axes[0], bins=20)
    mean_sales = df["sales"].mean()
    median_sales = df["sales"].median()
    axes[0].axvline(mean_sales, color="red", linestyle="--", label=f"Mean: {mean_sales:.2f}k units")
    axes[0].axvline(median_sales, color="green", linestyle="-", label=f"Median: {median_sales:.2f}k units")
    axes[0].set_title("Sales Distribution (Histogram + KDE)", fontsize=13, weight="bold")
    axes[0].set_xlabel("Sales (Thousands of Units)", fontsize=11)
    axes[0].set_ylabel("Frequency", fontsize=11)
    axes[0].legend(frameon=True)

    # 2.2 Sales Boxplot
    sns.boxplot(x=df["sales"], color="#aec7e8", ax=axes[1], width=0.4)
    sns.stripplot(x=df["sales"], color="#1f77b4", alpha=0.5, size=5, jitter=0.2, ax=axes[1])
    axes[1].set_title("Sales Boxplot (Spread & Outliers)", fontsize=13, weight="bold")
    axes[1].set_xlabel("Sales (Thousands of Units)", fontsize=11)

    fig.suptitle("Target Variable (Sales) Distribution Profile", fontsize=15, weight="bold", y=1.02)
    plt.tight_layout()
    sales_dist_file = out_path / "sales_distribution.png"
    plt.savefig(sales_dist_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] Sales distribution plot saved to: {sales_dist_file.resolve()}")

    # =========================================================================
    # STEP 3: Correlation Heatmap Matrix
    # =========================================================================
    plt.figure(figsize=(8, 6))
    corr_matrix = df[all_numeric].corr()
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".3f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        linewidths=1,
        square=True,
        cbar_kws={"shrink": 0.8, "label": "Pearson Correlation Coefficient (r)"},
    )
    plt.title("Pearson Correlation Heatmap: Ad Spends vs. Sales", fontsize=14, weight="bold", pad=14)
    plt.tight_layout()
    corr_file = out_path / "correlation_heatmap.png"
    plt.savefig(corr_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] Correlation heatmap saved to: {corr_file.resolve()}")

    # =========================================================================
    # STEP 4: Scatter Plots of Sales vs. Each Advertising Channel
    # =========================================================================
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    channel_colors = ["#2980b9", "#27ae60", "#e67e22"]

    for idx, col in enumerate(core_channels):
        ax = axes[idx]
        # Scatter with regplot for regression trendline and 95% confidence interval
        sns.regplot(
            data=df,
            x=col,
            y="sales",
            color=channel_colors[idx],
            scatter_kws={"alpha": 0.7, "s": 45, "edgecolor": "none"},
            line_kws={"color": "red", "linewidth": 2, "label": "Linear Fit"},
            ax=ax,
        )
        r_val = df[col].corr(df["sales"])
        ax.set_title(f"Sales vs. {col.upper()} Ad Spend\n(Pearson r = {r_val:.3f})", fontsize=12, weight="bold")
        ax.set_xlabel(f"{col.upper()} Advertising Spend ($k)", fontsize=11)
        ax.set_ylabel("Sales (Thousands of Units)", fontsize=11)
        ax.legend(loc="upper left", frameon=True, fontsize=9)

    fig.suptitle("Impact of Advertising Channels on Product Sales", fontsize=15, weight="bold", y=1.03)
    plt.tight_layout()
    scatter_file = out_path / "scatter_sales_vs_channels.png"
    plt.savefig(scatter_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] Channel scatter plots saved to: {scatter_file.resolve()}")

    # =========================================================================
    # STEP 5: Pairplot Matrix Across All Channels
    # =========================================================================
    g = sns.pairplot(
        df[["tv", "radio", "newspaper", "sales"]],
        diag_kind="kde",
        plot_kws={"alpha": 0.7, "s": 40, "color": "#1f77b4"},
        diag_kws={"fill": True, "color": "#3366cc"},
    )
    g.fig.subplots_adjust(top=0.93)
    g.fig.suptitle("Pairwise Relationships and Distributions Across Ad Channels", fontsize=14, weight="bold")
    pairplot_file = out_path / "pairplot.png"
    g.savefig(pairplot_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] Pairplot saved to: {pairplot_file.resolve()}")

    # =========================================================================
    # STEP 6: Channel Spend Contribution Analysis
    # =========================================================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    channel_totals = [df["tv"].sum(), df["radio"].sum(), df["newspaper"].sum()]
    channel_labels = ["TV Spend", "Radio Spend", "Newspaper Spend"]
    palette_pie = ["#3498db", "#2ecc71", "#e67e22"]

    # 6.1 Pie chart of budget allocation
    axes[0].pie(
        channel_totals,
        labels=channel_labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=palette_pie,
        explode=(0.05, 0.02, 0.02),
        textprops={"fontsize": 11, "weight": "bold"},
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )
    axes[0].set_title("Overall Marketing Budget Share by Channel", fontsize=13, weight="bold")

    # 6.2 Sales vs Total Spend
    sns.regplot(
        data=df,
        x="total_spend",
        y="sales",
        color="#8e44ad",
        scatter_kws={"alpha": 0.7, "s": 45},
        line_kws={"color": "red", "linewidth": 2, "label": "Linear Fit"},
        ax=axes[1],
    )
    r_total = df["total_spend"].corr(df["sales"])
    axes[1].set_title(f"Sales vs. Total Ad Spend ($k)\n(Pearson r = {r_total:.3f})", fontsize=13, weight="bold")
    axes[1].set_xlabel("Total Advertising Budget ($k)", fontsize=11)
    axes[1].set_ylabel("Sales (Thousands of Units)", fontsize=11)
    axes[1].legend(loc="upper left", frameon=True)

    fig.suptitle("Marketing Budget Allocation and Aggregate Sales Dynamics", fontsize=15, weight="bold", y=1.02)
    plt.tight_layout()
    contrib_file = out_path / "channel_spend_contribution.png"
    plt.savefig(contrib_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] Channel spend contribution plot saved to: {contrib_file.resolve()}")

    print("\n" + "=" * 65)
    print("EDA Complete! All plots and summary files generated in results/.")
    print("=" * 65)


def main():
    """Entry point for standalone EDA execution."""
    csv_path = project_root / "data" / "advertising.csv"
    results_dir = project_root / "results"
    df = load_sales_dataframe(file_path=str(csv_path))
    perform_eda(df, output_dir=str(results_dir))


if __name__ == "__main__":
    main()
