"""
analysis_utils.py
=================
Reusable analysis functions for the Supermarket Sales project.

Author : Binal Doshi
Program: MSc AI & Data Science, University of Mumbai (2025–2027)
Project: Retail Domain — Supermarket Sales Analysis
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
VIZ_DIR = ROOT / "visualizations"
VIZ_DIR.mkdir(exist_ok=True)

# ── Colour palette ────────────────────────────────────────────────────────────
PALETTE = {
    "primary":    "#1A6B8A",
    "secondary":  "#2ECC71",
    "accent":     "#E74C3C",
    "highlight":  "#F39C12",
    "neutral":    "#95A5A6",
    "background": "#F8F9FA",
}
PRODUCT_COLORS = [
    "#1A6B8A", "#2ECC71", "#E74C3C",
    "#F39C12", "#9B59B6", "#1ABC9C",
]
BRANCH_COLORS  = ["#1A6B8A", "#E74C3C", "#2ECC71"]

plt.rcParams.update({
    "figure.facecolor": PALETTE["background"],
    "axes.facecolor":   PALETTE["background"],
    "font.family":      "DejaVu Sans",
    "axes.spines.top":  False,
    "axes.spines.right":False,
})


# ── Data Loading ──────────────────────────────────────────────────────────────

def load_data(path: str | Path | None = None) -> pd.DataFrame:
    """Load and preprocess the supermarket sales CSV.

    Parameters
    ----------
    path : str or Path, optional
        Full path to the CSV file.  Defaults to ``data/supermarket_sales.csv``
        relative to the project root.

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe with engineered features:
        ``Date``, ``Time``, ``Month``, ``Month_Name``, ``Day_of_Week``,
        ``Hour``, ``Day_Name``.
    """
    if path is None:
        path = DATA_DIR / "supermarket_sales.csv"
    df = pd.read_csv(path)

    # Parse datetime
    df["Date"] = pd.to_datetime(df["Date"])
    df["Time"] = pd.to_datetime(df["Time"], format="%H:%M")

    # Feature engineering
    df["Month"]       = df["Date"].dt.month
    df["Month_Name"]  = df["Date"].dt.strftime("%b")
    df["Day_of_Week"] = df["Date"].dt.dayofweek          # 0 = Monday
    df["Day_Name"]    = df["Date"].dt.strftime("%A")
    df["Hour"]        = df["Time"].dt.hour

    return df


# ── Summary Helpers ───────────────────────────────────────────────────────────

def get_kpis(df: pd.DataFrame) -> dict:
    """Return a dict of headline KPI values."""
    return {
        "total_revenue":       round(df["Total"].sum(), 2),
        "total_transactions":  len(df),
        "avg_transaction":     round(df["Total"].mean(), 2),
        "avg_rating":          round(df["Rating"].mean(), 2),
        "top_product":         df.groupby("Product_Line")["Total"].sum().idxmax(),
        "peak_day":            df.groupby("Day_Name")["Total"].sum().idxmax(),
        "peak_hour":           int(df.groupby("Hour")["Total"].sum().idxmax()),
        "top_payment":         df["Payment"].value_counts().idxmax(),
    }


def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly revenue, transaction count, and average ticket size."""
    grp = df.groupby("Month").agg(
        Revenue=("Total", "sum"),
        Transactions=("Invoice_ID", "count"),
    ).reset_index()
    grp["Avg_Ticket"] = (grp["Revenue"] / grp["Transactions"]).round(2)
    month_map = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                 7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
    grp["Month_Name"] = grp["Month"].map(month_map)
    return grp


def product_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue and share by product line, sorted descending."""
    rev = df.groupby("Product_Line")["Total"].sum().reset_index()
    rev.columns = ["Product_Line", "Revenue"]
    rev["Share"] = (rev["Revenue"] / rev["Revenue"].sum() * 100).round(1)
    return rev.sort_values("Revenue", ascending=False).reset_index(drop=True)


def branch_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue, transactions, and avg rating per branch."""
    return df.groupby(["Branch", "City"]).agg(
        Revenue=("Total", "sum"),
        Transactions=("Invoice_ID", "count"),
        Avg_Rating=("Rating", "mean"),
    ).round(2).reset_index()


