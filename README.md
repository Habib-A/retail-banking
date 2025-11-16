# 🛍️ Retail Banking — RFM-Based Customer Segmentation

## 📋 Project Overview

This project applies **RFM (Recency, Frequency, Monetary)** analysis to retail banking transaction data to segment customers and develop targeted retention and engagement strategies for BankTrust.

**Business Goal:** Reduce churn, improve personalization, and optimize marketing efficiency through data-driven customer segmentation.

---

## 📁 Project Structures

```
retail-banking/
│
├── data/
│   ├── bank_data_C.csv              # Raw transaction data
│   ├──  processed/
│       ├── transactions_clean.csv           
│       ├── rfm_scores.csv                  
│       ├── kmeans_cluster_segments.csv     
│       └── cluster_profiles.csv             
│   └── cleaned_data.csv            # Cleaned transaction data
├── notebooks/
│   ├── Optimizing Retail Banking Strategies Through RFM-Based Customer Segmentation.ipynb        # Data cleaning, EDA, RFM segmentation
│   ├── 02_rfm_refinement.ipynb                                                                   # RFM refinement analysis 
│   └── 03_unsupervise_learning.ipynb                                                             # Unsupervise learning clustering analysis (4 Clusters)
│
└── README.md                        # This file
```

---


## 🧩 Tech Stack
| Category         | Tools & Libraries                 |
| ---------------- | --------------------------------- |
| Language         | Python                            |
| Data Analysis    | pandas, numpy                     |
| Visualization    | matplotlib, seaborn, plotly       |
| Machine Learning | scikit-learn (K-Means Clustering) |
| App Framework    | Streamlit                         |
| Version Control  | Git & GitHub                      |

---

## 🔍 Key Steps

1. **Data Cleaning**
   - Loaded 1,041,614 transactions from 879,358 unique customers
   - Parsed day-first dates with explicit format handling.
   - Fixed 2-digit year parsing issues (future DOBs corrected)
   - Combined date + time into `TransactionDateTime`
   - Validated: Zero duplicates
   
2. **Exploratory Data Analysis (EDA)**
   - **Demographics:** 73% male customers; top cities: Mumbai, New Delhi, Bangalore
   - **Distributions:** Heavy right skew in transaction amounts and account balances
   - **Outlier handling:**
     - IQR method flags 10–13% as outliers
     - Applied 1%–99% percentile capping for visualizations only
     - Raw data preserved for modeling
   - **Monthly trends:** Declining transaction volume from Aug → Oct (data coverage issue)

3. **RFM Segmentation (Initial)**
   - Computed **Recency** (days since last transaction), **Frequency** (transaction count), **Monetary** (total amount)
   - Assigned quintile scores (1–5) for each metric
     - **Champions:** R≥4, F≥4, M≥4
     - **Loyal:** R≥4, F≥3
     - **Potential Loyalists:** R≥3, F≥2, M≥3
     - **At Risk:** R≤2, F≤2, M≤2
     - **Need Attention:** R≤2, F≥4
     - **Others:** Everything else

4. **Feature Engineering**
   - Derived R (Recency), F (Frequency), and M (Monetary) scores
   - Scaled data for clustering

5. **Unsupervised Learning (K-Means)**
    - Determined optimal k using the Elbow Method and Silhouette Score
    - Applied K-Means clustering to segment customers (4 segments)
    - Evaluated clustering quality using Silhouette Score.
    - Profile each segment for business use

6. **Visualization**
  - Created RFM bar charts per cluster
  - Built an interactive dashboard using Streamlit for insights generation

---

## 📊 Cluster Insights
| Cluster | Business Name                      | Description                                                                                    |
| ------- | --------------------------------   | --------------------------------------------------------------------------------------------   |
| 0       | 🏆 **Big Spenders**               | Customers with the highest monetary value but weaker recency and frequency.                     |
| 1       | 🔁 **Loyal Customers**            | Best performing segment with excellent recency, high frequency, and substantial monetary value. |
| 2       | ⚠️ **At-Risk Customers**          | Customers showing poor performance across all RFM metrics - highest churn risk.                 |
| 3       | 💤 **Recent Low Value Customers** |  Recently active customers but with low transaction frequency and monetary value.               |
 
---

## 🚀 How to Run the App

1. **Clone the repository**

```bash
git clone https://github.com/Habib-A/retail-banking.git
cd rfm-segmentation
```

2.  **Install dependencies**

```bash
pip install -r requirements.txt
```

3.  **Run the Streamlit app**
```bash
https://retail-banking01.streamlit.app/
```

---

## 📈 Results

 - Segmented customers into four clear groups using K-Means.
 - Improved marketing targeting efficiency by identifying high-value segments.
 - Built and deployed Streamlit Dashboard for real-time insights.

---

## 📊 Data Dictionary

| Field                  | Description                          |
|------------------------|--------------------------------------|
| `TransactionID`        | Unique transaction identifier        |
| `CustomerID`           | Unique customer identifier           |
| `CustomerDOB`          | Customer date of birth               |
| `CustGender`           | Customer gender (M/F/T)              |
| `CustLocation`         | Customer city/location               |
| `CustAccountBalance`   | Current account balance (INR)        |
| `TransactionDate`      | Date of transaction                  |
| `TransactionTime`      | Time of transaction (HHMMSS)         |
| `TransactionAmount`    | Transaction value (INR)              |


---


📬 Author: Habib Pelumi Abdullahi

📧 habibpelumiabdullahi@gmail.com

