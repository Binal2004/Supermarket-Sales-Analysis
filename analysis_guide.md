# Analysis Guide — Supermarket Sales Project
**Author:** Binal Doshi | MSc AI & Data Science, University of Mumbai (2025–2027)
**Project:** Retail Domain — Supermarket Sales Analysis

---

## 1. Overview

This document provides a complete methodology reference for the Supermarket Sales Analysis project. It covers data dictionary, preprocessing steps, analytical methods used, visualization descriptions, and interpretation guidelines.

---

## 2. Dataset Dictionary

| Column | Type | Description |
|--------|------|-------------|
| `Invoice_ID` | string | Unique transaction identifier |
| `Branch` | categorical | Store branch code: A, B, or C |
| `City` | categorical | City of branch: Yangon, Mandalay, Naypyitaw |
| `Customer_Type` | categorical | Member or Normal |
| `Gender` | categorical | Male or Female |
| `Product_Line` | categorical | One of 6 product categories |
| `Unit_Price` | float | Price per unit ($) |
| `Quantity` | int | Number of units purchased (1–10) |
| `Tax` | float | 5% tax on cost of goods |
| `Total` | float | Total bill including tax |
| `Date` | date | Transaction date (Jan–Dec 2023) |
| `Time` | time | Transaction time (HH:MM) |
| `Payment` | categorical | Cash, Credit card, or E-wallet |
| `Rating` | float | Customer satisfaction rating (1–10) |

---

## 3. Feature Engineering

The following derived columns are added during preprocessing in `analysis_utils.load_data()`:

| Feature | Source | Description |
|---------|--------|-------------|
| `Month` | `Date` | Integer month (1–12) |
| `Month_Name` | `Date` | Abbreviated month string (Jan, Feb …) |
| `Day_of_Week` | `Date` | Integer (0=Monday … 6=Sunday) |
| `Day_Name` | `Date` | Full day name (Monday … Sunday) |
| `Hour` | `Time` | Integer hour of transaction (8–19) |

---

## 4. Analysis Methodology

### 4.1 Revenue Trend Analysis
- **Method:** Monthly aggregation of `Total` column
- **Chart:** Line chart with data labels and fill shading
- **Interpretation:** Identify seasonal peaks and troughs; Jul and Dec are consistently highest

### 4.2 Product Line Analysis
- **Method:** `groupby("Product_Line")["Total"].sum()`
- **Charts:** Horizontal bar chart (absolute revenue) + pie chart (share %)
- **Interpretation:** Health & Beauty leads with 18.7%; all product lines are relatively balanced (14.9%–18.7%), indicating healthy diversification

### 4.3 Branch Performance
- **Method:** Multi-key groupby on Branch and City; aggregating Revenue, Transaction Count, and mean Rating
- **Chart:** Three-panel bar comparison
- **Interpretation:** Branches B (Mandalay) and A (Yangon) are neck-and-neck; Branch C (Naypyitaw) has slightly fewer transactions but highest average rating (6.98)

### 4.4 Temporal Patterns
- **Method:** Day-of-week aggregation + pivot table (Day × Hour) for heatmap
- **Charts:** Bar chart + seaborn heatmap
- **Interpretation:** Saturday is the single highest-revenue day; the 18:00 hour is the busiest across all days. Evening hours (17–19) see consistent spikes, suggesting after-work shopping behavior

### 4.5 Customer Behavior
- **Method:** Cross-tabulation of Gender × Product_Line; comparison of Member vs Normal customer averages
- **Charts:** Grouped bar chart + dual-axis bar/line
- **Key stat:** Normal customers ($262.08 avg) spend marginally more per transaction than Members ($257.29), but the gap is small — loyalty programme ROI should be measured beyond transaction value

### 4.6 Payment Analysis
- **Method:** Groupby Payment, aggregating counts, revenue, and average transaction value
- **Charts:** Donut pie + revenue bar
- **Interpretation:** E-wallet leads in both transaction volume (720) and revenue share (36.2%). Credit card has the highest average transaction ($265.34), suggesting premium purchases skew toward card

