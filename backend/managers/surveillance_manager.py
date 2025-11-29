"""Surveillance manager for disease outbreak monitoring with AI agents.

MIGRATED FROM AZURE TO LANGGRAPH:
- Replaced Azure AI Agent Service with LangGraph orchestration
- Replaced Azure OpenAI with OpenAI Direct API
- Removed Azure Identity authentication
- Uses LangGraph for multi-agent coordination
"""

import uuid
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional

# Import LangGraph orchestrator (replaces Azure AI Agent Service)
from agents.langgraph_orchestrator import (
    LangGraphSurveillanceOrchestrator,
    process_surveillance_query
)

from config.settings import get_database_connection_string

# Load environment variables
load_dotenv()


class SurveillanceManager:
    """Manages the disease surveillance AI agent system using LangGraph."""
    
    def __init__(self, connection_string=None):
        """Initialize the surveillance manager.
        
        Args:
            connection_string: The database connection string (optional, will load from env if not provided).
        """
        # Get connection string from settings if not provided
        if connection_string is None:
            try:
                connection_string = get_database_connection_string()
            except ValueError:
                print("⚠️  WARNING: Database connection string not configured")
                connection_string = ""
        
        self.connection_string = connection_string
        
        # Initialize LangGraph orchestrator (replaces Azure AI Agent Service)
        print("🚀 Initializing LangGraph Surveillance Orchestrator...")
        try:
            self.orchestrator = LangGraphSurveillanceOrchestrator(connection_string)
            print("✅ LangGraph orchestrator initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing LangGraph orchestrator: {e}")
            import traceback
            traceback.print_exc()
            self.orchestrator = None
        
        # Session management (kept for compatibility with frontend)
        self.chat_sessions = {}
        self.active_sessions = {}
        self._session_lock = asyncio.Lock()
    
    async def initialize_session(self, session_id: str):
        """Initialize or reuse a surveillance session.
        
        Args:
            session_id: The session ID to initialize
            
        Returns:
            dict: The initialized session
        """
        async with self._session_lock:
            # Check if session exists
            if session_id in self.chat_sessions:
                session = self.chat_sessions[session_id]
                session["last_activity"] = datetime.now()
                print(f"♻️  Reusing existing session: {session_id}")
                return session
            
            # Create new session
            print(f"🆕 Creating new session: {session_id}")
            conversation_id = str(uuid.uuid4())
            
            session = {
                "session_id": session_id,
                "conversation_id": conversation_id,
                "created_at": datetime.now(),
                "last_activity": datetime.now(),
                "orchestrator": self.orchestrator,
                "active": True
            }
            
            self.chat_sessions[session_id] = session
            self.active_sessions[session_id] = session
            
            return session
    
    async def process_message(self, message: str, session_id: str = None, max_iterations: int = 10):
        """Process a user message through the surveillance agent system.
        
        Args:
            message: The user's message
            session_id: The session ID (optional, will create new if not provided)
            max_iterations: Maximum iterations for agent conversation (compatibility param, not used)
            
        Returns:
            dict: Response containing agent outputs in frontend-compatible format
        """
        try:
            # Generate session_id if not provided
            if session_id is None:
                session_id = str(uuid.uuid4())
            
            # Initialize or get session
            session = await self.initialize_session(session_id)
            
            print(f"\n{'='*60}")
            print(f"📨 Processing message for session: {session_id}")
            print(f"Message: {message[:100]}{'...' if len(message) > 100 else ''}")
            print(f"{'='*60}\n")
            
            # Check if orchestrator is available
            if not self.orchestrator:
                raise Exception("LangGraph orchestrator not initialized")
            
            # Process message through LangGraph orchestrator
            result = await self.orchestrator.process_message(message, session_id)
            
            # Update session last activity
            async with self._session_lock:
                if session_id in self.chat_sessions:
                    self.chat_sessions[session_id]["last_activity"] = datetime.now()
            
            # Format response for frontend compatibility
            response = {
                "session_id": session_id,
                "conversation_id": session.get("conversation_id", result.get("conversation_id", "")),
                "response": result.get("response", ""),
                "agents_involved": result.get("agents_involved", []),
                "timestamp": result.get("timestamp", datetime.now().isoformat()),
                "metadata": result.get("metadata", {})
            }
            
            print(f"\n{'='*60}")
            print(f"✅ Message processed successfully")
            print(f"Agents involved: {', '.join(response['agents_involved'])}")
            print(f"{'='*60}\n")
            
            return response
            
        except Exception as e:
            print(f"\n{'='*60}")
            print(f"❌ Error processing message: {e}")
            print(f"{'='*60}\n")
            
            import traceback
            traceback.print_exc()
            
            return {
                "error": str(e),
                "session_id": session_id,
                "response": f"I apologize, but I encountered an error while processing your request: {str(e)}",
                "agents_involved": [],
                "timestamp": datetime.now().isoformat()
            }
    
    async def close_session(self, session_id: str):
        """Close a surveillance session.
        
        Args:
            session_id: The session ID to close
        """
        async with self._session_lock:
            if session_id in self.chat_sessions:
                self.chat_sessions[session_id]["active"] = False
                print(f"🔒 Closed session: {session_id}")
            
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
    
    async def cleanup_old_sessions(self, max_age_minutes: int = 60):
        """Clean up old inactive sessions.
        
        Args:
            max_age_minutes: Maximum age in minutes before cleaning up a session
        """
        async with self._session_lock:
            now = datetime.now()
            sessions_to_remove = []
            
            for session_id, session in self.chat_sessions.items():
                last_activity = session.get("last_activity", session.get("created_at"))
                age_minutes = (now - last_activity).total_seconds() / 60
                
                if age_minutes > max_age_minutes:
                    sessions_to_remove.append(session_id)
            
            for session_id in sessions_to_remove:
                del self.chat_sessions[session_id]
                if session_id in self.active_sessions:
                    del self.active_sessions[session_id]
                print(f"🗑️  Cleaned up old session: {session_id}")
            
            if sessions_to_remove:
                print(f"✨ Cleaned up {len(sessions_to_remove)} old sessions")


# Convenience function for backward compatibility
async def process_surveillance_message(message: str, connection_string: str = None) -> dict:
    """Convenience function to process a surveillance message without managing sessions.
    
    Args:
        message: The user's message
        connection_string: Optional database connection string
        
    Returns:
        dict: Response from the surveillance system
    """
    manager = SurveillanceManager(connection_string)
    return await manager.process_message(message)
