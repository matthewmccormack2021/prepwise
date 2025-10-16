"""
Structured response models for consistent API responses.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class InterviewResponse(BaseModel):
    """Structured response model for interview interactions."""
    
    question_type: str = Field(..., description="Type of question (introduction, behavioral, technical)")
    question: str = Field(..., description="The question or response content")
    evaluation_criteria: Optional[List[str]] = Field(None, description="Criteria for evaluating the answer")
    follow_up_suggestions: Optional[List[str]] = Field(None, description="Suggested follow-up questions")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ChatResponse(BaseModel):
    """Standardized chat response model."""
    
    status: str = Field(..., description="Response status (success, error)")
    service: str = Field(default="backend", description="Service name")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    query: str = Field(..., description="Original user query")
    response: str = Field(..., description="Agent response content")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")
    conversation_length: Optional[int] = Field(None, description="Number of messages in conversation")
    error: Optional[str] = Field(None, description="Error message if status is error")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional response metadata")


class JobScrapeResponse(BaseModel):
    """Response model for job scraping operations."""
    
    status: str = Field(..., description="Response status (success, error)")
    service: str = Field(default="backend", description="Service name")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    url: str = Field(..., description="Scraped URL")
    job_info: Optional[Dict[str, Any]] = Field(None, description="Extracted job information")
    error: Optional[str] = Field(None, description="Error message if status is error")


class HealthResponse(BaseModel):
    """Health check response model."""
    
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    timestamp: datetime = Field(default_factory=datetime.now, description="Check timestamp")
    version: Optional[str] = Field(None, description="Service version")
    dependencies: Optional[Dict[str, str]] = Field(None, description="Dependency status")
