import os
import requests
from dotenv import load_dotenv
from google.adk.agent import Agent
from google.adk.tools import FunctionTool

# Load environment variables from .env file
load_dotenv()

# --- Cloud Function URLs ---
# Replace these URLs with actual deployed Cloud Function URLs
QUERY_KB_URL = os.environ.get("QUERY_KB_FUNCTION_URL", "https://us-central1-YOUR_PROJECT.cloudfunctions.net/query_gent_services_kb")
TRANSPORT_DISRUPTION_URL = os.environ.get("TRANSPORT_DISRUPTION_FUNCTION_URL", "https://us-central1-YOUR_PROJECT.cloudfunctions.net/get_transport_disruptions")
TRANSPORT_SCHEDULE_URL = os.environ.get("TRANSPORT_SCHEDULE_FUNCTION_URL", "https://us-central1-YOUR_PROJECT.cloudfunctions.net/get_transport_schedule")

# --- Tool Function Definitions ---
def query_gent_knowledge_base_tool(query: str) -> dict:
    """Queries the internal knowledge base about City of Gent services.
    Use this tool to find information about city services, regulations, opening hours, 
    waste collection schedules, permit processes, library info, etc. for Gent.
    
    Args:
        query: The specific question about Gent city services.
        
    Returns:
        A dictionary containing the status and the retrieved information, or an error message.
    """
    try:
        response = requests.post(QUERY_KB_URL, json={'query': query}, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling knowledge base tool: {e}")
        return {"status": "error", "error_message": f"Failed to query knowledge base: {str(e)}"}
    except Exception as e:
        print(f"Unexpected error in knowledge base tool: {e}")
        return {"status": "error", "error_message": "An unexpected error occurred while querying the knowledge base."}

def get_transport_disruptions_tool(filter: str | None = None) -> dict:
    """Checks for current public transport disruptions in Gent (strikes, delays, route changes) using the De Lijn API.
    Use this tool ONLY to find out if there are known PROBLEMS or ISSUES with buses or trams in Gent right now.
    Do NOT use for regular schedule times.
    
    Args:
        filter (Optional[str]): A specific filter for the query (e.g., 'line 1', 'strike').
        
    Returns:
        A dictionary containing the status and a list of current disruptions, or an error message.
    """
    payload = {'filter': filter} if filter else {}
    try:
        response = requests.post(TRANSPORT_DISRUPTION_URL, json=payload, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling disruptions tool: {e}")
        try: 
            error_details = e.response.json()
        except: 
            error_details = None
        if isinstance(error_details, dict) and "error_message" in error_details: 
            return {"status": "error", "error_message": error_details['error_message']}
        return {"status": "error", "error_message": f"Failed to contact the transport disruption service: {str(e)}"}
    except Exception as e:
        print(f"Unexpected error in disruptions tool: {e}")
        return {"status": "error", "error_message": "An unexpected error occurred while checking transport disruptions."}

def get_transport_schedule_tool(stop_id: str | None = None, line_number: str | None = None) -> dict:
    """Fetches REGULAR public transport schedule information (like next departure times) for a specific stop or line in Gent using the De Lijn API.
    Use this tool for standard timetable queries. Do NOT use for disruption information.
    
    Args:
        stop_id (Optional[str]): The ID of the bus/tram stop. Provide EITHER stop_id OR line_number.
        line_number (Optional[str]): The number of the bus/tram line. Provide EITHER stop_id OR line_number.
        
    Returns:
        A dictionary containing the status and schedule information, or an error message.
    """
    payload = {}
    if stop_id:
        payload['stop_id'] = stop_id
    if line_number:
        payload['line_number'] = line_number
    if not payload:
        return {"status": "error", "error_message": "You must provide either a stop_id or a line_number."}
        
    try:
        response = requests.post(TRANSPORT_SCHEDULE_URL, json=payload, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling schedule tool: {e}")
        try: 
            error_details = e.response.json()
        except: 
            error_details = None
        if isinstance(error_details, dict) and "error_message" in error_details: 
            return {"status": "error", "error_message": error_details['error_message']}
        return {"status": "error", "error_message": f"Failed to contact the transport schedule service: {str(e)}"}
    except Exception as e:
        print(f"Unexpected error in schedule tool: {e}")
        return {"status": "error", "error_message": "An unexpected error occurred while fetching the transport schedule."}

# --- Convert Python functions into ADK FunctionTool objects ---
tool_query_kb = FunctionTool(
    fn=query_gent_knowledge_base_tool,
    description="Look up information about Gent city services, procedures, and schedules."
)

tool_transport_disruptions = FunctionTool(
    fn=get_transport_disruptions_tool,
    description="Check for current public transport DISRUPTIONS (strikes, delays, issues) in Gent using the official De Lijn API."
)

tool_transport_schedule = FunctionTool(
    fn=get_transport_schedule_tool,
    description="Get REGULAR public transport schedule times (e.g., next departures) for a specific stop or line in Gent using the official De Lijn API."
)

# --- Define the Agent ---
agent = Agent(
    name="Gent City Assistant",
    description="An AI assistant providing information on City of Gent services, current public transport disruptions, and regular transport schedules via De Lijn.",
    instructions=[
        "You are a helpful assistant for residents and visitors of Gent, Belgium.",
        "Use the 'query_gent_knowledge_base_tool' to answer questions about city services like opening hours, waste collection, permits, etc.",
        "Use the 'get_transport_disruptions_tool' ONLY to check for current PROBLEMS like strikes, delays, or route changes affecting buses and trams in Gent.",
        "Use the 'get_transport_schedule_tool' ONLY to find REGULAR schedule times or next departures for a specific stop or line.",
        "Carefully choose between the disruption tool and the schedule tool based on the user's query.",
        "Inform the user if you need to check with De Lijn for disruption or schedule information.",
        "If a tool returns an error, inform the user you couldn't retrieve the information and mention the source (e.g., 'De Lijn API').",
        "If you don't know the answer or the tools don't provide it, say so clearly.",
        "Be polite and concise."
    ],
    model="gemini-1.5-pro-001",  # Specify the LLM model
    tools=[tool_query_kb, tool_transport_disruptions, tool_transport_schedule]  # List all three tools
)

# --- Agent Interaction Loop ---
def main():
    print("--- Gent City Assistant ---")
    print("Ask about Gent city services, transport disruptions, or schedules.")
    print("Type 'quit' or 'exit' to end the session.")
    
    # Check if URLs are placeholders
    missing_url = False
    for url_name, url_value in [
        ("QUERY_KB_URL", QUERY_KB_URL), 
        ("TRANSPORT_DISRUPTION_URL", TRANSPORT_DISRUPTION_URL), 
        ("TRANSPORT_SCHEDULE_URL", TRANSPORT_SCHEDULE_URL)
    ]:
        if "YOUR_PROJECT" in url_value:
            print(f"⚠️  Warning: {url_name} is still a placeholder. Tool calls will fail.")
            missing_url = True
    
    if missing_url:
        print("\nPlease deploy the Cloud Functions and update the URLs in .env or agent.py\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        if not user_input:
            continue
            
        try:
            response = agent.generate_content(user_input)
            if response and response.parts:
                final_text = "".join(part.text for part in response.parts if hasattr(part, 'text'))
                print(f"Agent: {final_text}")
            else:
                print("Agent: I'm sorry, I couldn't generate a response for that.")
        except Exception as e:
            print(f"Agent Error: An error occurred during processing: {e}")
            print("Agent: I encountered an issue processing your request. Please try again.")

if __name__ == "__main__":
    main()
