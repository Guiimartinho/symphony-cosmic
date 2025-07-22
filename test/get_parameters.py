# get_parameters.py
# A single-purpose script to get the definitive list of parameters from the NASA HAPI server.

import requests
import json

# The HAPI "info" URL for our dataset asks for metadata, not data.
INFO_URL = "https://cdaweb.gsfc.nasa.gov/hapi/info?id=OMNI_HRO_1MIN"

print(f"--- Asking NASA for the official parameter list for OMNI_HRO_1MIN ---")
print(f"Requesting URL: {INFO_URL}")

try:
    response = requests.get(INFO_URL)
    response.raise_for_status()  # Check for HTTP errors (like 404, 500)

    info_data = response.json()

    # The parameter list is under the 'parameters' key in the JSON response
    parameters = info_data.get('parameters', [])

    print("\n--- OFFICIAL PARAMETER LIST FROM NASA SERVER ---")
    if not parameters:
        print("Could not retrieve parameter list from the server.")
    else:
        # Loop through the list of parameters and print the 'name' of each one
        for param in parameters:
            name = param.get('name')
            description = param.get('description', 'No description')
            units = param.get('units', '')
            print(f"- Name: '{name}' \t (Units: {units})")
    
    print("\n--- End of List ---")
    print("Please compare this list with the parameters in 'nasa_client.py'.")

except requests.exceptions.RequestException as e:
    print(f"\nERROR: Failed to connect to NASA server: {e}")
except json.JSONDecodeError:
    print(f"\nERROR: Failed to parse the response from the server. It was not valid JSON.")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")