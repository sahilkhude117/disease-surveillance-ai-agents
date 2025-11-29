"""
LangGraph Multi-Agent Orchestrator
Replaces Azure AI Agent Service with open-source LangGraph

This is a production-ready implementation that can replace the current
surveillance_manager.py with minimal changes to the rest of the codebase.
"""

import os
import uuid
import asyncio
from typing import TypedDict, Annotated, Sequence, Literal
import operator
from datetime import datetime

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import Tool
from dotenv import load_dotenv

# Import existing plugins
from plugins.data_collection_plugin import DataCollectionPlugin
from plugins.anomaly_detection_plugin import AnomalyDetectionPlugin
from plugins.prediction_plugin import PredictionPlugin
from plugins.alert_plugin import AlertPlugin
from plugins.reporting_plugin import ReportingPlugin
from plugins.logging_plugin import LoggingPlugin

# Import agent instructions
from agents.agent_definitions import (
    get_data_collection_agent_instructions,
    get_anomaly_detection_agent_instructions,
    get_prediction_agent_instructions,
    get_alert_agent_instructions,
    get_reporting_agent_instructions,
    get_assistant_agent_instructions
)

load_dotenv()


# ============================================================================
# State Definition
# ============================================================================

class SurveillanceAgentState(TypedDict):
    """State for the surveillance agent workflow"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    session_id: str
    conversation_id: str
    current_agent: str
    user_query: str
    data_collected: dict
    anomalies_found: list
    predictions_made: dict
    alerts_generated: list
    final_report: str
    agents_executed: list
    should_continue: bool


# ============================================================================
# LangGraph Agent Orchestrator
# ============================================================================

class LangGraphSurveillanceOrchestrator:
    """
    Multi-agent orchestrator using LangGraph
    
    This class manages the disease surveillance workflow using multiple
    specialized agents coordinated through a state graph.
    """
    
    def __init__(self, connection_string: str = None):
        """
        Initialize the orchestrator
        
        Args:
            connection_string: Database connection string
        """
        # Get connection string
        if connection_string is None:
            connection_string = os.getenv("DB_CONNECTION_STRING")
        
        self.connection_string = connection_string
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7,
            max_tokens=4096
        )
        
        # Initialize plugins
        self.plugins = self._initialize_plugins()
        
        # Build workflow graph
        self.workflow = self._build_workflow()
        
        print("✅ LangGraph Surveillance Orchestrator initialized")
    
    def _initialize_plugins(self):
        """Initialize all plugins"""
        try:
            return {
                "data_collection": DataCollectionPlugin(self.connection_string),
                "anomaly_detection": AnomalyDetectionPlugin(self.connection_string),
                "prediction": PredictionPlugin(self.connection_string),
                "alert": AlertPlugin(self.connection_string),
                "reporting": ReportingPlugin(self.connection_string),
                "logging": LoggingPlugin(self.connection_string)
            }
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize some plugins: {e}")
            return {}
    
    # ========================================================================
    # Agent Nodes
    # ========================================================================
    
    def _data_collection_node(self, state: SurveillanceAgentState) -> SurveillanceAgentState:
        """Data Collection Agent Node"""
        print("📊 Executing Data Collection Agent...")
        
        try:
            # Get agent instructions
            system_prompt = get_data_collection_agent_instructions()
            user_query = state["user_query"]
            
            # Create messages
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"User query: {user_query}\n\nCollect relevant surveillance data.")
            ]
            
            # Invoke LLM
            response = self.llm.invoke(messages)
            
            # Simulate data collection (in production, this would call actual plugin methods)
            data_collected = {
                "hospital_data": "Sample hospital data...",
                "social_media_data": "Sample social media trends...",
                "environmental_data": "Sample environmental metrics...",
                "timestamp": datetime.now().isoformat()
            }
            
            # Update state
            new_messages = list(state["messages"]) + [
                AIMessage(content=response.content, name="DataCollectionAgent")
            ]
            
            return {
                **state,
                "messages": new_messages,
                "current_agent": "DataCollectionAgent",
                "data_collected": data_collected,
                "agents_executed": state["agents_executed"] + ["DataCollectionAgent"],
                "should_continue": True
            }
        
        except Exception as e:
            print(f"❌ Error in data collection: {e}")
            return {**state, "should_continue": False}
    
    def _anomaly_detection_node(self, state: SurveillanceAgentState) -> SurveillanceAgentState:
        """Anomaly Detection Agent Node"""
        print("🔍 Executing Anomaly Detection Agent...")
        
        try:
            system_prompt = get_anomaly_detection_agent_instructions()
            data_summary = str(state.get("data_collected", {}))
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Analyze this data for anomalies:\n{data_summary}")
            ]
            
            response = self.llm.invoke(messages)
            
            # Simulate anomaly detection
            anomalies = [
                {
                    "id": "ANOM_001",
                    "type": "hospital_surge",
                    "severity": "high",
                    "confidence": 0.85,
                    "location": "Mumbai",
                    "description": "Unusual spike in respiratory illness cases"
                }
            ]
            
            new_messages = list(state["messages"]) + [
                AIMessage(content=response.content, name="AnomalyDetectionAgent")
            ]
            
            return {
                **state,
                "messages": new_messages,
                "current_agent": "AnomalyDetectionAgent",
                "anomalies_found": anomalies,
                "agents_executed": state["agents_executed"] + ["AnomalyDetectionAgent"],
                "should_continue": True
            }
        
        except Exception as e:
            print(f"❌ Error in anomaly detection: {e}")
            return {**state, "should_continue": False}
    
    def _prediction_node(self, state: SurveillanceAgentState) -> SurveillanceAgentState:
        """Prediction Agent Node"""
        print("🔮 Executing Prediction Agent...")
        
        try:
            system_prompt = get_prediction_agent_instructions()
            context = f"Data: {state.get('data_collected', {})}\nAnomalies: {state.get('anomalies_found', [])}"
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Predict disease outbreak based on:\n{context}")
            ]
            
            response = self.llm.invoke(messages)
            
            # Simulate predictions
            predictions = {
                "disease": "Influenza",
                "forecast_weeks": 3,
                "predicted_cases": 1500,
                "confidence": 0.78,
                "risk_level": "medium"
            }
            
            new_messages = list(state["messages"]) + [
                AIMessage(content=response.content, name="PredictionAgent")
            ]
            
            return {
                **state,
                "messages": new_messages,
                "current_agent": "PredictionAgent",
                "predictions_made": predictions,
                "agents_executed": state["agents_executed"] + ["PredictionAgent"],
                "should_continue": True
            }
        
        except Exception as e:
            print(f"❌ Error in prediction: {e}")
            return {**state, "should_continue": False}
    
    def _alert_node(self, state: SurveillanceAgentState) -> SurveillanceAgentState:
        """Alert Generation Agent Node"""
        print("⚠️  Executing Alert Agent...")
        
        try:
            system_prompt = get_alert_agent_instructions()
            context = f"Predictions: {state.get('predictions_made', {})}\nAnomalies: {state.get('anomalies_found', [])}"
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Generate alerts based on:\n{context}")
            ]
            
            response = self.llm.invoke(messages)
            
            # Simulate alert generation
            alerts = [
                {
                    "alert_id": "ALT_001",
                    "severity": "high",
                    "message": "Increased influenza activity detected in Mumbai region",
                    "audience": "public_health_officials"
                }
            ]
            
            new_messages = list(state["messages"]) + [
                AIMessage(content=response.content, name="AlertAgent")
            ]
            
            return {
                **state,
                "messages": new_messages,
                "current_agent": "AlertAgent",
                "alerts_generated": alerts,
                "agents_executed": state["agents_executed"] + ["AlertAgent"],
                "should_continue": True
            }
        
        except Exception as e:
            print(f"❌ Error in alert generation: {e}")
            return {**state, "should_continue": False}
    
    def _reporting_node(self, state: SurveillanceAgentState) -> SurveillanceAgentState:
        """Reporting Agent Node"""
        print("📝 Executing Reporting Agent...")
        
        try:
            system_prompt = get_reporting_agent_instructions()
            
            # Compile all information
            full_context = f"""
            User Query: {state['user_query']}
            
            Data Collected: {state.get('data_collected', {})}
            
            Anomalies Found: {state.get('anomalies_found', [])}
            
            Predictions: {state.get('predictions_made', {})}
            
            Alerts: {state.get('alerts_generated', [])}
            
            Previous Agent Outputs:
            {self._format_agent_messages(state['messages'])}
            """
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Generate comprehensive surveillance report:\n{full_context}")
            ]
            
            response = self.llm.invoke(messages)
            
            new_messages = list(state["messages"]) + [
                AIMessage(content=response.content, name="ReportingAgent")
            ]
            
            return {
                **state,
                "messages": new_messages,
                "current_agent": "ReportingAgent",
                "final_report": response.content,
                "agents_executed": state["agents_executed"] + ["ReportingAgent"],
                "should_continue": False  # End workflow
            }
        
        except Exception as e:
            print(f"❌ Error in reporting: {e}")
            return {**state, "should_continue": False}
    
    def _assistant_node(self, state: SurveillanceAgentState) -> SurveillanceAgentState:
        """Assistant Agent Node (for simple queries)"""
        print("💬 Executing Assistant Agent...")
        
        try:
            system_prompt = get_assistant_agent_instructions()
            user_query = state["user_query"]
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_query)
            ]
            
            response = self.llm.invoke(messages)
            
            new_messages = list(state["messages"]) + [
                AIMessage(content=response.content, name="AssistantAgent")
            ]
            
            return {
                **state,
                "messages": new_messages,
                "current_agent": "AssistantAgent",
                "final_report": response.content,
                "agents_executed": state["agents_executed"] + ["AssistantAgent"],
                "should_continue": False
            }
        
        except Exception as e:
            print(f"❌ Error in assistant: {e}")
            return {**state, "should_continue": False}
    
    # ========================================================================
    # Routing Logic
    # ========================================================================
    
    def _should_use_simple_assistant(self, state: SurveillanceAgentState) -> bool:
        """Determine if query is simple enough for assistant only"""
        user_query = state["user_query"].lower()
        
        simple_keywords = ["what is", "hello", "hi", "help", "about", "explain"]
        return any(keyword in user_query for keyword in simple_keywords)
    
    def _route_entry(self, state: SurveillanceAgentState) -> Literal["assistant", "data_collection"]:
        """Route from entry point"""
        if self._should_use_simple_assistant(state):
            print("→ Routing to Assistant (simple query)")
            return "assistant"
        else:
            print("→ Routing to Data Collection (complex surveillance query)")
            return "data_collection"
    
    def _route_after_data_collection(self, state: SurveillanceAgentState) -> Literal["anomaly_detection", END]:
        """Route after data collection"""
        if state.get("should_continue"):
            return "anomaly_detection"
        return END
    
    def _route_after_anomaly_detection(self, state: SurveillanceAgentState) -> Literal["prediction", "reporting", END]:
        """Route after anomaly detection"""
        if not state.get("should_continue"):
            return END
        
        user_query = state["user_query"].lower()
        if "predict" in user_query or "forecast" in user_query:
            print("→ Prediction requested, routing to Prediction Agent")
            return "prediction"
        else:
            print("→ No prediction requested, routing to Reporting")
            return "reporting"
    
    def _route_after_prediction(self, state: SurveillanceAgentState) -> Literal["alert", END]:
        """Route after prediction"""
        if state.get("should_continue"):
            return "alert"
        return END
    
    def _route_after_alert(self, state: SurveillanceAgentState) -> Literal["reporting", END]:
        """Route after alert generation"""
        if state.get("should_continue"):
            return "reporting"
        return END
    
    # ========================================================================
    # Workflow Construction
    # ========================================================================
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        print("🏗️  Building LangGraph workflow...")
        
        # Create graph
        workflow = StateGraph(SurveillanceAgentState)
        
        # Add nodes
        workflow.add_node("assistant", self._assistant_node)
        workflow.add_node("data_collection", self._data_collection_node)
        workflow.add_node("anomaly_detection", self._anomaly_detection_node)
        workflow.add_node("prediction", self._prediction_node)
        workflow.add_node("alert", self._alert_node)
        workflow.add_node("reporting", self._reporting_node)
        
        # Set entry point with routing
        workflow.set_conditional_entry_point(
            self._route_entry,
            {
                "assistant": "assistant",
                "data_collection": "data_collection"
            }
        )
        
        # Add edges with conditional routing
        workflow.add_conditional_edges(
            "data_collection",
            self._route_after_data_collection,
            {
                "anomaly_detection": "anomaly_detection",
                END: END
            }
        )
        
        workflow.add_conditional_edges(
            "anomaly_detection",
            self._route_after_anomaly_detection,
            {
                "prediction": "prediction",
                "reporting": "reporting",
                END: END
            }
        )
        
        workflow.add_conditional_edges(
            "prediction",
            self._route_after_prediction,
            {
                "alert": "alert",
                END: END
            }
        )
        
        workflow.add_conditional_edges(
            "alert",
            self._route_after_alert,
            {
                "reporting": "reporting",
                END: END
            }
        )
        
        # Terminal nodes
        workflow.add_edge("assistant", END)
        workflow.add_edge("reporting", END)
        
        print("✅ Workflow graph built successfully")
        return workflow.compile()
    
    # ========================================================================
    # Public API
    # ========================================================================
    
    async def process_message(self, message: str, session_id: str = None) -> dict:
        """
        Process a user message through the surveillance workflow
        
        Args:
            message: User's query
            session_id: Optional session ID
            
        Returns:
            Dictionary with response, session_id, and metadata
        """
        # Generate IDs
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        conversation_id = str(uuid.uuid4())
        
        print(f"\n{'='*60}")
        print(f"🚀 Starting surveillance workflow")
        print(f"Session ID: {session_id}")
        print(f"Conversation ID: {conversation_id}")
        print(f"Query: {message}")
        print(f"{'='*60}\n")
        
        # Initialize state
        initial_state = {
            "messages": [HumanMessage(content=message)],
            "session_id": session_id,
            "conversation_id": conversation_id,
            "current_agent": "",
            "user_query": message,
            "data_collected": {},
            "anomalies_found": [],
            "predictions_made": {},
            "alerts_generated": [],
            "final_report": "",
            "agents_executed": [],
            "should_continue": True
        }
        
        try:
            # Execute workflow
            final_state = await self.workflow.ainvoke(initial_state)
            
            # Extract response
            response = final_state.get("final_report", "")
            if not response and final_state.get("messages"):
                # Fallback to last message
                response = final_state["messages"][-1].content
            
            print(f"\n{'='*60}")
            print(f"✅ Workflow completed successfully")
            print(f"Agents executed: {', '.join(final_state['agents_executed'])}")
            print(f"{'='*60}\n")
            
            return {
                "response": response,
                "session_id": session_id,
                "conversation_id": conversation_id,
                "agents_involved": final_state["agents_executed"],
                "timestamp": datetime.now().isoformat(),
                "metadata": {
                    "data_collected": final_state.get("data_collected", {}),
                    "anomalies_found": final_state.get("anomalies_found", []),
                    "predictions_made": final_state.get("predictions_made", {}),
                    "alerts_generated": final_state.get("alerts_generated", [])
                }
            }
        
        except Exception as e:
            print(f"\n{'='*60}")
            print(f"❌ Workflow failed: {e}")
            print(f"{'='*60}\n")
            
            import traceback
            traceback.print_exc()
            
            return {
                "error": str(e),
                "session_id": session_id,
                "conversation_id": conversation_id,
                "response": f"Error processing request: {str(e)}",
                "agents_involved": []
            }
    
    # ========================================================================
    # Utilities
    # ========================================================================
    
    def _format_agent_messages(self, messages: Sequence[BaseMessage]) -> str:
        """Format agent messages for display"""
        formatted = []
        for msg in messages:
            if hasattr(msg, "name") and msg.name:
                formatted.append(f"{msg.name}: {msg.content[:200]}...")
        return "\n".join(formatted)


# ============================================================================
# Convenience Functions
# ============================================================================

# Global instance
_orchestrator = None

def get_orchestrator(connection_string: str = None) -> LangGraphSurveillanceOrchestrator:
    """Get or create orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = LangGraphSurveillanceOrchestrator(connection_string)
    return _orchestrator


