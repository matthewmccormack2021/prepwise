"""Shared models and enums for PrepWise application."""

from enum import Enum
from typing import Optional, List
from pydantic import BaseModel

class InterviewPosition(str, Enum):
    """Available interview positions."""
    SOFTWARE_ENGINEER = "software_engineer"
    DATA_SCIENTIST = "data_scientist"
    PRODUCT_MANAGER = "product_manager"
    DESIGNER = "designer"
    MARKETING_MANAGER = "marketing_manager"

class QuestionType(str, Enum):
    """Types of interview questions."""
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"
    SITUATIONAL = "situational"

class InterviewerPersonality(str, Enum):
    """Interviewer personality types."""
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"
    CHALLENGING = "challenging"

class UserProfile(BaseModel):
    """User profile information."""
    id: str
    name: str
    email: Optional[str] = None
    target_positions: List[InterviewPosition] = []
    experience_level: str = "entry"
    preferred_question_types: List[QuestionType] = []

class InterviewRequest(BaseModel):
    """Request to start an interview."""
    position: InterviewPosition
    personality: InterviewerPersonality
    question_type: Optional[QuestionType] = None
    difficulty: Optional[str] = None
    user_profile: Optional[UserProfile] = None
