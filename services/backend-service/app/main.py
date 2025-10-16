"""FastAPI backend service for PrepWise agentic system."""

import os
import uuid
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from loguru import logger

from app.agents.orchestrator import create_orchestrator
from app.services.web_scraper import scrape_job_posting
from app.models.response_models import ChatResponse, JobScrapeResponse, HealthResponse
from app.config import config

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None  # Optional session ID for conversation persistence

class ScrapeRequest(BaseModel):
    url: str

# Configure logging
logger.remove()
logger.add("logs/backend.log", rotation=config.LOG_ROTATION, retention=config.LOG_RETENTION, level=config.LOG_LEVEL)
logger.add(lambda msg: print(msg, end=""), level=config.LOG_LEVEL)

app = FastAPI(
    title="PrepWise Backend Service",
    description="FastAPI backend for PrepWise AI interview practice platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,  # Configure appropriately for production
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

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="backend",
        version="1.0.0"
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint with proper session management and structured responses."""
    try:
        # Generate session ID if not provided
        session_id = request.session_id or f"session_{uuid.uuid4().hex[:8]}"
        
        # Create orchestrator with session management
        orchestrator_agent = create_orchestrator(session_id)
        
        # Process the query
        result = orchestrator_agent(request.query)
        
        # Extract response content - handle different result formats
        if hasattr(result, 'message') and hasattr(result.message, 'content'):
            response_content = result.message.content
        elif hasattr(result, 'content'):
            response_content = result.content
        elif isinstance(result, dict) and 'content' in result:
            response_content = result['content']
        elif isinstance(result, str):
            response_content = result
        else:
            # Fallback: convert result to string
            response_content = str(result)
        
        # Get conversation length for metadata (optional)
        conversation_length = None
        
        return ChatResponse(
            status="success",
            query=request.query,
            response=response_content,
            session_id=session_id,
            conversation_length=conversation_length,
            metadata={
                "model": config.get_ollama_model(),
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return ChatResponse(
            status="error",
            query=request.query,
            response="",
            error=str(e),
            metadata={
                "error_type": type(e).__name__,
                "timestamp": datetime.now().isoformat()
            }
        )

@app.post("/scrape-job", response_model=JobScrapeResponse)
async def scrape_job(request: ScrapeRequest):
    """Scrape job information from a job posting URL."""
    try:
        logger.info(f"Scraping job posting from URL: {request.url}")
        
        # Scrape the job posting
        job_info = scrape_job_posting(request.url)
        
        if 'error' in job_info:
            return JobScrapeResponse(
                status="error",
                url=request.url,
                error=job_info['error']
            )
        
        return JobScrapeResponse(
            status="success",
            url=request.url,
            job_info=job_info
        )
        
    except Exception as e:
        logger.error(f"Error in scrape-job endpoint: {str(e)}")
        return JobScrapeResponse(
            status="error",
            url=request.url,
            error=str(e)
        )

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Run the application
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True,
        log_level=config.LOG_LEVEL.lower()
    )
