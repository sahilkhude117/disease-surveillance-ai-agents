"""Consolidated logging plugin for all agent and event logging in disease surveillance system."""

import json
import uuid


class LoggingPlugin:
    """A consolidated plugin for all logging functions in disease surveillance."""
    
    def __init__(self, connection_string):
        self.connection_string = connection_string
        # Store agent ID and thread ID in memory once retrieved
        self._current_agent_id = None
        self._current_thread_id = None
    
    def log_agent_get_agent_id(self) -> str:
        """Retrieves the current agent's ID from context.
        
        Returns:
            The current agent's ID or a placeholder if not available
        """
        try:
            if self._current_agent_id:
                return self._current_agent_id
            return "AGENT_ID_NOT_SET"
        except Exception as e:
            print(f"Error in log_agent_get_agent_id: {e}")
            return "AGENT_ID_ERROR"
    
    def set_agent_id(self, agent_id: str):
        """Sets the current agent ID.
        
        Args:
            agent_id: The ID to set
        """
        try:
            self._current_agent_id = agent_id
        except Exception as e:
            print(f"Error in set_agent_id: {e}")
    
    def log_agent_get_thread_id(self) -> str:
        """Retrieves the latest thread ID.
    
        Returns:
            latest thread id or a placeholder if not available
        """
        try:
            if self._current_thread_id:
                return self._current_thread_id
                
            try:
                from config.settings import get_project_client
                
                try:
                    project_client = get_project_client()
                    thread_id = None
    
                    with project_client:
                        try:
                            threads_list = project_client.agents.list_threads(limit=1)
                            if hasattr(threads_list, 'first_id'):
                                thread_id = threads_list.first_id
                            elif hasattr(threads_list, 'data') and threads_list.data:
                                thread_id = threads_list.data[0].id
                            else:
                                threads_data = getattr(threads_list, 'data', None) or []
                                if threads_data and len(threads_data) > 0:
                                    thread_id = threads_data[0].get('id')
                            
                            print(f"Thread ID From Logging Plugin: {thread_id}")
                            
                            if thread_id:
                                self._current_thread_id = thread_id
                        except Exception as e:
                            print(f"Error getting thread ID from client: {e}")
                            return "thread_id_not_available"
                    
                    return thread_id or "thread_id_not_found"
                    
                except Exception as e:
                    print(f"Error getting project client: {e}")
                    return "thread_id_not_available_client_error"
            except ImportError:
                print("Could not import get_project_client")
                return "thread_id_import_error"
                
        except Exception as e:
            print(f"Error getting thread ID: {e}")
            return "thread_id_error"
    
    def log_agent_thinking(self, agent_name: str, thinking_stage: str, thought_content: str, 
                        conversation_id: str = None, session_id: str = None, 
                        azure_agent_id: str = None, model_deployment_name: str = None,
                        thread_id: str = None, user_query: str = None, 
                        agent_output: str = None, thinking_stage_output: str = None,
                        status: str = "success") -> str:
        """Logs the agent's thinking process to the database with improved error handling.
        
        Args:
            agent_name: Name of the agent (e.g., DATA_COLLECTION_AGENT, ANOMALY_DETECTION_AGENT)
            thinking_stage: Current thinking stage (e.g., collection_start, analysis_start)
            thought_content: The agent's thoughts at this stage
            conversation_id: Unique ID for this conversation
            session_id: ID of the current chat session
            azure_agent_id: ID of the Azure AI agent
            model_deployment_name: Name of the model deployment
            thread_id: ID of the Azure thread for this conversation (if available)
            user_query: The original user query that initiated this thinking process
            agent_output: The full agent response (including prefix)
            thinking_stage_output: The output of this specific thinking stage
            status: Status of this thinking step (success, error, rate_limited, etc.)
            
        Returns:
            JSON string with the result of the logging operation
        """
        try:
            import json
            import uuid
            
            # Generate conversation_id if not provided
            if not conversation_id:
                conversation_id = str(uuid.uuid4())
            
            # If thread_id is None, try to get it
            if thread_id is None:
                try:
                    thread_id = self.log_agent_get_thread_id()
                except Exception as e:
                    print(f"Error getting thread ID: {e}")
                    thread_id = "thread_id_retrieval_error"
            
            # If azure_agent_id is None, try to get it
            if azure_agent_id is None or azure_agent_id == "Get by calling log_agent_get_agent_id()":
                try:
                    azure_agent_id = self.log_agent_get_agent_id()
                except Exception as e:
                    print(f"Error getting agent ID: {e}")
                    azure_agent_id = "agent_id_retrieval_error"
            
            # Handle non-string outputs
            if thinking_stage_output is not None and not isinstance(thinking_stage_output, str):
                try:
                    thinking_stage_output = json.dumps(thinking_stage_output)
                except Exception:
                    thinking_stage_output = str(thinking_stage_output)
            
            if agent_output is not None and not isinstance(agent_output, str):
                try:
                    agent_output = json.dumps(agent_output)
                except Exception:
                    agent_output = str(agent_output)
            
            # Truncate fields that might be too long
            max_text_length = 50000
            
            if thought_content and len(thought_content) > max_text_length:
                thought_content = thought_content[:max_text_length] + "... [TRUNCATED]"
                
            if thinking_stage_output and len(thinking_stage_output) > max_text_length:
                thinking_stage_output = thinking_stage_output[:max_text_length] + "... [TRUNCATED]"
                
            if agent_output and len(agent_output) > max_text_length:
                agent_output = agent_output[:max_text_length] + "... [TRUNCATED]"
            
            try:
                import psycopg2
                conn = psycopg2.connect(self.connection_string)
                cursor = conn.cursor()
                
                # Insert into agent_thinking_logs table
                cursor.execute("""
                    INSERT INTO agent_thinking_logs
                    (agent_name, thinking_stage, thought_content, thinking_stage_output, agent_output, 
                    conversation_id, session_id, agent_id, model_deployment_name, thread_id,
                    user_query, status, created_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                """, (agent_name, thinking_stage, thought_content, thinking_stage_output, agent_output, 
                      conversation_id, session_id, azure_agent_id, model_deployment_name, thread_id,
                      user_query, status))
                
                conn.commit()
                cursor.close()
                conn.close()
                
                return json.dumps({"success": True, "conversation_id": conversation_id})
                
            except Exception as db_error:
                print(f"Database error in log_agent_thinking: {db_error}")
                
                try:
                    # Log to console as fallback
                    print(f"FALLBACK LOG - Agent: {agent_name}, Stage: {thinking_stage}")
                    print(f"FALLBACK LOG - Conversation: {conversation_id}, Session: {session_id}")
                    print(f"FALLBACK LOG - Content: {thought_content[:200]}...")
                    
                    return json.dumps({
                        "success": False, 
                        "error": str(db_error),
                        "fallback": "Logged to console", 
                        "conversation_id": conversation_id
                    })
                except Exception as fallback_error:
                    print(f"Fallback logging error: {fallback_error}")
                    return json.dumps({"error": f"Database error: {db_error}, Fallback error: {fallback_error}"})
                
        except Exception as e:
            print(f"Error in log_agent_thinking: {e}")
            import traceback
            traceback.print_exc()
            try:
                import json
                return json.dumps({"error": str(e)})
            except:
                return '{"error": "Unknown error in log_agent_thinking"}'

    def log_agent_response(self, agent_name: str, response_content: str, 
                           conversation_id: str = None, session_id: str = None,
                           azure_agent_id: str = None, model_deployment_name: str = None,
                           thread_id: str = None, user_query: str = None) -> str:
        """Logs a complete agent response to facilitate debugging."""
        return self.log_agent_thinking(
            agent_name=agent_name,
            thinking_stage="complete_response",
            thought_content=f"Complete response from {agent_name}",
            conversation_id=conversation_id,
            session_id=session_id,
            azure_agent_id=azure_agent_id,
            model_deployment_name=model_deployment_name,
            thread_id=thread_id,
            user_query=user_query,
            agent_output=response_content,
            thinking_stage_output=response_content
        )
    
    def log_agent_error(self, agent_name: str, error_type: str, error_message: str,
                      conversation_id: str = None, session_id: str = None,
                      azure_agent_id: str = None, model_deployment_name: str = None,
                      thread_id: str = None, user_query: str = None) -> str:
        """Logs an error that occurred during agent thinking."""
        return self.log_agent_thinking(
            agent_name=agent_name,
            thinking_stage="error",
            thought_content=f"Error type: {error_type}\nError message: {error_message}",
            conversation_id=conversation_id,
            session_id=session_id,
            azure_agent_id=azure_agent_id,
            model_deployment_name=model_deployment_name,
            thread_id=thread_id,
            user_query=user_query,
            status="error"
        )