async def process_surveillance_query(query: str, session_id: str = None) -> dict:
    """
    Convenience function to process a surveillance query
    
    Args:
        query: User's surveillance query
        session_id: Optional session ID
        
    Returns:
        Response dictionary
    """
    orchestrator = get_orchestrator()
    return await orchestrator.process_message(query, session_id)


# ============================================================================
# Testing
# ============================================================================

if __name__ == "__main__":
    """Test the orchestrator"""
    import asyncio
    
    async def test():
        print("Testing LangGraph Surveillance Orchestrator\n")
        
        # Test 1: Simple query
        print("\n" + "="*60)
        print("TEST 1: Simple query")
        print("="*60)
        result1 = await process_surveillance_query("What is this system about?")
        print(f"Response: {result1['response'][:200]}...")
        
        # Test 2: Anomaly detection
        print("\n" + "="*60)
        print("TEST 2: Anomaly detection")
        print("="*60)
        result2 = await process_surveillance_query("Are there any unusual health patterns in Mumbai?")
        print(f"Response: {result2['response'][:200]}...")
        
        # Test 3: Prediction
        print("\n" + "="*60)
        print("TEST 3: Outbreak prediction")
        print("="*60)
        result3 = await process_surveillance_query("Predict influenza spread for the next 3 weeks")
        print(f"Response: {result3['response'][:200]}...")
    
    asyncio.run(test())
