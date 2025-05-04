import os,dotenv
import sqlite3
import pandas as pd
import json
import uuid
# --- ADK Core Imports ---
from google.adk.agents import Agent, BaseAgent, LlmAgent
from google.adk.tools import FunctionTool, ToolContext
from google.adk.tools.agent_tool import AgentTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

dotenv.load_dotenv()

MODEL_NAME = "gemini-2.5-flash-preview-04-17"#Use one of these: gemini-2.5-pro-exp-03-25, gemini-2.5-flash-preview-04-17, gemini-2.5-pro-preview-03-25
APP_NAME = "data_query_app"
USER_ID = "user_1"

def sql_tool_function(query: str):
    """This function takes in an SQL query and runs it against the database"""
    pass

# 1. Data Agent
data_agent = Agent(
    name="DataAgent",
    model=MODEL_NAME,
    description=f"",
    instruction=f"""
""",
    tools=[FunctionTool(sql_tool_function)]
)

# 2. Primary Agent
primary_agent = Agent(
    name="PrimaryAgent",
    model=MODEL_NAME,
    description="",
    instruction=f"""

""",
    tools=[AgentTool(agent=data_agent)],
    output_key="primary_agent_final_response"
)



# --- Runtime Setup ---
session_service = InMemorySessionService()
runner = Runner(
    agent=primary_agent, # Start with the Primary Agent
    app_name=APP_NAME,
    session_service=session_service
)

# Generate a unique session ID for this run
session_id = f"session_{uuid.uuid4()}"

# Create the session
session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=session_id
)
print(f"\nSession created with ID: {session_id}")

# --- Interaction Logic ---
def run_query(query: str):
    """Helper function to run a query against the primary agent."""
    print(f"\n>>> User Query: {query}")
    content = genai_types.Content(role='user', parts=[genai_types.Part(text=query)])
    final_response_text = "Agent did not produce a final response."


    events = runner.run(user_id=USER_ID, session_id=session_id, new_message=content)

    for event in events:
         
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text.strip()

            break # Stop after the first final response

    print(f"<<< PrimaryAgent Response: {final_response_text}")

    # Inspect final state
    final_session = session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
    print("--- Final Session State ---")
    print(json.dumps(final_session.state, indent=2))
    print("-" * 30)

# --- Main Execution ---
if __name__ == "__main__":

    #test query
    run_query("what is the capital of France?")

    #final evaluation queries
    # run_query("Which company has the highest revenue?")
    # run_query("What is the market cap of AAPL?")
    # run_query("What are all the different countries represented in the data?")
    # run_query("How many companies are represented in the data?")
    # run_query("NVDA and AVGO are competitors. What is the difference in revenue between them?")

