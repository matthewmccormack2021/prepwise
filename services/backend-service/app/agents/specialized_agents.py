"""
Specialized interview agents using the AgentFactory pattern.
"""

import os
from strands import tool
from strands.models.ollama import OllamaModel
from .session_manager import AgentFactory, SessionService
from ..config import config


# Create an Ollama model instance using config
ollama_model = OllamaModel(
    host=config.get_ollama_host(),  # Ollama server address
    model_id=config.get_ollama_model()  # Specify which model to use
)

# Initialize session service and agent factory
session_service = SessionService()
agent_factory = AgentFactory(ollama_model, session_service)

INTRODUCTION_ASSISTANT_PROMPT = """
You are a specialized introduction assistant. You are responsible for starting the interview with a user for the given role and introducing yourself to the user.
"""

@tool
def introduction_assistant(user_input: str, session_id: str = "default") -> str:
    """
    Process and respond to introduction-related queries using efficient agent management.

    Args:
        user_input: The user's input or response
        session_id: Session ID for conversation persistence

    Returns:
        A detailed introduction response with conversation context
    """
    try:
        agent = agent_factory.create_agent(
            agent_type="introduction",
            system_prompt=INTRODUCTION_ASSISTANT_PROMPT,
            session_id=session_id
        )
        
        result = agent(user_input)
        
        # Handle different result formats
        if hasattr(result, 'message') and hasattr(result.message, 'content'):
            return result.message.content
        elif hasattr(result, 'content'):
            return result.content
        elif isinstance(result, dict) and 'content' in result:
            return result['content']
        elif isinstance(result, str):
            return result
        else:
            return str(result)
    except Exception as e:
        return f"Error in introduction assistant: {str(e)}"

BEHAVIORAL_QUESTION_GENERATOR_PROMPT = """
You are a specialized behavioral question assistant. You are responsible for generating a behavioral question for the user.
"""

@tool
def behavioral_question_generator(user_input: str, session_id: str = "default") -> str:
    """
    Process and respond to behavioral question queries using efficient agent management.

    Args:
        user_input: The user's input or response
        session_id: Session ID for conversation persistence

    Returns:
        A detailed behavioral question response with conversation context
    """
    try:
        agent = agent_factory.create_agent(
            agent_type="behavioral_generator",
            system_prompt=BEHAVIORAL_QUESTION_GENERATOR_PROMPT,
            session_id=session_id
        )
        
        result = agent(user_input)
        
        # Handle different result formats
        if hasattr(result, 'message') and hasattr(result.message, 'content'):
            return result.message.content
        elif hasattr(result, 'content'):
            return result.content
        elif isinstance(result, dict) and 'content' in result:
            return result['content']
        elif isinstance(result, str):
            return result
        else:
            return str(result)
    except Exception as e:
        return f"Error in behavioral question generator: {str(e)}"

BEHAVIORAL_QUESTION_EVALUATOR_PROMPT = """
You are a specialized behavioral question assistant. You are responsible for assessing the users answer to a behavioral question.
"""

@tool
def behavioral_question_evaluator(user_input: str, session_id: str = "default") -> str:
    """
    Process and respond to behavioral question evaluation using efficient agent management.

    Args:
        user_input: The user's answer to evaluate
        session_id: Session ID for conversation persistence

    Returns:
        A detailed evaluation response with conversation context
    """
    try:
        agent = agent_factory.create_agent(
            agent_type="behavioral_evaluator",
            system_prompt=BEHAVIORAL_QUESTION_EVALUATOR_PROMPT,
            session_id=session_id
        )
        
        result = agent(user_input)
        
        # Handle different result formats
        if hasattr(result, 'message') and hasattr(result.message, 'content'):
            return result.message.content
        elif hasattr(result, 'content'):
            return result.content
        elif isinstance(result, dict) and 'content' in result:
            return result['content']
        elif isinstance(result, str):
            return result
        else:
            return str(result)
    except Exception as e:
        return f"Error in behavioral question evaluator: {str(e)}"

TECHNICAL_QUESTION_GENERATOR_PROMPT = """
You are a specialized technical question assistant. You are responsible for generating a technical question.
"""

@tool
def technical_question_generator(user_input: str, session_id: str = "default") -> str:
    """
    Process and respond to technical question queries using efficient agent management.

    Args:
        user_input: The user's input or response
        session_id: Session ID for conversation persistence

    Returns:
        A detailed technical question response with conversation context
    """
    try:
        agent = agent_factory.create_agent(
            agent_type="technical_generator",
            system_prompt=TECHNICAL_QUESTION_GENERATOR_PROMPT,
            session_id=session_id
        )
        
        result = agent(user_input)
        
        # Handle different result formats
        if hasattr(result, 'message') and hasattr(result.message, 'content'):
            return result.message.content
        elif hasattr(result, 'content'):
            return result.content
        elif isinstance(result, dict) and 'content' in result:
            return result['content']
        elif isinstance(result, str):
            return result
        else:
            return str(result)
    except Exception as e:
        return f"Error in technical question generator: {str(e)}"

TECHNICAL_QUESTION_EVALUATOR_PROMPT = """
You are a specialized technical question assistant. You are responsible for assessing the users answer to a technical question.
"""

@tool
def technical_question_evaluator(user_input: str, session_id: str = "default") -> str:
    """
    Process and respond to technical question evaluation using efficient agent management.

    Args:
        user_input: The user's answer to evaluate
        session_id: Session ID for conversation persistence

    Returns:
        A detailed evaluation response with conversation context
    """
    try:
        agent = agent_factory.create_agent(
            agent_type="technical_evaluator",
            system_prompt=TECHNICAL_QUESTION_EVALUATOR_PROMPT,
            session_id=session_id
        )
        
        result = agent(user_input)
        
        # Handle different result formats
        if hasattr(result, 'message') and hasattr(result.message, 'content'):
            return result.message.content
        elif hasattr(result, 'content'):
            return result.content
        elif isinstance(result, dict) and 'content' in result:
            return result['content']
        elif isinstance(result, str):
            return result
        else:
            return str(result)
    except Exception as e:
        return f"Error in technical question evaluator: {str(e)}"