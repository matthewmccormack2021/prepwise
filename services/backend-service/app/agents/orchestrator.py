"""
Main orchestrator agent for coordinating interview workflows.
"""

import os
import uuid
from strands import Agent
from strands.models.ollama import OllamaModel
from .session_manager import SessionService, AgentFactory
from .workflow_tools import behavioral_workflow, technical_workflow
from .specialized_agents import introduction_assistant
from ..config import config

# Create an Ollama model instance using config
ollama_model = OllamaModel(
    host=config.get_ollama_host(),  # Ollama server address
    model_id=config.get_ollama_model()  # Specify which model to use
)

# Initialize session service and agent factory
session_service = SessionService()
agent_factory = AgentFactory(ollama_model, session_service)

# Define the orchestrator system prompt with clear tool selection guidance
MAIN_SYSTEM_PROMPT = """
You are an experienced interviewer that uses specialized agents and workflows to conduct comprehensive interviews:
- For starting the interview and general introduction → Use the introduction_assistant tool
- For behavioral questions and evaluations → Use the behavioral_workflow tool
- For technical questions and evaluations → Use the technical_workflow tool
- For simple questions not requiring specialized knowledge → Answer directly

When a user answers a question, provide thoughtful feedback and respond with another question that builds naturally from their answer. Always maintain conversation flow and context.

Always select the most appropriate tool based on the user's query and interview progress.
"""


def create_orchestrator(session_id: str = None) -> Agent:
    """
    Create an orchestrator agent with proper session management.
    
    Args:
        session_id: Optional session ID for conversation persistence
        
    Returns:
        Configured Agent instance
    """
    if session_id is None:
        session_id = f"session_{uuid.uuid4().hex[:8]}"
    
    session_manager = session_service.get_session_manager(session_id)
    conversation_manager = session_service.get_conversation_manager()
    
    return Agent(
        model=ollama_model,
        system_prompt=MAIN_SYSTEM_PROMPT,
        session_manager=session_manager,
        conversation_manager=conversation_manager,
        tools=[
            introduction_assistant, 
            behavioral_workflow, 
            technical_workflow
        ]
    )


# Create default orchestrator for backward compatibility
orchestrator = create_orchestrator()