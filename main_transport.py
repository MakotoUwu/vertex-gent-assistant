# main_transport.py (contains De Lijn API functions)
import functions_framework
import os
import requests

# Load API Key from environment variable set during deployment
DE_LIJN_API_KEY = os.environ.get("DE_LIJN_API_KEY")
# Base URL - Verify this in the official De Lijn documentation
DE_LIJN_API_BASE_URL = os.environ.get("DE_LIJN_API_BASE_URL", "https://api.delijn.be/v1")

@functions_framework.http
def get_transport_disruptions(request):
    """HTTP Cloud Function to get transport disruptions from De Lijn API."""
    if not DE_LIJN_API_KEY:
        print("Error: DE_LIJN_API_KEY environment variable not set.")
        return {"status": "error", "error_message": "API key is not configured on the server."}, 500

    request_json = request.get_json(silent=True)
    query_filter = None # Optional filter based on user query
    if request.args and 'filter' in request.args:
        query_filter = request.args.get('filter')
    elif request_json and 'filter' in request_json:
        query_filter = request_json['filter']

    headers = {
        "Ocp-Apim-Subscription-Key": DE_LIJN_API_KEY
    }
    # IMPORTANT: Verify the correct endpoint and parameters in De Lijn documentation
    endpoint = f"{DE_LIJN_API_BASE_URL}/disruptions" # Example endpoint
    params = {
        "area": "Gent" # Example parameter - Check API docs for filtering by area
    }
    if query_filter:
        # IMPORTANT: Check how the API expects filters (e.g., 'query', 'line', etc.)
        params['query'] = query_filter # Example parameter

    try:
        print(f"Requesting De Lijn disruptions: {endpoint} with params {params}")
        response = requests.get(endpoint, headers=headers, params=params, timeout=15) # 15-second timeout
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        data = response.json()
        # IMPORTANT: Inspect the actual API response structure from De Lijn documentation
        # The keys 'interruptions' and 'detours' are illustrative examples.
        disruptions_list = data.get("interruptions", []) + data.get("detours", [])

        if disruptions_list:
            # IMPORTANT: Adapt formatting based on the actual data fields provided by the API
            # Example: Extracting 'type' and 'details'
            formatted_disruptions = [
                f"{d.get('type', 'Disruption')}: {d.get('details', 'No specific details provided')}" 
                for d in disruptions_list
            ]
            print(f"Found {len(formatted_disruptions)} disruptions.")
            return { "status": "success", "disruptions": formatted_disruptions }
        else:
            print("No disruptions reported matching the query.")
            message = "No current disruptions reported for Gent."
            if query_filter:
                message = f"No current disruptions reported for Gent matching filter: '{query_filter}'."
            return { "status": "success", "disruptions": [], "message": message }

    except requests.exceptions.Timeout:
        print("Error: Request to De Lijn API timed out.")
        return { "status": "error", "error_message": "The request to the De Lijn transport API timed out." }, 504 # Gateway Timeout

    except requests.exceptions.HTTPError as e:
        error_message = f"De Lijn API request failed: Status {e.response.status_code}, Response: {e.response.text[:500]}"
        print(f"Error: {error_message}")
        status_code = e.response.status_code
        user_message = f"Could not retrieve disruption data from De Lijn (Error {status_code})."
        if status_code == 401 or status_code == 403:
            user_message = "Authentication failed with the De Lijn API. Please check the configured API key."
        elif status_code == 429:
            user_message = "Rate limit exceeded for the De Lijn API. Please try again later."
        elif status_code >= 500:
             user_message = "The De Lijn API seems to be having temporary issues. Please try again later."
        
        return { "status": "error", "error_message": user_message }, status_code

    except requests.exceptions.RequestException as e:
        # Catch connection errors, DNS errors, etc.
        print(f"Error: Could not connect to De Lijn API: {e}")
        return { "status": "error", "error_message": "Could not connect to the De Lijn transport API." }, 502 # Bad Gateway
    
    except Exception as e:
        # Catch any other unexpected errors (e.g., JSON decoding errors, logic errors)
        print(f"Unexpected error in get_transport_disruptions: {str(e)}")
        return { "status": "error", "error_message": f"An unexpected internal error occurred while fetching disruption data." }, 500

