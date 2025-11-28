"""Surveillance manager for disease outbreak monitoring with AI agents."""

import uuid
import asyncio
import json
import os
import pyodbc
import time
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional

from azure.identity.aio import DefaultAzureCredential
from semantic_kernel.agents import AgentGroupChat
from semantic_kernel.agents import AzureAIAgent
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from config.settings import initialize_ai_agent_settings
from agents.agent_definitions import (
    DATA_COLLECTION_AGENT, get_data_collection_agent_instructions,
    ANOMALY_DETECTION_AGENT, get_anomaly_detection_agent_instructions,
    PREDICTION_AGENT, get_prediction_agent_instructions,
    ALERT_AGENT, get_alert_agent_instructions,
    REPORTING_AGENT, get_reporting_agent_instructions,
    ASSISTANT_AGENT, get_assistant_agent_instructions
)
from agents.agent_strategies import (
    SurveillanceSelectionStrategy, SurveillanceTerminationStrategy
)
from agents.agent_manager import create_or_reuse_agent
from plugins.data_collection_plugin import DataCollectionPlugin
from plugins.anomaly_detection_plugin import AnomalyDetectionPlugin
from plugins.prediction_plugin import PredictionPlugin
from plugins.alert_plugin import AlertPlugin
from plugins.reporting_plugin import ReportingPlugin
from plugins.logging_plugin import LoggingPlugin

# Load environment variables
load_dotenv()


