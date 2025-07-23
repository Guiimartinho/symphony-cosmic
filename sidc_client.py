# sidc_client.py

import requests
import logging
from typing import Dict, Any

from config import SIDC_SUNSPOT_URL

def fetch_sunspot_data() -> Dict[str, Any]:
    """
    Fetches the latest daily sunspot number from the SIDC/SILSO data file.
    """
    compiled_data: Dict[str, Any] = {}
    try:
        logging.info(f"Fetching Sunspot data from SIDC: {SIDC_SUNSPOT_URL}")
        response = requests.get(SIDC_SUNSPOT_URL, timeout=10)
        response.raise_for_status()
        
        # Parse the plain text file
        lines = response.text.strip().split('\n')
        last_line = lines[-1]
        columns = last_line.split()
        
        # The sunspot number is the 5th column (index 4)
        sunspot_number = float(columns[4])
        
        if sunspot_number >= 0:
            compiled_data['sunspot_number'] = int(sunspot_number)
            logging.info(f"Success! Fetched latest Sunspot Number: {sunspot_number}")
        else:
            logging.warning("Latest sunspot data is marked as missing (-1). Defaulting to 0.")
            compiled_data['sunspot_number'] = 0

    except Exception as e:
        logging.error(f"Failed during Sunspot fetch: {e}")
        compiled_data['sunspot_number'] = 0
    
    return compiled_data

# --- Test Block for Direct Execution ---
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    print("--- Running sidc_client.py in Standalone Test Mode ---")
    data = fetch_sunspot_data()
    print("\n--- Test Result ---")
    print(data)
    print("\n--- Test Finished ---")