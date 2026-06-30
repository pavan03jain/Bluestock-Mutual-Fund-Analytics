-- ====================================================================
-- 1. Top 5 Funds Ranked by Expense Ratio (Lowest to Highest)
-- Pulls from the updated performance metrics dimension table.
-- ====================================================================
SELECT 
    f.amfi_code, 
    f.fund_house, 
    f.scheme_name, 
    p.expense_ratio_pct 
FROM dim_fund f
INNER JOIN dim_performance_metrics p ON f.amfi_code = p.amfi_code
WHERE p.expense_ratio_pct IS NOT NULL
ORDER BY p.expense_ratio_pct ASC 
LIMIT 5;


-- ====================================================================
-- 2. Average NAV Per Scheme Mapped Across Available Logs
-- Aggregates numerical values across historical ledger dates.
-- ====================================================================
SELECT 
    f.scheme_name,
    n.amfi_code, 
    ROUND(AVG(n.nav), 4) AS avg_historical_nav, 
    COUNT(n.date) AS total_logged_days
FROM fact_nav n
INNER JOIN dim_fund f ON n.amfi_code = f.amfi_code
GROUP BY f.scheme_name, n.amfi_code
ORDER BY avg_historical_nav DESC;


-- ====================================================================
-- 3. Total Investment Allocation Breakdown Grouped by State Locations
-- Tracks demographic layout metrics across geographic layers.
-- ====================================================================
SELECT 
    state, 
    SUM(amount_inr) AS total_invested_amount, 
    COUNT(*) AS total_transactions
FROM fact_transactions
WHERE state IS NOT NULL
GROUP BY state
ORDER BY total_invested_amount DESC;


-- ====================================================================
-- 4. Transaction Volume Distribution Segmented by Investor Age Demographics
-- Groups portfolio action flows by age ranges.
-- ====================================================================
SELECT 
    age_group, 
    transaction_type, 
    COUNT(*) AS transaction_count, 
    SUM(amount_inr) AS volume_inr
FROM fact_transactions
WHERE age_group IS NOT NULL
GROUP BY age_group, transaction_type
ORDER BY age_group ASC, volume_inr DESC;


-- ====================================================================
-- 5. High-Risk High-Expense Schemes Screening
-- Screens across static profiles and active evaluation dimensions.
-- ====================================================================
SELECT 
    f.amfi_code, 
    f.scheme_name, 
    f.fund_house, 
    p.risk_category, 
    p.expense_ratio_pct
FROM dim_fund f
INNER JOIN dim_performance_metrics p ON f.amfi_code = p.amfi_code
WHERE p.risk_category IN ('Very High', 'High') 
  AND p.expense_ratio_pct > 1.5
ORDER BY p.expense_ratio_pct DESC;