import os
from strands import Agent
from strands.models.ollama import OllamaModel
from .specialized_agents import introduction_assistant
from .workflow_tools import behavioral_workflow, technical_workflow

# Get Ollama host from environment variable, default to host.docker.internal for Docker
ollama_host = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")

# Create an Ollama model instance
ollama_model = OllamaModel(
    host=ollama_host,  # Ollama server address
    model_id="llama3.2"               # Specify which model to use
)

# Define the orchestrator system prompt with clear tool selection guidance
MAIN_SYSTEM_PROMPT = """
You are an interviewer that uses specialized agents and workflows to conduct an interview:
- For starting the interview and general introduction → Use the introduction_assistant tool
- For behavioral questions → Use the behavioral_workflow tool (coordinates question generation and evaluation)
- For technical questions → Use the technical_workflow tool (coordinates question generation and evaluation)
- For simple questions not requiring specialized knowledge → Answer directly

The workflow tools execute complete graph-based workflows that coordinate multiple specialized agents:
- behavioral_workflow: Generates and evaluates behavioral interview questions
- technical_workflow: Generates and evaluates technical interview questions

Always select the most appropriate tool based on the user's query.
"""

# Strands Agents SDK allows easy integration of agent tools
orchestrator = Agent(model=ollama_model,
    system_prompt=MAIN_SYSTEM_PROMPT,
    callback_handler=None,  # Disable default callback to capture streaming ourselves
    tools=[introduction_assistant, behavioral_workflow, technical_workflow]
)