class SurveillanceManager:
    """Manages the disease surveillance AI agent system."""
    
    def __init__(self, connection_string=None):
        """Initialize the surveillance manager.
        
        Args:
            connection_string: The database connection string (optional, will load from env if not provided).
        """
        # Get connection string from settings if not provided
        if connection_string is None:
            from config.settings import get_database_connection_string
            try:
                connection_string = get_database_connection_string()
            except ValueError:
                print("WARNING: Database connection string not configured")
                connection_string = ""
        
        self.connection_string = connection_string
        
        # Initialize plugins with error handling
        try:
            self.data_collection_plugin = DataCollectionPlugin(connection_string) if connection_string else None
        except Exception as e:
            print(f"Error initializing data collection plugin: {e}")
            self.data_collection_plugin = None
            
        try:
            self.anomaly_detection_plugin = AnomalyDetectionPlugin(connection_string) if connection_string else None
        except Exception as e:
            print(f"Error initializing anomaly detection plugin: {e}")
            self.anomaly_detection_plugin = None
            
        try:
            self.prediction_plugin = PredictionPlugin(connection_string) if connection_string else None
        except Exception as e:
            print(f"Error initializing prediction plugin: {e}")
            self.prediction_plugin = None
            
        try:
            self.alert_plugin = AlertPlugin(connection_string) if connection_string else None
        except Exception as e:
            print(f"Error initializing alert plugin: {e}")
            self.alert_plugin = None
            
        try:
            self.reporting_plugin = ReportingPlugin(connection_string) if connection_string else None
        except Exception as e:
            print(f"Error initializing reporting plugin: {e}")
            self.reporting_plugin = None
        
        # Session management
        self.chat_sessions = {}
        self.active_sessions = {}  # Add this for compatibility with frontend
        self._session_lock = asyncio.Lock()
        self._processing_locks = {}
        self._session_tasks = {}
        
        # Get Bing API key from environment
        self.bing_api_key = os.getenv("BING_SEARCH_API_KEY")
        if not self.bing_api_key:
            print("WARNING: BING_SEARCH_API_KEY not found in environment variables")
    
    async def initialize_session(self, session_id):
        """Initialize or reuse a surveillance session.
        
        Args:
            session_id: The session ID to initialize
            
        Returns:
            dict: The initialized session
        """
        # Check if session exists
        if session_id in self.chat_sessions:
            session = self.chat_sessions[session_id]
            if not session.get("initializing", False) and "chat" in session:
                print(f"Reusing existing surveillance session: {session_id}")
                async with self._session_lock:
                    session["last_activity"] = datetime.now()
                return session
        
        # Acquire lock for initialization
        async with self._session_lock:
            # Double-check after acquiring lock
            if session_id in self.chat_sessions:
                session = self.chat_sessions[session_id]
                if not session.get("initializing", False) and "chat" in session:
                    session["last_activity"] = datetime.now()
                    return session
                elif session.get("initializing", False):
                    print(f"Session {session_id} is already being initialized, waiting...")
            
            print(f"Creating new surveillance session: {session_id}")
            
            # Generate conversation ID
            conversation_id = str(uuid.uuid4())
            
            # Mark as initializing
            self.chat_sessions[session_id] = {
                "initializing": True,
                "last_activity": datetime.now(),
                "conversation_id": conversation_id,
                "cancellation_token": asyncio.Future()
            }
        
        try:
            # Get Azure AI Agent settings
            ai_agent_settings = initialize_ai_agent_settings()
            
            # Create credentials and client
            creds = DefaultAzureCredential(
                exclude_environment_credential=True,
                exclude_managed_identity_credential=True
            )
            client = AzureAIAgent.create_client(credential=creds)
            
            # Create session with all agents
            session = await self._create_agents_for_session(
                client,
                ai_agent_settings,
                session_id,
                conversation_id
            )
            
            # Update the chat session
            async with self._session_lock:
                if session_id in self.chat_sessions:
                    self.chat_sessions[session_id].update(session)
                    return self.chat_sessions[session_id]
                else:
                    await self._cleanup_resources(session)
                    self.chat_sessions[session_id] = session
                    return self.chat_sessions[session_id]
        
        except Exception as e:
            print(f"Error in initialize_session for {session_id}: {e}")
            import traceback
            traceback.print_exc()
            async with self._session_lock:
                if session_id in self.chat_sessions:
                    del self.chat_sessions[session_id]
            raise
    
    async def _create_agents_for_session(self, client, ai_agent_settings, session_id, conversation_id):
        """Create or reuse all surveillance agents for a session.
        
        Args:
            client: The Azure AI Agent client
            ai_agent_settings: The agent settings
            session_id: The session ID
            conversation_id: The conversation ID
            
        Returns:
            dict: The session data with initialized agents
        """
        # Create credentials
        credential = DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
        
        # Create separate logging plugins for each agent
        data_collection_logging = LoggingPlugin(self.connection_string)
        anomaly_detection_logging = LoggingPlugin(self.connection_string)
        prediction_logging = LoggingPlugin(self.connection_string)
        alert_logging = LoggingPlugin(self.connection_string)
        reporting_logging = LoggingPlugin(self.connection_string)
        assistant_logging = LoggingPlugin(self.connection_string)
        
        # Create Bing connection configuration
        bing_connection = None
        if self.bing_api_key:
            bing_connection = {
                "type": "BingGrounding",
                "api_key": self.bing_api_key
            }
            print(f"Bing connection configured with API key")
        else:
            print("WARNING: Bing search will not be available")
        
        # Create or reuse all agents
        agents = {}
        
        # Data Collection Agent
        print(f"Creating data collection agent for session {session_id}...")
        agents[DATA_COLLECTION_AGENT] = await create_or_reuse_agent(
            client=client,
            agent_name=DATA_COLLECTION_AGENT,
            model_deployment_name=ai_agent_settings.model_deployment_name,
            instructions=get_data_collection_agent_instructions(),
            plugins=[self.data_collection_plugin, data_collection_logging]
        )
        
        # Anomaly Detection Agent
        print(f"Creating anomaly detection agent for session {session_id}...")
        agents[ANOMALY_DETECTION_AGENT] = await create_or_reuse_agent(
            client=client,
            agent_name=ANOMALY_DETECTION_AGENT,
            model_deployment_name=ai_agent_settings.model_deployment_name,
            instructions=get_anomaly_detection_agent_instructions(),
            plugins=[self.anomaly_detection_plugin, anomaly_detection_logging]
        )
        
        # Prediction Agent (with Bing for R0 research)
        print(f"Creating prediction agent for session {session_id}...")
        agents[PREDICTION_AGENT] = await create_or_reuse_agent(
            client=client,
            agent_name=PREDICTION_AGENT,
            model_deployment_name=ai_agent_settings.model_deployment_name,
            instructions=get_prediction_agent_instructions(),
            plugins=[self.prediction_plugin, prediction_logging],
            connections=bing_connection
        )
        
        # Alert Agent
        print(f"Creating alert agent for session {session_id}...")
        agents[ALERT_AGENT] = await create_or_reuse_agent(
            client=client,
            agent_name=ALERT_AGENT,
            model_deployment_name=ai_agent_settings.model_deployment_name,
            instructions=get_alert_agent_instructions(),
            plugins=[self.alert_plugin, alert_logging]
        )
        
        # Reporting Agent
        print(f"Creating reporting agent for session {session_id}...")
        agents[REPORTING_AGENT] = await create_or_reuse_agent(
            client=client,
            agent_name=REPORTING_AGENT,
            model_deployment_name=ai_agent_settings.model_deployment_name,
            instructions=get_reporting_agent_instructions(),
            plugins=[self.reporting_plugin, reporting_logging]
        )
        
        # Assistant Agent
        print(f"Creating assistant agent for session {session_id}...")
        agents[ASSISTANT_AGENT] = await create_or_reuse_agent(
            client=client,
            agent_name=ASSISTANT_AGENT,
            model_deployment_name=ai_agent_settings.model_deployment_name,
            instructions=get_assistant_agent_instructions(),
            plugins=[self.data_collection_plugin, assistant_logging]
        )
        
        # Get agent IDs and set them in logging plugins
        agent_ids = self._extract_agent_ids(agents)
        self._set_agent_ids_in_plugins(
            agent_ids,
            data_collection_logging,
            anomaly_detection_logging,
            prediction_logging,
            alert_logging,
            reporting_logging,
            assistant_logging
        )
        
        # Print agent status
        for agent_name, agent in agents.items():
            print(f"{agent_name} ready: {agent.name} (ID: {agent_ids.get(agent_name, 'None')})")
        
        # Create chat object
        chat = AgentGroupChat(
            agents=list(agents.values()),
            termination_strategy=SurveillanceTerminationStrategy(),
            selection_strategy=SurveillanceSelectionStrategy()
        )
        
        print(f"Surveillance session created successfully: {session_id}")
        
        # Initialize task tracking
        self._session_tasks[session_id] = []
        
        # Return session data
        return {
            "chat": chat,
            "client": client,
            "credential": credential,
            "last_activity": datetime.now(),
            "model_deployment_name": ai_agent_settings.model_deployment_name,
            "agents": agents,
            "agent_ids": agent_ids,
            "conversation_id": conversation_id,
            "initializing": False,
            "cancellation_token": asyncio.Future()
        }
    
    def _extract_agent_ids(self, agents):
        """Extract agent IDs from agent objects."""
        agent_ids = {}
        for agent_name, agent in agents.items():
            if hasattr(agent, 'definition') and hasattr(agent.definition, 'id'):
                agent_ids[agent_name] = agent.definition.id
            else:
                agent_ids[agent_name] = None
        return agent_ids
    
    def _set_agent_ids_in_plugins(self, agent_ids, data_collection_logging, 
                                  anomaly_detection_logging, prediction_logging,
                                  alert_logging, reporting_logging, assistant_logging):
        """Set agent IDs in logging plugins."""
        if agent_ids.get(DATA_COLLECTION_AGENT):
            data_collection_logging.set_agent_id(agent_ids[DATA_COLLECTION_AGENT])
        if agent_ids.get(ANOMALY_DETECTION_AGENT):
            anomaly_detection_logging.set_agent_id(agent_ids[ANOMALY_DETECTION_AGENT])
        if agent_ids.get(PREDICTION_AGENT):
            prediction_logging.set_agent_id(agent_ids[PREDICTION_AGENT])
        if agent_ids.get(ALERT_AGENT):
            alert_logging.set_agent_id(agent_ids[ALERT_AGENT])
        if agent_ids.get(REPORTING_AGENT):
            reporting_logging.set_agent_id(agent_ids[REPORTING_AGENT])
        if agent_ids.get(ASSISTANT_AGENT):
            assistant_logging.set_agent_id(agent_ids[ASSISTANT_AGENT])
    
    async def _cleanup_resources(self, session):
        """Clean up resources for a session."""
        if "client" in session:
            client = session["client"]
            if hasattr(client, 'close') and callable(client.close):
                try:
                    await client.close()
                except Exception as e:
                    print(f"Error closing client: {e}")
        
        if "credential" in session:
            credential = session["credential"]
            if hasattr(credential, 'close') and callable(credential.close):
                try:
                    await credential.close()
                except Exception as e:
                    print(f"Error closing credentials: {e}")
    
    async def process_message(self, message: str, session_id: str = None, max_iterations: int = 10):
        """Process a user message through the surveillance agent system.
        
        Args:
            message: The user's message
            session_id: The session ID (optional, will create new if not provided)
            max_iterations: Maximum iterations for agent conversation
            
        Returns:
            dict: Response containing agent outputs in frontend-compatible format
        """
        try:
            # Generate session_id if not provided
            if session_id is None:
                session_id = str(uuid.uuid4())
            
            # Initialize or get session
            session = await self.initialize_session(session_id)
            chat = session["chat"]
            conversation_id = session["conversation_id"]
            
            # Create user message
            msg = ChatMessageContent(
                role=AuthorRole.USER,
                content=message
            )
            
            # Add message to chat
            await chat.add_chat_message(msg)
            
            # Track responses
            latest_responses = {}
            
            # Process chat with timeout
            timeout_seconds = 600  # 10 minutes
            await self._process_with_timeout(
                chat,
                latest_responses,
                timeout_seconds,
                session.get("cancellation_token")
            )
            
            # Format response for frontend (matching azure structure)
            # Combine all agent responses into a single response string
            combined_response = ""
            agents_involved = []
            
            for agent_name, response_msg in latest_responses.items():
                if hasattr(response_msg, 'content'):
                    agents_involved.append(agent_name)
                    # Add agent responses with proper formatting
                    content = response_msg.content
                    # Remove agent name prefix if it exists
                    if content.startswith(f"{agent_name} > "):
                        content = content[len(f"{agent_name} > "):]
                    combined_response += f"\n\n{content}"
            
            # Format final response similar to azure pattern
            response = {
                "session_id": session_id,
                "conversation_id": conversation_id,
                "response": combined_response.strip(),
                "agents_involved": agents_involved,
                "timestamp": datetime.now().isoformat()
            }
            
            return response
            
        except Exception as e:
            print(f"Error processing message: {e}")
            import traceback
            traceback.print_exc()
            return {
                "error": str(e),
                "session_id": session_id,
                "response": f"Error processing request: {str(e)}",
                "agents_involved": []
            }
    
    async def _process_with_timeout(self, chat, latest_responses, timeout_seconds, cancellation_token=None):
        """Process chat invocation with timeout."""
        start_time = time.time()
        
        try:
            async def process_stream():
                try:
                    async for response in chat.invoke():
                        # Check cancellation
                        if cancellation_token and cancellation_token.done():
                            print("Processing cancelled")
                            return
                        
                        # Check timeout
                        if time.time() - start_time > timeout_seconds:
                            print(f"Process timeout after {timeout_seconds} seconds")
                            return
                        
                        if response is None or not hasattr(response, 'name'):
                            continue
                        
                        agent_name = response.name
                        latest_responses[agent_name] = response
                        
                        # Check if we have all required responses
                        if REPORTING_AGENT in latest_responses:
                            print("Received reporting agent response, terminating")
                            return
                
                except asyncio.CancelledError:
                    print("Process stream cancelled")
                    raise
                except Exception as e:
                    print(f"Error in process_stream: {e}")
                    import traceback
                    traceback.print_exc()
            
            # Create processing task
            process_task = asyncio.create_task(process_stream())
            
            # Create timeout task
            timeout_task = asyncio.create_task(asyncio.sleep(timeout_seconds))
            
            # Wait for completion
            done, pending = await asyncio.wait(
                {process_task, timeout_task},
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel pending tasks
            for task in pending:
                task.cancel()
        
        except asyncio.TimeoutError:
            print(f"Process timed out after {timeout_seconds} seconds")
        except Exception as e:
            print(f"Error during _process_with_timeout: {e}")
            import traceback
            traceback.print_exc()
    
    async def close_session(self, session_id: str):
        """Close a surveillance session.
        
        Args:
            session_id: The session ID to close
        """
        async with self._session_lock:
            if session_id in self.chat_sessions:
                session = self.chat_sessions[session_id]
                await self._cleanup_resources(session)
                del self.chat_sessions[session_id]
                print(f"Closed surveillance session: {session_id}")
