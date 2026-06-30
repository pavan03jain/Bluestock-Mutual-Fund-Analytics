-- ====================================================================
-- DIMENSION 1: Core Fund Metadata (Static Master Records)
-- ====================================================================
DROP TABLE IF EXISTS dim_fund CASCADE;
CREATE TABLE dim_fund (
    amfi_code INT PRIMARY KEY,
    fund_house VARCHAR(150) NOT NULL,
    scheme_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    sub_category VARCHAR(100),
    plan VARCHAR(50),
    launch_date DATE,
    benchmark VARCHAR(150),
    fund_manager VARCHAR(150),
    sebi_category_code VARCHAR(50)
);

-- ====================================================================
-- DIMENSION 2: Advanced Performance Engineering Metrics 
-- (Directly feeds your Power BI Scatter Matrix & Leaderboard)
-- ====================================================================
DROP TABLE IF EXISTS dim_performance_metrics CASCADE;
CREATE TABLE dim_performance_metrics (
    amfi_code INT PRIMARY KEY,
    overall_rank INT NOT NULL,
    cagr_3y NUMERIC(5, 2),
    sharpe_ratio NUMERIC(4, 2),
    alpha NUMERIC(5, 2),
    max_drawdown NUMERIC(5, 2),
    expense_ratio_pct NUMERIC(4, 2),
    exit_load_pct NUMERIC(4, 2),
    fund_score NUMERIC(5, 2),
    risk_category VARCHAR(50),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code) ON DELETE CASCADE
);

-- ====================================================================
-- FACT TABLE 1: Historical Daily Performance Ledger (Time-Series)
-- ====================================================================
DROP TABLE IF EXISTS fact_nav CASCADE;
CREATE TABLE fact_nav (
    amfi_code INT,
    date DATE,
    nav NUMERIC(10, 4) NOT NULL,
    PRIMARY KEY (amfi_code, date),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code) ON DELETE CASCADE
);

-- ====================================================================
-- FACT TABLE 2: Investor Transaction Demographics Ledger 
-- (Feeds Regional Density & AUM Growth Plots)
-- ====================================================================
DROP TABLE IF EXISTS fact_transactions CASCADE;
CREATE TABLE fact_transactions (
    transaction_id SERIAL PRIMARY KEY,
    investor_id VARCHAR(100) NOT NULL,
    transaction_date DATE NOT NULL,
    amfi_code INT NOT NULL,
    transaction_type VARCHAR(20) CHECK (transaction_type IN ('SIP', 'LUMP_SUM', 'REDEMPTION')),
    amount_inr NUMERIC(12, 2) NOT NULL,
    state VARCHAR(100),
    city VARCHAR(100),
    city_tier VARCHAR(10),
    age_group VARCHAR(20),
    gender VARCHAR(10),
    annual_income_lakh NUMERIC(5, 2),
    payment_mode VARCHAR(50),
    kyc_status VARCHAR(20),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code) ON DELETE CASCADE
);

-- ====================================================================
-- PERFORMANCE INDEXING (Crucial for high-paying MLOps/Data Eng roles)
-- Ensures dashboards render instantly even with millions of rows.
-- ====================================================================
CREATE INDEX idx_perf_rank ON dim_performance_metrics (overall_rank);
CREATE INDEX idx_nav_date ON fact_nav (date);
CREATE INDEX idx_trans_date ON fact_transactions (transaction_date);