@functions_framework.http
def get_transport_schedule(request):
    """HTTP Cloud Function to get transport schedules from De Lijn API."""
    if not DE_LIJN_API_KEY:
        print("Error: DE_LIJN_API_KEY environment variable not set.")
        return {"status": "error", "error_message": "API key is not configured on the server."}, 500

    request_json = request.get_json(silent=True)
    
    # --- Parameter Extraction --- 
    # IMPORTANT: Determine required parameters from De Lijn API docs.
    # Examples: stop_id, stop_name, line_number, direction, time_window
    stop_identifier = None 
    line_filter = None
    time_query = None # e.g., 'next', '14:30'

    if request.args:
        stop_identifier = request.args.get('stop') # Example: could be ID or name
        line_filter = request.args.get('line')
        time_query = request.args.get('time')
    elif request_json:
        stop_identifier = request_json.get('stop')
        line_filter = request_json.get('line')
        time_query = request_json.get('time')

    if not stop_identifier:
        return ("Missing required parameter 'stop' (stop ID or name) in request.", 400)

    # --- API Call Construction --- 
    headers = {
        "Ocp-Apim-Subscription-Key": DE_LIJN_API_KEY
    }
    # IMPORTANT: Verify the correct endpoint and parameters in De Lijn documentation
    # Examples: /stops/{stop_id}/realtime, /lines/{line_id}/stops/{stop_id}/schedule
    endpoint = f"{DE_LIJN_API_BASE_URL}/schedule" # Placeholder endpoint
    params = {
        # IMPORTANT: Map extracted parameters to API query params based on De Lijn docs
        "stopIdentifier": stop_identifier, 
        # "queryTime": time_query, # Example
        # "lineNumber": line_filter, # Example
        "area": "Gent" # Example filter
    }
    if line_filter:
        params['lineFilter'] = line_filter # Example
    if time_query:
        params['timeQuery'] = time_query # Example

    # --- API Call and Response Handling --- 
    try:
        print(f"Requesting De Lijn schedule: {endpoint} with params {params}")
        response = requests.get(endpoint, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        # IMPORTANT: Inspect the actual API response structure from De Lijn docs.
        # Extract relevant schedule info (e.g., upcoming departures, times, line numbers)
        schedule_info = data.get("departures", []) # Example key

        if schedule_info:
             # IMPORTANT: Format the schedule based on the actual data fields.
            formatted_schedule = [
                f"Line {dep.get('line', '?')} at {dep.get('time', '?')} towards {dep.get('direction', '?')}" 
                for dep in schedule_info
            ] # Example formatting
            print(f"Found {len(formatted_schedule)} schedule entries.")
            return { "status": "success", "schedule": formatted_schedule }
        else:
            print("No schedule information found for the query.")
            return { "status": "success", "schedule": [], "message": "No schedule information found matching your query." }

    # --- Error Handling (similar to disruptions) ---
    except requests.exceptions.Timeout:
        print("Error: Request to De Lijn API timed out.")
        return { "status": "error", "error_message": "The request to the De Lijn schedule API timed out." }, 504
    except requests.exceptions.HTTPError as e:
        error_message = f"De Lijn API request failed: Status {e.response.status_code}, Response: {e.response.text[:500]}"
        print(f"Error: {error_message}")
        status_code = e.response.status_code
        user_message = f"Could not retrieve schedule data from De Lijn (Error {status_code})."
        # Add specific messages based on status code if needed (401, 403, 429, 5xx)
        return { "status": "error", "error_message": user_message }, status_code
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not connect to De Lijn API: {e}")
        return { "status": "error", "error_message": "Could not connect to the De Lijn schedule API." }, 502
    except Exception as e:
        print(f"Unexpected error in get_transport_schedule: {str(e)}")
        return { "status": "error", "error_message": f"An unexpected internal error occurred while fetching schedule data." }, 500
