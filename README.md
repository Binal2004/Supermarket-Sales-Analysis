# 🛒 Retail Domain — Supermarket Sales Analysis
### Data Analysis Portfolio 
**Author:** Binal Doshi 

---

## 📁 Project Structure

```
retail_project/
├── README.md                          ← This file
├── data/
│   ├── supermarket_sales.csv          ← Main dataset (2,000 rows)
│   └── house_prices.csv               ← Secondary dataset (300 rows)
├── notebooks/
│   └── supermarket_sales_analysis.ipynb  ← Full Jupyter notebook
├── reports/
│   └── supermarket_sales_report.pdf   ← Professional PDF report
├── visualizations/
│   ├── viz1_monthly_revenue.png
│   ├── viz2_product_revenue.png
│   ├── viz3_branch_performance.png
│   ├── viz4_day_of_week.png
│   ├── viz5_heatmap.png
│   ├── viz6_payment.png
│   ├── viz7_customer_analysis.png
│   ├── viz8_ratings_corr.png
│   ├── viz9_kpi_dashboard.png
│   └── viz10_scatter.png
└── src/
    └── (reusable analysis functions)
```

---

## 📊 Dataset

| Attribute | Detail |
|-----------|--------|
| File | `supermarket_sales.csv` |
| Records | 2,000 transactions |
| Period | Jan 2023 – Dec 2023 |
| Branches | A (Yangon), B (Mandalay), C (Naypyitaw) |
| Features | 14 columns |
| Missing Values | None |

---

## 🔍 Analysis Sections

1. **Data Loading & EDA** — Shape, types, missing values, feature engineering
2. **Revenue Trends** — Monthly sales trend with annotations
3. **Product Line Analysis** — Revenue bars, pie share, scatter plot
4. **Branch Performance** — Revenue, transactions, avg rating comparison
5. **Temporal Patterns** — Day-of-week bars + day×hour heatmap
6. **Customer Behavior** — Gender × product, member vs normal
7. **Payment Analysis** — Distribution pie + revenue by payment
8. **Statistical Analysis** — Rating histogram + correlation matrix
9. **KPI Dashboard** — Executive summary visualization
10. **Business Insights** — 6 actionable recommendations

---

## 💡 Key Findings

- **Total Revenue:** $519,280.69 across 2,000 transactions
- **Top Product:** Health & Beauty
- **Peak Day:** Saturday
- **Peak Hour:** 18:00 (6 PM)
- **Top Payment:** E-wallet
- **Avg Rating:** 6.97 / 10

---

## 🛠️ Requirements

```
pandas
numpy
matplotlib
seaborn
reportlab
nbformat
```

Install: `pip install pandas numpy matplotlib seaborn reportlab nbformat`

---

## 🚀 How to Run

```bash
# Run the Jupyter notebook
jupyter notebook notebooks/supermarket_sales_analysis.ipynb

# Or regenerate all visualizations + PDF
python3 generate_all.py
```
