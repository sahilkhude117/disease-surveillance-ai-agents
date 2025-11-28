"""
Disease Surveillance AI Agent System - API Server
Uvicorn server startup script
"""

import uvicorn
import logging
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('surveillance_api.log')
    ]
)

logger = logging.getLogger(__name__)


def start_server(
    host: str = "0.0.0.0",
    port: int = 8000,
    reload: bool = False,
    workers: int = 1
):
    """
    Start the FastAPI server
    
    Args:
        host: Host address to bind to
        port: Port number to listen on
        reload: Enable auto-reload for development
        workers: Number of worker processes (production)
    """
    
    logger.info("="*60)
    logger.info("Disease Surveillance AI Agent System")
    logger.info("API Server Starting...")
    logger.info("="*60)
    logger.info(f"Host: {host}")
    logger.info(f"Port: {port}")
    logger.info(f"Reload: {reload}")
    logger.info(f"Workers: {workers}")
    logger.info("="*60)
    logger.info(f"API Documentation: http://localhost:{port}/docs")
    logger.info(f"Alternative Docs: http://localhost:{port}/redoc")
    logger.info(f"Health Check: http://localhost:{port}/health")
    logger.info("="*60)
    
    try:
        uvicorn.run(
            "api.app:app",
            host=host,
            port=port,
            reload=reload,
            workers=workers if not reload else 1,  # Workers don't work with reload
            log_level="info",
            access_log=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Disease Surveillance AI Agent System API Server"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host address (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port number (default: 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of worker processes for production (default: 1)"
    )
    
    args = parser.parse_args()
    
    start_server(
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers
    )
