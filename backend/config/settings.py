"""Application settings and configuration management."""

import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application configuration settings."""
    
    # Azure AI Configuration
    AZURE_AI_PROJECT_CONNECTION_STRING = os.getenv("AZURE_AI_AGENT_PROJECT_CONNECTION_STRING", "")
    AZURE_AI_MODEL_DEPLOYMENT_NAME = os.getenv("AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME", "gpt-4")
    
    # Database Configuration
    DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING", "")
    
    # Azure Storage Configuration
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
    STORAGE_CONTAINER_NAME = "surveillance-reports"
    
    # Bing Search Configuration
    BING_SEARCH_API_KEY = os.getenv("BING_SEARCH_API_KEY", "")
    BING_CONNECTION_NAME = os.getenv("BING_CONNECTION_NAME", "")
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Agent Configuration
    AGENT_TIMEOUT = 300  # seconds
    MAX_RETRIES = 3
    
    # Data Collection Settings
    DATA_COLLECTION_INTERVAL = 3600  # seconds (1 hour)
    ANOMALY_DETECTION_THRESHOLD = 0.75
    PREDICTION_HORIZON_WEEKS = 3
    
    # Alert Settings
    ALERT_HIGH_RISK_THRESHOLD = 0.8
    ALERT_MEDIUM_RISK_THRESHOLD = 0.5
    ALERT_LOW_RISK_THRESHOLD = 0.3
    
    @classmethod
    def validate(cls):
        """Validate that required settings are configured."""
        required_settings = [
            ("AZURE_AI_PROJECT_CONNECTION_STRING", cls.AZURE_AI_PROJECT_CONNECTION_STRING),
            ("AZURE_AI_MODEL_DEPLOYMENT_NAME", cls.AZURE_AI_MODEL_DEPLOYMENT_NAME),
        ]
        
        missing = [name for name, value in required_settings if not value]
        if missing:
            raise ValueError(f"Missing required settings: {', '.join(missing)}")
        
        return True

# Create a singleton instance
settings = Settings()


class AIAgentSettings:
    """Settings for AI Agent initialization."""
    
    def __init__(self, connection_string: str = None, model_deployment_name: str = None):
        """Initialize AI Agent settings.
        
        Args:
            connection_string: Azure AI Project connection string
            model_deployment_name: Model deployment name
        """
        self.connection_string = connection_string or settings.AZURE_AI_PROJECT_CONNECTION_STRING
        self.model_deployment_name = model_deployment_name or settings.AZURE_AI_MODEL_DEPLOYMENT_NAME
    
    def validate(self):
        """Validate settings."""
        if not self.connection_string:
            raise ValueError("Azure AI Project connection string is required")
        if not self.model_deployment_name:
            raise ValueError("Model deployment name is required")
        return True


def initialize_ai_agent_settings(connection_string: str = None, 
                                 model_deployment_name: str = None) -> AIAgentSettings:
    """Initialize AI Agent settings.
    
    Args:
        connection_string: Optional connection string override
        model_deployment_name: Optional model deployment name override
        
    Returns:
        AIAgentSettings instance
    """
    ai_settings = AIAgentSettings(
        connection_string=connection_string,
        model_deployment_name=model_deployment_name
    )
    ai_settings.validate()
    return ai_settings


def get_database_connection_string() -> str:
    """Get database connection string from settings.
    
    Returns:
        Database connection string
        
    Raises:
        ValueError: If connection string is not configured
    """
    connection_string = settings.DB_CONNECTION_STRING
    if not connection_string:
        raise ValueError("Database connection string is not configured. Set DB_CONNECTION_STRING environment variable.")
    return connection_string


def get_project_client() -> AIProjectClient:
    """Create and return an Azure AI Project client.
    
    Returns:
        AIProjectClient instance
    """
    connection_string = settings.AZURE_AI_PROJECT_CONNECTION_STRING
    if not connection_string:
        raise ValueError("Azure AI Project connection string is not configured")
    
    credential = DefaultAzureCredential(
        exclude_environment_credential=True,
        exclude_managed_identity_credential=True
    )
    
    return AIProjectClient.from_connection_string(
        conn_str=connection_string,
        credential=credential
    )
