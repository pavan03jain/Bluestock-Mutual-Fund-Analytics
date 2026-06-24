import os
import time
import requests
import pandas as pd
from datetime import datetime

TARGET_SCHEMES = {
    "125497": "HDFC_Top_100_Direct",
    "119551": "SBI_Bluechip",
    "120503": "ICICI_Bluechip",
    "118632": "Nippon_Large_Cap",
    "119092": "Axis_Bluechip",
    "120841": "Kotak_Bluechip"
}

def fetch_and_save_nav(scheme_code, filename_suffix, retries=3):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    for attempt in range(retries):
        try:
            # Increased timeout to 30 seconds to prevent ReadTimeouts
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            meta = data.get("meta", {})
            nav_data = data.get("data", [])
            
            if not nav_data:
                print(f"⚠️ No NAV data returned for code: {scheme_code}")
                return
            
            df = pd.DataFrame(nav_data)
            df['scheme_code'] = scheme_code
            df['scheme_name'] = meta.get('scheme_name', 'Unknown')
            df['extracted_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            os.makedirs("data/raw", exist_ok=True)
            output_path = f"data/raw/{scheme_code}_{filename_suffix}.csv"
            
            df.to_csv(output_path, index=False)
            print(f"✅ Saved API Fetch: {output_path} ({len(df)} historical records)")
            return  # Exit function successfully
            
        except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
            print(f"⏳ Attempt {attempt + 1}/{retries} failed for code {scheme_code}. Retrying in 3s...")
            time.sleep(3)
    print(f"❌ Failed to fetch AMFI code {scheme_code} after {retries} attempts.")

if __name__ == "__main__":
    print("=== STARTING LIVE NAV API EXTRACTION ===")
    for code, label in TARGET_SCHEMES.items():
        fetch_and_save_nav(code, label)
    print("=======================================\n")