import os
from strands import Agent, tool
from strands.models.ollama import OllamaModel
from strands.multiagent import GraphBuilder
# Define a specialized system prompt

# Get Ollama host from environment variable, default to host.docker.internal for Docker
ollama_host = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")

# Create an Ollama model instance
ollama_model = OllamaModel(
    host=ollama_host,  # Ollama server address
    model_id="llama3.2"               # Specify which model to use
)

INTRODUCTION_ASSISTANT_PROMPT = """
You are a specialized introduction assistant. You are responsible for starting the interview with a user for the given role and introducing yourself to the user.
"""

@tool
def introduction_assistant(user_input: str) -> str:
    """
    Process and respond to introduction-related queries using streaming to capture all output.

    Args:
        user_input: The last user question or answer

    Returns:
        A detailed introduction response with all reasoning captured
    """
    try:
        # Strands Agents SDK makes it easy to create a specialized agent
        introduction_agent = Agent(model=ollama_model,
            system_prompt=INTRODUCTION_ASSISTANT_PROMPT,
            callback_handler=None  # Disable default callback to capture ourselves
        )

        # Use callback handler to capture all output instead of streaming
        captured_output = []
        
        def capture_callback(**kwargs):
            if "data" in kwargs:
                captured_output.append(kwargs["data"])
            elif "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
                captured_output.append(f"\n[Using tool: {kwargs['current_tool_use']['name']}]\n")
        
        # Create agent with callback handler
        intro_agent_with_callback = Agent(
            model=ollama_model,
            system_prompt=INTRODUCTION_ASSISTANT_PROMPT,
            callback_handler=capture_callback
        )
        
        # Call the agent - callback will capture output
        result = intro_agent_with_callback(user_input)
        
        # Return captured output if available, otherwise fallback to result
        if captured_output:
            return "".join(captured_output)
        else:
            return str(result.message) if hasattr(result, 'message') else str(result)
    except Exception as e:
        return f"Error in introduction assistant: {str(e)}"

BEHAVIORAL_QUESTION_GENERATOR_PROMPT = """
You are a specialized behavioral question assistant. You are responsible for generating a behavioral question for the user.
"""

@tool
def behavioral_question_generator(user_input: str) -> str:
    """
    Process and respond to behavioral question queries using streaming to capture all output.

    Args:
        user_input: The last user question or answer

    Returns:
        A detailed behavioral question response with all reasoning captured
    """
    try:
        # Strands Agents SDK makes it easy to create a specialized agent
        behavioral_question_agent = Agent(model=ollama_model,
            system_prompt=BEHAVIORAL_QUESTION_GENERATOR_PROMPT,
            callback_handler=None  # Disable default callback to capture ourselves
        )

        # Use callback handler to capture all output instead of streaming
        captured_output = []
        
        def capture_callback(**kwargs):
            if "data" in kwargs:
                captured_output.append(kwargs["data"])
            elif "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
                captured_output.append(f"\n[Using tool: {kwargs['current_tool_use']['name']}]\n")
        
        # Create agent with callback handler
        behavioral_agent_with_callback = Agent(
            model=ollama_model,
            system_prompt=BEHAVIORAL_QUESTION_GENERATOR_PROMPT,
            callback_handler=capture_callback
        )
        
        # Call the agent - callback will capture output
        result = behavioral_agent_with_callback(user_input)
        
        # Return captured output if available, otherwise fallback to result
        if captured_output:
            return "".join(captured_output)
        else:
            return str(result.message) if hasattr(result, 'message') else str(result)
    except Exception as e:
        return f"Error in behavioral question assistant: {str(e)}"

BEHAVIORAL_QUESTION_EVALUATOR_PROMPT = """
You are a specialized behavioral question assistant. You are responsible for assessing the users answer to a behavioral question.
"""

