# nasa_client.py (NASA DONKI API Client)

import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

from config import NASA_API_BASE_URL

def fetch_nasa_data(api_key: str) -> Dict[str, Any]:
    """
    Fetches data from NASA's DONKI endpoints (CME, GST, FLR).
    """
    if not api_key:
        logging.warning("NASA API key is missing.")
        return {}

    end_date = datetime.now()
    start_date_30_days = end_date - timedelta(days=30)
    start_date_2_days = end_date - timedelta(days=2)

    compiled_data: Dict[str, Any] = {}
    
    # --- Fetch 1: CME Speed Series (30-day range) ---
    try:
        params = {"startDate": start_date_30_days.strftime('%Y-%m-%d'), "endDate": end_date.strftime('%Y-%m-%d'), "api_key": api_key}
        response = requests.get(f"{NASA_API_BASE_URL}/CME", params=params, timeout=15)
        response.raise_for_status()
        events = response.json()
        speed_series = [
            analysis.get('speed', 0)
            for event in events
            if event.get('cmeAnalyses') for analysis in event['cmeAnalyses']
            if analysis.get('speed', 0) > 0
        ]
        compiled_data['cme_speed_series'] = speed_series[-16:]
        logging.info(f"CME fetch complete. Found {len(speed_series)} events.")
    except Exception as e:
        logging.error(f"Failed during CME fetch: {e}")

    # --- Fetch 2: GST Kp Index (30-day range) ---
    try:
        params = {"startDate": start_date_30_days.strftime('%Y-%m-%d'), "endDate": end_date.strftime('%Y-%m-%d'), "api_key": api_key}
        response = requests.get(f"{NASA_API_BASE_URL}/GST", params=params, timeout=15)
        response.raise_for_status()
        events = response.json()
        max_kp = 0
        if events:
            for event in events:
                if event.get('allKpIndex'):
                    for kp_reading in event['allKpIndex']:
                        kp_value = kp_reading.get('kpIndex', 0)
                        if kp_value > max_kp: max_kp = kp_value
        compiled_data['max_kp_index'] = int(max_kp)
        logging.info(f"GST fetch complete. Max KpIndex: {max_kp}")
    except Exception as e:
        logging.error(f"Failed during GST fetch: {e}")

    # --- Fetch 3: Solar Flares (2-day range) ---
    try:
        params = {"startDate": start_date_2_days.strftime('%Y-%m-%d'), "endDate": end_date.strftime('%Y-%m-%d'), "api_key": api_key}
        response = requests.get(f"{NASA_API_BASE_URL}/FLR", params=params, timeout=15)
        response.raise_for_status()
        events = response.json()
        latest_flare = events[-1] if events else None
        compiled_data['latest_flare'] = latest_flare
        if latest_flare:
            logging.info(f"Solar Flare fetch complete. Found a recent flare: {latest_flare.get('classType')}")
        else:
            logging.info("Solar Flare fetch complete. No recent flares.")
    except Exception as e:
        logging.error(f"Failed during Solar Flare fetch: {e}")

    return compiled_data

# --- Test Block for Direct Execution ---
if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    load_dotenv()
    test_api_key = os.getenv("NASA_API_KEY")
    print("--- Running nasa_client.py in Standalone Test Mode ---")
    if not test_api_key:
        logging.critical("CRITICAL: NASA_API_KEY not found in .env file.")
    else:
        fetched_data = fetch_nasa_data(test_api_key)
        print("\n--- Test Result ---")
        print(fetched_data)
    print("\n--- Test Finished ---")