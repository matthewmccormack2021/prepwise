"""FastAPI backend service for PrepWise agentic system."""

import os
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from loguru import logger

from app.agents.orchestrator import orchestrator
from app.services.web_scraper import scrape_job_posting

class ChatRequest(BaseModel):
    query: str

class ScrapeRequest(BaseModel):
    url: str

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
        
        # Call the agent - callback will capture output
        result = orchestrator(request.query)
        
        # Return captured output if available, otherwise fallback to result
        if captured_output:
            full_response = "".join(captured_output)
        else:
            # Properly extract message content from Strands Agent result
            if hasattr(result, 'message'):
                if hasattr(result.message, 'content'):
                    # Handle different content formats
                    content = result.message.content
                    if isinstance(content, list) and len(content) > 0:
                        # Extract text from content list
                        if hasattr(content[0], 'text'):
                            full_response = content[0].text
                        else:
                            full_response = str(content[0])
                    elif isinstance(content, str):
                        full_response = content
                    else:
                        full_response = str(content)
                else:
                    full_response = str(result.message)
            else:
                full_response = str(result)
        
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

@app.post("/scrape-job")
async def scrape_job(request: ScrapeRequest):
    """Scrape job information from a job posting URL."""
    try:
        logger.info(f"Scraping job posting from URL: {request.url}")
        
        # Scrape the job posting
        job_info = scrape_job_posting(request.url)
        
        if 'error' in job_info:
            return {
                "status": "error",
                "service": "backend",
                "timestamp": datetime.now().isoformat(),
                "url": request.url,
                "error": job_info['error']
            }
        
        return {
            "status": "success",
            "service": "backend",
            "timestamp": datetime.now().isoformat(),
            "url": request.url,
            "job_info": job_info
        }
        
    except Exception as e:
        logger.error(f"Error in scrape-job endpoint: {str(e)}")
        return {
            "status": "error",
            "service": "backend", 
            "timestamp": datetime.now().isoformat(),
            "url": request.url,
            "error": str(e),
            "message": "Failed to scrape job posting"
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
