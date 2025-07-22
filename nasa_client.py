# nasa_client.py (Version with two instruments: GST and CME)

import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

NASA_API_BASE_URL = "https://api.nasa.gov/DONKI"

def fetch_live_data(api_key: str) -> Dict[str, Any]:
    """
    Fetches data from two DONKI endpoints: GST and CME.
    """
    if not api_key:
        logging.warning("NASA API key is missing.")
        return {}

    end_date = datetime.now()
    start_date = end_date - timedelta(days=15)
    date_params = {
        "startDate": start_date.strftime('%Y-%m-%d'),
        "endDate": end_date.strftime('%Y-%m-%d'),
        "api_key": api_key
    }

    compiled_data: Dict[str, Any] = {}
    logging.info(f"Querying NASA DONKI from {date_params['startDate']} to {date_params['endDate']}...")

    # --- Fetch 1: Geomagnetic Storm (GST) for Kp Index ---
    try:
        logging.info("Fetching GST data for atmospheric noise...")
        response_gst = requests.get(f"{NASA_API_BASE_URL}/GST", params=date_params)
        response_gst.raise_for_status()
        gst_events = response_gst.json()
        
        max_kp = 0
        if gst_events:
            for event in gst_events:
                if event.get('allKpIndex'):
                    for kp_reading in event['allKpIndex']:
                        kp_value = kp_reading.get('kpIndex', 0)
                        if kp_value > max_kp:
                            max_kp = kp_value
        compiled_data['max_kp_index'] = int(max_kp)
        logging.info(f"GST Check Complete. Max KpIndex observed: {max_kp}")

    except Exception as e:
        logging.error(f"Failed during GST fetch: {e}")
        compiled_data['max_kp_index'] = 0 # Default to 0 on error

    # --- Fetch 2: Coronal Mass Ejection (CME) for Speed/Frequency ---
    try:
        logging.info("Fetching CME data for main frequency...")
        response_cme = requests.get(f"{NASA_API_BASE_URL}/CME", params=date_params)
        response_cme.raise_for_status()
        cme_events = response_cme.json()

        fastest_speed = 0
        if cme_events:
            for event in cme_events:
                # CMEs can have multiple analyses, we check the first one
                if event.get('cmeAnalyses'):
                    analysis = event['cmeAnalyses'][0]
                    speed = analysis.get('speed', 0)
                    if speed > fastest_speed:
                        fastest_speed = speed
        compiled_data['fastest_cme_speed'] = int(fastest_speed)
        logging.info(f"CME Check Complete. Fastest CME speed observed: {fastest_speed} km/s")

    except Exception as e:
        logging.error(f"Failed during CME fetch: {e}")
        compiled_data['fastest_cme_speed'] = 0 # Default to 0 on error

    return compiled_data