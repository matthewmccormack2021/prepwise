"""
Session management and conversation handling for PrepWise agents.
"""

import os
from typing import Optional
from strands import Agent
from strands.session.file_session_manager import FileSessionManager
from strands.agent.conversation_manager import SlidingWindowConversationManager, SummarizingConversationManager
from strands.models.ollama import OllamaModel
from ..config import config


class SessionService:
    """Manages session persistence and conversation context for agents."""
    
    def __init__(self, storage_dir: Optional[str] = None):
        """Initialize session service with storage directory."""
        self.storage_dir = storage_dir or config.get_session_storage_dir()
        config.ensure_session_storage_dir()
        
        # Create conversation manager with summarization for long conversations
        self.conversation_manager = SummarizingConversationManager()
    
    def get_session_manager(self, session_id: str) -> FileSessionManager:
        """Get or create a session manager for the given session ID."""
        return FileSessionManager(
            session_id=session_id,
            storage_dir=self.storage_dir
        )
    
    def get_conversation_manager(self):
        """Get the conversation manager instance."""
        return self.conversation_manager


class AgentFactory:
    """Factory for creating specialized agents with consistent configuration."""
    
    def __init__(self, model: OllamaModel, session_service: SessionService):
        """Initialize agent factory with model and session service."""
        self.model = model
        self.session_service = session_service
        self._agents_cache = {}
    
    def create_agent(self, 
                    agent_type: str, 
                    system_prompt: str, 
                    tools: Optional[list] = None,
                    session_id: str = "default") -> Agent:
        """
        Create or retrieve a cached agent with consistent configuration.
        
        Args:
            agent_type: Type identifier for the agent
            system_prompt: System prompt for the agent
            tools: Optional list of tools for the agent
            session_id: Session ID for persistence
            
        Returns:
            Configured Agent instance
        """
        cache_key = f"{agent_type}_{session_id}"
        
        if cache_key not in self._agents_cache:
            session_manager = self.session_service.get_session_manager(session_id)
            conversation_manager = self.session_service.get_conversation_manager()
            
            self._agents_cache[cache_key] = Agent(
                model=self.model,
                system_prompt=system_prompt,
                session_manager=session_manager,
                conversation_manager=conversation_manager,
                tools=tools or []
            )
        
        return self._agents_cache[cache_key]
    
    def clear_cache(self):
        """Clear the agents cache."""
        self._agents_cache.clear()