def payment_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Transactions, revenue, avg transaction, and revenue share by payment."""
    grp = df.groupby("Payment").agg(
        Transactions=("Invoice_ID", "count"),
        Revenue=("Total", "sum"),
    ).reset_index()
    grp["Avg_Transaction"] = (grp["Revenue"] / grp["Transactions"]).round(2)
    grp["Revenue_Share"]   = (grp["Revenue"] / grp["Revenue"].sum() * 100).round(1)
    return grp.sort_values("Revenue", ascending=False).reset_index(drop=True)


# ── Visualization Functions ───────────────────────────────────────────────────

def _save(fig: plt.Figure, filename: str) -> Path:
    """Save figure to the visualizations directory and close it."""
    out = VIZ_DIR / filename
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✔  Saved {out.name}")
    return out


def plot_monthly_revenue(df: pd.DataFrame) -> Path:
    """Line chart of monthly revenue (viz1)."""
    data  = monthly_revenue(df)
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(data["Month_Name"], data["Revenue"],
            marker="o", linewidth=2.5, color=PALETTE["primary"], zorder=3)
    ax.fill_between(range(len(data)), data["Revenue"],
                    alpha=0.12, color=PALETTE["primary"])
    for _, row in data.iterrows():
        ax.annotate(f"${row['Revenue']:,.0f}",
                    xy=(row["Month"]-1, row["Revenue"]),
                    xytext=(0, 10), textcoords="offset points",
                    ha="center", fontsize=8, color=PALETTE["primary"])
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(data["Month_Name"])
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.set_title("Monthly Revenue Trend (2023)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Month"); ax.set_ylabel("Total Revenue ($)")
    fig.tight_layout()
    return _save(fig, "viz1_monthly_revenue.png")


def plot_product_revenue(df: pd.DataFrame) -> Path:
    """Horizontal bar chart of revenue by product line (viz2)."""
    data = product_revenue(df)
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(data["Product_Line"], data["Revenue"],
                   color=PRODUCT_COLORS[:len(data)])
    for bar, val in zip(bars, data["Revenue"]):
        ax.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2,
                f"${val:,.0f}", va="center", fontsize=9)
    ax.set_xlabel("Total Revenue ($)")
    ax.set_title("Revenue by Product Line", fontsize=14, fontweight="bold", pad=15)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    fig.tight_layout()
    return _save(fig, "viz2_product_revenue.png")


def plot_branch_performance(df: pd.DataFrame) -> Path:
    """Side-by-side bar charts for branch KPIs (viz3)."""
    data = branch_summary(df)
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    metrics = [("Revenue", "Revenue ($)", BRANCH_COLORS),
               ("Transactions", "# Transactions", BRANCH_COLORS),
               ("Avg_Rating", "Avg Rating (/10)", BRANCH_COLORS)]
    for ax, (col, label, colors) in zip(axes, metrics):
        bars = ax.bar(data["City"], data[col], color=colors, width=0.55)
        for bar, val in zip(bars, data[col]):
            fmt = f"${val:,.0f}" if col == "Revenue" else f"{val:,.2f}" if col == "Avg_Rating" else f"{val:,}"
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01*data[col].max(),
                    fmt, ha="center", fontsize=9, fontweight="bold")
        ax.set_title(label, fontsize=11, fontweight="bold")
        ax.set_xlabel("Branch")
    fig.suptitle("Branch Performance Comparison", fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    return _save(fig, "viz3_branch_performance.png")


def plot_day_of_week(df: pd.DataFrame) -> Path:
    """Bar chart of revenue by day of week (viz4)."""
    order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    data  = df.groupby("Day_Name")["Total"].sum().reindex(order).reset_index()
    peak  = data["Total"].idxmax()
    colors = [PALETTE["accent"] if i == peak else PALETTE["primary"]
              for i in range(len(data))]
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(data["Day_Name"], data["Total"], color=colors, width=0.6)
    for bar, val in zip(bars, data["Total"]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
                f"${val:,.0f}", ha="center", fontsize=8)
    ax.set_title("Total Revenue by Day of Week", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Day"); ax.set_ylabel("Revenue ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=PALETTE["accent"], label="Peak Day"),
                        Patch(color=PALETTE["primary"], label="Other Days")],
              loc="upper left", framealpha=0.8)
    fig.tight_layout()
    return _save(fig, "viz4_day_of_week.png")


def plot_heatmap(df: pd.DataFrame) -> Path:
    """Day × Hour revenue heatmap (viz5)."""
    order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    pivot = df.pivot_table(values="Total", index="Day_Name",
                           columns="Hour", aggfunc="sum").reindex(order)
    fig, ax = plt.subplots(figsize=(13, 5))
    sns.heatmap(pivot, cmap="YlOrRd", ax=ax, linewidths=0.3,
                cbar_kws={"label": "Revenue ($)"})
    ax.set_title("Sales Heatmap: Day of Week vs Hour of Day",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Hour of Day"); ax.set_ylabel("Day of Week")
    fig.tight_layout()
    return _save(fig, "viz5_heatmap.png")


def plot_payment(df: pd.DataFrame) -> Path:
    """Payment method pie + revenue bar (viz6)."""
    data = payment_summary(df)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    colors = [PALETTE["primary"], PALETTE["secondary"], PALETTE["accent"]]
    ax1.pie(data["Transactions"], labels=data["Payment"],
            autopct="%1.1f%%", colors=colors,
            wedgeprops={"width": 0.55}, startangle=140)
    ax1.set_title("Payment Method Distribution", fontsize=12, fontweight="bold")
    bars = ax2.bar(data["Payment"], data["Revenue"], color=colors, width=0.5)
    for bar, val in zip(bars, data["Revenue"]):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
                 f"${val:,.0f}", ha="center", fontsize=9, fontweight="bold")
    ax2.set_title("Revenue by Payment Method", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Revenue ($)")
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    fig.tight_layout()
    return _save(fig, "viz6_payment.png")


def plot_customer_analysis(df: pd.DataFrame) -> Path:
    """Gender × product + member vs normal comparison (viz7)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Gender × product
    gender_prod = df.groupby(["Product_Line","Gender"])["Total"].sum().unstack()
    gender_prod.plot(kind="bar", ax=ax1, color=[PALETTE["primary"], PALETTE["accent"]],
                     width=0.7, edgecolor="white")
    ax1.set_title("Product Line Revenue by Gender", fontsize=11, fontweight="bold")
    ax1.set_xlabel(""); ax1.set_ylabel("Revenue ($)")
    ax1.tick_params(axis="x", rotation=30)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax1.legend(title="Gender")

    # Member vs Normal
    mem = df.groupby("Customer_Type").agg(
        Avg_Spend=("Total","mean"), Count=("Invoice_ID","count")).reset_index()
    color_map = {"Member": PALETTE["primary"], "Normal": PALETTE["accent"]}
    bar_colors = [color_map.get(t, PALETTE["neutral"]) for t in mem["Customer_Type"]]
    ax2b = ax2.twinx()
    ax2.bar(mem["Customer_Type"], mem["Avg_Spend"], color=bar_colors,
            width=0.4, alpha=0.85, label="Avg Spend ($)")
    ax2b.plot(mem["Customer_Type"], mem["Count"], marker="o", color=PALETTE["highlight"],
              linewidth=2, markersize=8, label="# Transactions")
    ax2.set_title("Member vs Normal Customer", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Avg Spend ($)"); ax2b.set_ylabel("# Transactions")
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2b.get_legend_handles_labels()
    ax2.legend(lines1+lines2, labels1+labels2, loc="upper right", fontsize=8)

    fig.tight_layout()
    return _save(fig, "viz7_customer_analysis.png")


def plot_ratings_corr(df: pd.DataFrame) -> Path:
    """Rating histogram + correlation matrix (viz8)."""
    num_cols = ["Unit_Price","Quantity","Tax","Total","Rating"]
    corr = df[num_cols].corr()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    ax1.hist(df["Rating"], bins=20, color=PALETTE["primary"], edgecolor="white", alpha=0.85)
    ax1.axvline(df["Rating"].mean(),   color=PALETTE["accent"],    linestyle="--", label=f"Mean: {df['Rating'].mean():.2f}")
    ax1.axvline(df["Rating"].median(), color=PALETTE["highlight"], linestyle=":",  label=f"Median: {df['Rating'].median():.2f}")
    ax1.set_title("Customer Rating Distribution", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Rating"); ax1.set_ylabel("Frequency")
    ax1.legend()

    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(corr, ax=ax2, annot=True, fmt=".2f", cmap="coolwarm",
                center=0, linewidths=0.5, mask=mask,
                cbar_kws={"shrink": 0.8})
    ax2.set_title("Feature Correlation Matrix", fontsize=12, fontweight="bold")

    fig.tight_layout()
    return _save(fig, "viz8_ratings_corr.png")


def plot_kpi_dashboard(df: pd.DataFrame) -> Path:
    """Executive KPI dashboard (viz9)."""
    kpis = get_kpis(df)
    fig = plt.figure(figsize=(14, 7))
    fig.patch.set_facecolor("#1A2E44")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor("#1A2E44")
    ax.axis("off")

    # Title
    ax.text(0.5, 0.93, "Supermarket Sales — Executive KPI Dashboard",
            ha="center", va="center", fontsize=16, fontweight="bold",
            color="white", transform=ax.transAxes)
    ax.text(0.5, 0.87, "January 2023 – December 2023  |  All Branches",
            ha="center", va="center", fontsize=10, color="#95A5A6",
            transform=ax.transAxes)

    # KPI cards
    cards = [
        ("Total Revenue",     f"${kpis['total_revenue']:,.0f}", "#2ECC71"),
        ("Transactions",      f"{kpis['total_transactions']:,}",  "#3498DB"),
        ("Avg Transaction",   f"${kpis['avg_transaction']:,.2f}", "#F39C12"),
        ("Avg Rating",        f"{kpis['avg_rating']:.2f}/10",     "#9B59B6"),
        ("Top Product",       kpis["top_product"],                "#E74C3C"),
        ("Peak Shopping Day", kpis["peak_day"],                   "#1ABC9C"),
    ]
    for i, (label, value, color) in enumerate(cards):
        x = 0.08 + (i % 3) * 0.31
        y = 0.58 if i < 3 else 0.25
        rect = plt.Rectangle((x-0.13, y-0.12), 0.27, 0.22,
                               facecolor=color, alpha=0.15,
                               transform=ax.transAxes, clip_on=False,
                               linewidth=2, edgecolor=color)
        ax.add_patch(rect)
        ax.text(x, y+0.06, value, ha="center", fontsize=13, fontweight="bold",
                color=color, transform=ax.transAxes)
        ax.text(x, y-0.04, label, ha="center", fontsize=8,
                color="#BDC3C7", transform=ax.transAxes)

    return _save(fig, "viz9_kpi_dashboard.png")


def plot_scatter(df: pd.DataFrame) -> Path:
    """Unit price vs quantity scatter by product line (viz10)."""
    fig, ax = plt.subplots(figsize=(11, 6))
    products = df["Product_Line"].unique()
    for prod, color in zip(products, PRODUCT_COLORS):
        subset = df[df["Product_Line"] == prod]
        ax.scatter(subset["Unit_Price"], subset["Quantity"],
                   label=prod, color=color, alpha=0.55, s=25)
    ax.set_title("Unit Price vs Quantity Sold by Product Line",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Unit Price ($)"); ax.set_ylabel("Quantity")
    ax.legend(title="Product Line", bbox_to_anchor=(1.01, 1), loc="upper left",
              fontsize=8)
    fig.tight_layout()
    return _save(fig, "viz10_scatter.png")


# ── Generate All ──────────────────────────────────────────────────────────────

def generate_all_visualizations(df: pd.DataFrame | None = None):
    """Run every plot function and save to the visualizations directory."""
    if df is None:
        df = load_data()
    print("Generating all visualizations …")
    plot_monthly_revenue(df)
    plot_product_revenue(df)
    plot_branch_performance(df)
    plot_day_of_week(df)
    plot_heatmap(df)
    plot_payment(df)
    plot_customer_analysis(df)
    plot_ratings_corr(df)
    plot_kpi_dashboard(df)
    plot_scatter(df)
    print(f"\nAll visualizations saved to: {VIZ_DIR}")


if __name__ == "__main__":
    generate_all_visualizations()
