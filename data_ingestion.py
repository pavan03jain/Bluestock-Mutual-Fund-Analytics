import os
import pandas as pd

def load_and_inspect_datasets(data_dir="data/raw"):
    """Scans raw directory, loads all CSV files, and prints structural summaries."""
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"⚠️ No CSV files found in '{data_dir}'. Make sure your files are placed there!")
        return {}
        
    datasets = {}
    print("=== STEP 1: BULK DATASET INSPECTION ===")
    for file in csv_files:
        path = os.path.join(data_dir, file)
        try:
            df = pd.read_csv(path)
            datasets[file] = df
            
            print(f"\n📄 File: {file}")
            print(f"   Shape (Rows, Columns): {df.shape}")
            print(f"   Columns & Types:\n{df.dtypes.to_string(prefix='     ')}")
            print(f"   First 2 Rows Sample:")
            print(df.head(2))
            print("-" * 50)
        except Exception as e:
            print(f"❌ Error reading {file}: {e}")
            
    return datasets

def explore_fund_master(datasets):
    """Explores metadata values mapping exactly to the 01_fund_master file schema."""
    print("\n=== STEP 2: FUND MASTER VALUE EXPLORATION ===")
    master_file = next((name for name in datasets if 'master' in name.lower()), None)
    
    if not master_file:
        print("⚠️ Master dataset file (01_fund_master.csv) not detected in data/raw.")
        return
        
    df = datasets[master_file]
    print(f"Analyzing Target: {master_file}")
    
    for col in df.columns:
        col_lower = col.lower()
        if 'house' in col_lower:
            print(f"📍 Unique Fund Houses: {df[col].nunique()}")
        elif 'sub_category' in col_lower:
            print(f"📍 Unique Sub-Categories Count: {df[col].nunique()} -> {list(df[col].unique()[:4])}...")
        elif 'category' in col_lower and 'sub' not in col_lower:
            print(f"📍 Distinct Macro Categories: {df[col].unique()}")
        elif 'risk' in col_lower:
            print(f"📍 Registered Risk Grades: {df[col].unique()}")

def validate_amfi_codes(datasets):
    """Validates structural integrity between master mappings and history logs."""
    print("\n=== STEP 3: DATA QUALITY & AMFI CROSS-VALIDATION ===")
    
    master_file = next((name for name in datasets if 'master' in name.lower()), None)
    history_file = next((name for name in datasets if 'history' in name.lower() or 'nav_history' in name.lower()), None)
    
    if not master_file or not history_file:
        print("⚠️ Skipping validation: Missing master schema or comprehensive tracking log mappings.")
        return
        
    m_df = datasets[master_file]
    h_df = datasets[history_file]
    
    m_col = [c for c in m_df.columns if 'code' in c.lower() or 'amfi' in c.lower()][0]
    h_col = [c for c in h_df.columns if 'code' in c.lower() or 'amfi' in c.lower()][0]
    
    master_set = set(m_df[m_col].dropna().unique())
    history_set = set(h_df[h_col].dropna().unique())
    
    missing_codes = master_set - history_set
    
    print("📊 Data Quality Integrity Check Summary:")
    print(f"   Unique AMFI Codes mapped in Master: {len(master_set)}")
    print(f"   Unique AMFI Codes appearing in History Logs: {len(history_set)}")
    
    if len(missing_codes) == 0:
        print("   ✅ PASSED: Every scheme code in fund_master matches historical log entries.")
    else:
        print(f"   ❌ STRUCTURAL GAP: {len(missing_codes)} master codes are missing from the history table.")

if __name__ == "__main__":
    data_cache = load_and_inspect_datasets()
    if data_cache:
        explore_fund_master(data_cache)
        validate_amfi_codes(data_cache)