@tool
def behavioral_question_evaluator(user_input: str) -> str:
    """
    Process and respond to behavioral question queries using streaming to capture all output.

    Args:
        user_input: The last user question or answer

    Returns:
        A detailed behavioral question response with all reasoning captured
    """
    try:
        # Strands Agents SDK makes it easy to create a specialized agent
        behavioral_question_agent = Agent(model=ollama_model,
            system_prompt=BEHAVIORAL_QUESTION_EVALUATOR_PROMPT,
            callback_handler=None  # Disable default callback to capture ourselves
        )

        # Use callback handler to capture all output instead of streaming
        captured_output = []
        
        def capture_callback(**kwargs):
            if "data" in kwargs:
                captured_output.append(kwargs["data"])
            elif "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
                captured_output.append(f"\n[Using tool: {kwargs['current_tool_use']['name']}]\n")
        
        # Create agent with callback handler
        behavioral_agent_with_callback = Agent(
            model=ollama_model,
            system_prompt=BEHAVIORAL_QUESTION_EVALUATOR_PROMPT,
            callback_handler=capture_callback
        )
        
        # Call the agent - callback will capture output
        result = behavioral_agent_with_callback(user_input)
        
        # Return captured output if available, otherwise fallback to result
        if captured_output:
            return "".join(captured_output)
        else:
            return str(result.message) if hasattr(result, 'message') else str(result)
    except Exception as e:
        return f"Error in behavioral question assistant: {str(e)}"

TECHNICAL_QUESTION_GENERATOR_PROMPT = """
You are a specialized technical question assistant. You are responsible for generating a technical question.
"""

@tool
def technical_question_generator(user_input: str) -> str:
    """
    Process and respond to technical question queries using streaming to capture all output.

    Args:
        user_input: The last user question or answer

    Returns:
        A detailed technical question response with all reasoning captured
    """
    try:
        # Strands Agents SDK makes it easy to create a specialized agent
        technical_question_agent = Agent(model=ollama_model,
            system_prompt=TECHNICAL_QUESTION_GENERATOR_PROMPT,
            callback_handler=None  # Disable default callback to capture ourselves
        )

        # Use callback handler to capture all output instead of streaming
        captured_output = []
        
        def capture_callback(**kwargs):
            if "data" in kwargs:
                captured_output.append(kwargs["data"])
            elif "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
                captured_output.append(f"\n[Using tool: {kwargs['current_tool_use']['name']}]\n")
        
        # Create agent with callback handler
        technical_agent_with_callback = Agent(
            model=ollama_model,
            system_prompt=TECHNICAL_QUESTION_GENERATOR_PROMPT,
            callback_handler=capture_callback
        )
        
        # Call the agent - callback will capture output
        result = technical_agent_with_callback(user_input)
        
        # Return captured output if available, otherwise fallback to result
        if captured_output:
            return "".join(captured_output)
        else:
            return str(result.message) if hasattr(result, 'message') else str(result)
    except Exception as e:
        return f"Error in technical question assistant: {str(e)}"

TECHNICAL_QUESTION_EVALUATOR_PROMPT = """
You are a specialized technical question assistant. You are responsible for assessing the users answer to a technical question.
"""

@tool
def technical_question_evaluator(user_input: str) -> str:
    """
    Process and respond to technical question queries using streaming to capture all output.

    Args:
        user_input: The last user question or answer

    Returns:
        A detailed technical question response with all reasoning captured
    """
    try:
        # Strands Agents SDK makes it easy to create a specialized agent
        technical_question_agent = Agent(model=ollama_model,
            system_prompt=TECHNICAL_QUESTION_EVALUATOR_PROMPT,
            callback_handler=None  # Disable default callback to capture ourselves
        )

        # Use callback handler to capture all output instead of streaming
        captured_output = []
        
        def capture_callback(**kwargs):
            if "data" in kwargs:
                captured_output.append(kwargs["data"])
            elif "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
                captured_output.append(f"\n[Using tool: {kwargs['current_tool_use']['name']}]\n")
        
        # Create agent with callback handler
        technical_agent_with_callback = Agent(
            model=ollama_model,
            system_prompt=TECHNICAL_QUESTION_EVALUATOR_PROMPT,
            callback_handler=capture_callback
        )
        
        # Call the agent - callback will capture output
        result = technical_agent_with_callback(user_input)
        
        # Return captured output if available, otherwise fallback to result
        if captured_output:
            return "".join(captured_output)
        else:
            return str(result.message) if hasattr(result, 'message') else str(result)
    except Exception as e:
        return f"Error in technical question assistant: {str(e)}"