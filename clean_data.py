import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Path configuration
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
DB_PATH = "bluestock_mf.db"

os.makedirs(PROCESSED_DIR, exist_ok=True)

print("⚡ Starting Day 2 Processing & Cleaning Pipeline...")

# ==========================================
# 1. CLEANING NAV HISTORY
# ==========================================
print("\n🧹 Processing nav_history.csv...")
nav_raw_path = os.path.join(RAW_DIR, "02_nav_history.csv")

if os.path.exists(nav_raw_path):
    df_nav = pd.read_csv(nav_raw_path)
    
    # Standardize column strings and convert dates to native objects
    df_nav.columns = df_nav.columns.str.strip().str.lower()
    df_nav['date'] = pd.to_datetime(df_nav['date'])
    
    # Sort chronological indexes sequentially to facilitate time-series lookups
    df_nav = df_nav.sort_values(by=['amfi_code', 'date']).drop_duplicates(subset=['amfi_code', 'date'])
    
    # Filter out anomalous data points
    df_nav = df_nav[df_nav['nav'] > 0]
    
    # Handle Market Weekends & Holidays: Create a dense comprehensive date grid per scheme and forward-fill values
    filled_nav_groups = []
    for amfi, group in df_nav.groupby('amfi_code'):
        full_date_range = pd.date_range(start=group['date'].min(), end=group['date'].max(), freq='D')
        group = group.set_index('date').reindex(full_date_range)
        group['amfi_code'] = amfi
        group['nav'] = group['nav'].ffill()  # Forward-fill weekend/holiday gaps
        group = group.reset_index().rename(columns={'index': 'date'})
        filled_nav_groups.append(group)
        
    df_nav_clean = pd.concat(filled_nav_groups, ignore_index=True)
    df_nav_clean.to_csv(os.path.join(PROCESSED_DIR, "clean_nav.csv"), index=False)
    print(f"   ✅ Saved clean_nav.csv! Rows updated from {len(df_nav)} to {len(df_nav_clean)}")
else:
    print("   ❌ Error: 02_nav_history.csv not found in data/raw/")

# ==========================================
# 2. CLEANING INVESTOR TRANSACTIONS
# ==========================================
print("\n🧹 Processing investor_transactions.csv...")
tx_raw_path = os.path.join(RAW_DIR, "08_investor_transactions.csv")

if os.path.exists(tx_raw_path):
    df_tx = pd.read_csv(tx_raw_path)
    df_tx.columns = df_tx.columns.str.strip().str.lower().str.replace(' ', '_')
    
    df_tx['transaction_date'] = pd.to_datetime(df_tx['transaction_date'])
    df_tx['transaction_type'] = df_tx['transaction_type'].str.strip().str.capitalize() # SIP/Lumpsum/Redemption
    df_tx = df_tx[df_tx['amount_inr'] > 0]
    
    df_tx.to_csv(os.path.join(PROCESSED_DIR, "clean_transactions.csv"), index=False)
    print(f"   ✅ Saved clean_transactions.csv! Cleaned {len(df_tx)} transaction rows.")

# ==========================================
# 3. STANDARDIZING ADDITIONAL CORE TABLES
# ==========================================
print("\n🧹 Standardizing remaining dimensions and facts...")
for file in os.listdir(RAW_DIR):
    if file.startswith(('01_', '03_', '04_', '05_', '06_', '07_', '09_', '10_')):
        df = pd.read_csv(os.path.join(RAW_DIR, file))
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('%', 'pct')
        clean_name = file.split('_', 1)[1]
        df.to_csv(os.path.join(PROCESSED_DIR, f"clean_{clean_name}"), index=False)

print("\n🎉 Flat-file cleaning sequence successfully terminated.")
# ==========================================
# 4. DATA MIGRATION TO SQLite DATABASE
# ==========================================
print("\n🗄️ Initializing relational storage compilation...")
engine = create_engine(f"sqlite:///{DB_PATH}")

# Initialize schema layout models using your local static file rules
with open("schema.sql", "r") as f:
    sql_schema = f.read()

# Split out separate command blocks to prevent engine parsing exceptions
with engine.connect() as connection:
    for statement in sql_schema.split(";"):
        if statement.strip():
            connection.execute(np.str_(statement))

print("   ✅ Normalised Star Schema tables generated successfully.")

# Stream processed rows into corresponding structural storage units
print("🚀 Loading data rows into the database tables...")
pd.read_csv(os.path.join(PROCESSED_DIR, "clean_fund_master.csv")).to_sql("dim_fund", engine, if_exists="append", index=False)
pd.read_csv(os.path.join(PROCESSED_DIR, "clean_nav.csv")).to_sql("fact_nav", engine, if_exists="append", index=False)
pd.read_csv(os.path.join(PROCESSED_DIR, "clean_transactions.csv")).to_sql("fact_transactions", engine, if_exists="append", index=False)

print("\n🏆 SUCCESS: Day 2 pipeline ran successfully! bluestock_mf.db database is compiled.")