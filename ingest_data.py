import pandas as pd
from sqlalchemy import create_engine
import os

print("⏳ Connecting to Bluestock Mutual Fund Engine database...")
DB_URI = "postgresql://postgres:admin123@localhost:5432/bluestock_mf"
engine = create_engine(DB_URI)

SCORECARD_PATH = "notebooks/fund_scorecard.csv"

if os.path.exists(SCORECARD_PATH):
    print("📦 Reading fund scorecard dataset...")
    df = pd.read_csv(SCORECARD_PATH)
    
    # ----------------------------------------------------------------
    # 1. Populate dim_fund (Static Metadata Dimension)
    # ----------------------------------------------------------------
    print("🚀 Extracting and loading metadata into 'dim_fund'...")
    df_fund = df[['amfi_code', 'scheme_name']].copy()
    # Add a fallback placeholder for mandatory non-null fund_house column
    df_fund['fund_house'] = 'Unknown Fund House' 
    
    # Remove any duplicates to protect primary keys
    df_fund = df_fund.drop_duplicates(subset=['amfi_code'])
    
    # Push metadata
    df_fund.to_sql(name="dim_fund", con=engine, if_exists="append", index=False)
    print("✅ dim_fund successfully populated!")

    # ----------------------------------------------------------------
    # 2. Populate dim_performance_metrics (Analytical Star Dimension)
    # ----------------------------------------------------------------
    print("🚀 Mapping and loading indicators into 'dim_performance_metrics'...")
    
    # Rename matching columns to fit schema specifications perfectly
    df_metrics = df[[
        'amfi_code', 'overall_rank', 'cagr_3y', 
        'sharpe_ratio', 'alpha', 'max_drawdown', 'expense_ratio', 'fund_score'
    ]].copy()
    
    df_metrics = df_metrics.rename(columns={
        'expense_ratio': 'expense_ratio_pct'
    })
    
    # Push structured analytics values
    df_metrics.to_sql(name="dim_performance_metrics", con=engine, if_exists="append", index=False)
    print("✅ dim_performance_metrics successfully populated!")

else:
    print(f"❌ Error: Workspace asset {SCORECARD_PATH} not found.")

print("\n🏁 Star Schema migration framework execution finished successfully.")