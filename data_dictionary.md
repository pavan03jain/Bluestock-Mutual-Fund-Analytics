# Bluestock Mutual Fund Analytics Platform — Data Dictionary

## 1. dim_fund (Dimension Table)
Contains the master reference properties for all 40+ tracked mutual fund schemes.

| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `amfi_code` | TEXT | Primary Key | Unique 6-digit AMFI identifier code for the fund scheme. |
| `fund_house` | TEXT | - | Name of the Asset Management Company (e.g., SBI Mutual Fund). |
| `scheme_name` | TEXT | - | Complete official nomenclature of the fund scheme. |
| `category` | TEXT | - | Macro asset class categorization (Equity, Debt, Hybrid). |
| `sub_category` | TEXT | - | Micro strategy target segment (Large Cap, Mid Cap, Small Cap, Liquid). |
| `expense_ratio_pct` | REAL | - | Total annual operations charge expressed as a percentage value. |
| `risk_category` | TEXT | - | SEBI risk ranking profile (Low, Moderate, High, Very High). |

## 2. fact_nav (Fact Table)
Tracks granular time-series daily Net Asset Value logs across operational market dates.

| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `amfi_code` | TEXT | Foreign Key | References `dim_fund(amfi_code)` mapping. |
| `date` | TEXT | Composite PK | Timestamp of target valuation (includes forward-filled dates). |
| `nav` | REAL | - | Net Asset Value in Indian Rupees (INR) for that specific date index. |

## 3. fact_transactions (Fact Table)
Logs simulated retail and institutional transaction operations across Indian states.

| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `investor_id` | TEXT | - | Unique structural hash string tracking distinct investors. |
| `transaction_date`| TEXT | - | Point-in-time timestamp when the transaction occurred. |
| `amfi_code` | TEXT | Foreign Key | Target financial instrument code mapped back to fund master. |
| `transaction_type`| TEXT | - | Financial movement classification: SIP, Lumpsum, or Redemption. |
| `amount_inr` | INTEGER | - | Numerical value of capital moved measured in INR. |
| `state` | TEXT | - | Domestic regional state origin mapping investor profile location. |