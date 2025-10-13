"""FastAPI backend service for PrepWise agentic system."""

import os
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from loguru import logger

from app.agents.orchestrator import orchestrator

class ChatRequest(BaseModel):
    query: str

# Configure logging
logger.remove()
logger.add("logs/backend.log", rotation="1 day", retention="7 days", level="INFO")
logger.add(lambda msg: print(msg, end=""), level="INFO")

app = FastAPI(
    title="PrepWise Backend Service",
    description="FastAPI backend for PrepWise AI interview practice platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "PrepWise Backend Service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "start_interview": "/api/interview/start",
            "generate_question": "/api/interview/question",
            "submit_answer": "/api/interview/answer",
            "end_interview": "/api/interview/end"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "backend",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/chat")
async def chat(request: ChatRequest):
    """Chat endpoint with the agent using callback handler to capture all output."""
    try:
        # Use callback handler to capture all agent output including reasoning and tool usage
        captured_output = []
        
        def capture_callback(**kwargs):
            if "data" in kwargs:
                captured_output.append(kwargs["data"])
            elif "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
                captured_output.append(f"\n[Using tool: {kwargs['current_tool_use']['name']}]\n")
        
        # Create orchestrator with callback handler
        from app.agents.orchestrator import ollama_model, MAIN_SYSTEM_PROMPT
        from app.agents.specialized_agents import introduction_assistant, behavioral_question_assistant, technical_question_assistant
        from strands import Agent
        
        orchestrator_with_callback = Agent(
            model=ollama_model,
            system_prompt=MAIN_SYSTEM_PROMPT,
            callback_handler=capture_callback,
            tools=[introduction_assistant, behavioral_question_assistant, technical_question_assistant]
        )
        
        # Call the agent - callback will capture output
        result = orchestrator_with_callback(request.query)
        
        # Return captured output if available, otherwise fallback to result
        if captured_output:
            full_response = "".join(captured_output)
        else:
            full_response = str(result.message) if hasattr(result, 'message') else str(result)
        
        # Return the complete agent response along with metadata
        return {
            "status": "success",
            "service": "backend",
            "timestamp": datetime.now().isoformat(),
            "query": request.query,
            "response": full_response
        }
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return {
            "status": "error",
            "service": "backend", 
            "timestamp": datetime.now().isoformat(),
            "query": request.query,
            "error": str(e),
            "message": "Failed to process chat request. Please ensure Ollama server is running on localhost:11434"
        }

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )
