"""Main entry point for the disease surveillance AI agent application."""

import sys
import json
import uvicorn
import logging
from dotenv import load_dotenv

from config.settings import get_database_connection_string
from api.app import app

# Load environment variables
load_dotenv()


def main():
    """Main function to run the disease surveillance application."""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting Disease Surveillance AI Agent System")
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        # Get database connection string
        connection_string = get_database_connection_string()
        
        if sys.argv[1] == "--test-connection":
            # Test database connection
            try:
                import pyodbc
                conn = pyodbc.connect(connection_string)
                cursor = conn.cursor()
                cursor.execute("SELECT @@VERSION")
                version = cursor.fetchone()
                logger.info(f"Database connection successful: {version[0]}")
                cursor.close()
                conn.close()
                print("✅ Database connection successful!")
                return
            except Exception as e:
                logger.error(f"Database connection failed: {e}")
                print(f"❌ Database connection failed: {e}")
                return
        
        elif sys.argv[1] == "--test-plugins":
            # Test plugin initialization
            logger.info("Testing plugin initialization...")
            try:
                from plugins.data_collection_plugin import DataCollectionPlugin
                from plugins.anomaly_detection_plugin import AnomalyDetectionPlugin
                from plugins.prediction_plugin import PredictionPlugin
                from plugins.alert_plugin import AlertPlugin
                from plugins.reporting_plugin import ReportingPlugin
                from plugins.logging_plugin import LoggingPlugin
                
                plugins = {
                    "Data Collection": DataCollectionPlugin(connection_string),
                    "Anomaly Detection": AnomalyDetectionPlugin(connection_string),
                    "Prediction": PredictionPlugin(connection_string),
                    "Alert": AlertPlugin(connection_string),
                    "Reporting": ReportingPlugin(connection_string),
                    "Logging": LoggingPlugin(connection_string)
                }
                
                for name, plugin in plugins.items():
                    logger.info(f"✅ {name} plugin initialized successfully")
                    print(f"✅ {name} plugin initialized successfully")
                
                print("\n✅ All plugins initialized successfully!")
                return
            except Exception as e:
                logger.error(f"Plugin initialization failed: {e}")
                print(f"❌ Plugin initialization failed: {e}")
                import traceback
                traceback.print_exc()
                return
        
        elif sys.argv[1] == "--test-agents":
            # Test agent initialization
            logger.info("Testing agent initialization...")
            try:
                from agents.agent_definitions import (
                    DATA_COLLECTION_AGENT, ANOMALY_DETECTION_AGENT,
                    PREDICTION_AGENT, ALERT_AGENT, REPORTING_AGENT, ASSISTANT_AGENT
                )
                
                agents = [
                    DATA_COLLECTION_AGENT,
                    ANOMALY_DETECTION_AGENT,
                    PREDICTION_AGENT,
                    ALERT_AGENT,
                    REPORTING_AGENT,
                    ASSISTANT_AGENT
                ]
                
                for agent_name in agents:
                    logger.info(f"✅ {agent_name} defined")
                    print(f"✅ {agent_name} defined")
                
                print("\n✅ All agents defined successfully!")
                return
            except Exception as e:
                logger.error(f"Agent initialization failed: {e}")
                print(f"❌ Agent initialization failed: {e}")
                return
        
        elif sys.argv[1] == "--version":
            print("Disease Surveillance AI Agent System v1.0.0")
            print("Built with Azure AI Agent Service and Semantic Kernel")
            return
        
        elif sys.argv[1] == "--help":
            print("""
Disease Surveillance AI Agent System

Usage:
    python main.py                    Start the API server
    python main.py --test-connection  Test database connection
    python main.py --test-plugins     Test plugin initialization
    python main.py --test-agents      Test agent definitions
    python main.py --version          Show version information
    python main.py --help             Show this help message

Environment Variables Required:
    AZURE_AI_PROJECT_CONNECTION_STRING
    AZURE_AI_MODEL_DEPLOYMENT_NAME
    DB_CONNECTION_STRING
    AZURE_STORAGE_CONNECTION_STRING (optional)
    BING_SEARCH_API_KEY (optional)

For more information, see the README.md file.
            """)
            return
    
    # Run the API server
    logger.info("Starting FastAPI server on http://0.0.0.0:8000")
    print("""
╔══════════════════════════════════════════════════════════════╗
║   Disease Surveillance AI Agent System                      ║
║   Starting API Server...                                     ║
║                                                              ║
║   API: http://localhost:8000                                ║
║   Docs: http://localhost:8000/docs                          ║
║   Health: http://localhost:8000/health                      ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()
