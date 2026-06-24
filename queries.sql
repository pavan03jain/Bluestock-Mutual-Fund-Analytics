-- 1. Top 5 Funds Ranked by Expense Ratio (Lowest to Highest)
SELECT amfi_code, fund_house, scheme_name, expense_ratio_pct 
FROM dim_fund 
WHERE expense_ratio_pct IS NOT NULL
ORDER BY expense_ratio_pct ASC 
LIMIT 5;

-- 2. Average NAV Per Scheme Mapped Across Available Logs
SELECT amfi_code, AVG(nav) AS avg_historical_nav, COUNT(date) AS total_logged_days
FROM fact_nav 
GROUP BY amfi_code
ORDER BY avg_historical_nav DESC;

-- 3. Total Investment Allocation Breakdown Grouped by State Locations
SELECT state, SUM(amount_inr) AS total_invested_amount, COUNT(*) AS total_transactions
FROM fact_transactions
GROUP BY state
ORDER BY total_invested_amount DESC;

-- 4. Transaction Volume Distribution Segmented by Investor Age Demographics
SELECT age_group, transaction_type, COUNT(*) AS transaction_count, SUM(amount_inr) AS volume_inr
FROM fact_transactions
GROUP BY age_group, transaction_type
ORDER BY age_group, volume_inr DESC;

-- 5. High-Risk High-Expense Schemes Screening
SELECT amfi_code, scheme_name, fund_house, risk_category, expense_ratio_pct
FROM dim_fund
WHERE risk_category IN ('Very High', 'High') AND expense_ratio_pct > 1.5
ORDER BY expense_ratio_pct DESC;