### 4.7 Statistical Analysis
- **Method:** Descriptive statistics + Pearson correlation matrix (numeric columns only)
- **Key finding:** Rating shows near-zero correlation with Total spend (r ≈ -0.01), meaning high spenders are not necessarily more satisfied. This is important — satisfaction drivers are non-monetary

---

## 5. Visualization Reference

| File | Description | Key Insight |
|------|-------------|-------------|
| `viz1_monthly_revenue.png` | Monthly revenue line chart | Jul ($50,184) and Dec ($49,403) are peak months |
| `viz2_product_revenue.png` | Product line revenue bars | Health & Beauty leads at $96,970 |
| `viz3_branch_performance.png` | Branch KPI comparison | All three branches within 12% of each other |
| `viz4_day_of_week.png` | Revenue by day of week | Thursday is peak day ($79,450) |
| `viz5_heatmap.png` | Day × Hour sales heatmap | 18:00 hour is consistently the hottest slot |
| `viz6_payment.png` | Payment distribution | E-wallet = 36% of all transactions |
| `viz7_customer_analysis.png` | Gender × Product + Member analysis | Female customers drive Health & Beauty |
| `viz8_ratings_corr.png` | Rating histogram + correlation | Rating is independent of spend amount |
| `viz9_kpi_dashboard.png` | Executive KPI summary | All headline metrics in one view |
| `viz10_scatter.png` | Unit price vs quantity scatter | Most transactions cluster at mid-price, 5 units |

---

## 6. Statistical Notes & Assumptions

- **Tax calculation:** Tax = 5% of (Unit_Price × Quantity); Total = Tax × 21 (based on 5% tax structure in dataset)
- **Ratings scale:** 1–10 continuous; no strong ceiling/floor effects observed (mean 6.96, std 1.73)
- **No outlier removal:** Dataset is clean with no missing values; outliers were reviewed but not removed as they represent legitimate high-value transactions
- **Time zone:** All timestamps assumed to be local Myanmar time (MMT, UTC+6:30)

---

## 7. How to Reproduce Results

### Step 1 – Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 – Run the Jupyter notebook
```bash
jupyter notebook notebooks/supermarket_sales_analysis.ipynb
```

### Step 3 – Regenerate all visualizations programmatically
```bash
python src/analysis_utils.py
```

### Step 4 – Import utility functions in your own script
```python
from src.analysis_utils import load_data, get_kpis, monthly_revenue, plot_monthly_revenue

df = load_data("data/supermarket_sales.csv")
kpis = get_kpis(df)
print(kpis)
plot_monthly_revenue(df)
```

---

## 8. Business Recommendations Reference

| # | Finding | Recommendation | Expected Impact |
|---|---------|----------------|----------------|
| 1 | Health & Beauty leads revenue | Increase inventory 15–20% | Revenue +8% |
| 2 | Saturday is peak day | Launch loyalty double-point events on Saturdays | Revenue +12% |
| 3 | E-wallet leads transaction volume | Partner for cashback/exclusive discounts | Txn volume +10% |
| 4 | 18:00 is peak hour | Schedule evening flash sales 6–9 PM | Revenue +7% |
| 5 | Member spend ≈ Normal spend | Enhance membership benefits to grow loyalty base | Avg Spend +5% |
| 6 | Branches are nearly equal | Implement cross-branch best-practice sharing | Rating +0.3pts |

---

## 9. Limitations & Future Work

- **Geographic scope:** Data covers Myanmar branches only; findings may not generalise to other markets
- **No basket analysis:** Item-level data is not available; market basket / association rule analysis is not possible with this dataset
- **Single year:** Trends are based on 2023 only; multi-year comparison would strengthen seasonal conclusions
- **External factors:** No economic or competitor data available to contextualise revenue dips (e.g., August)

**Suggested next steps:**
- Forecasting next quarter's revenue using ARIMA or Prophet
- Customer segmentation using RFM (Recency, Frequency, Monetary) analysis
- Churn prediction for the membership programme

---

*Documentation prepared by Binal Doshi — MSc AI & Data Science Portfolio, University of Mumbai*
