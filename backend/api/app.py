"""
Disease Surveillance AI Agent System - FastAPI Application
Main FastAPI application with CORS, middleware, and health checks
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Disease Surveillance AI Agent System",
    description="AI-driven disease surveillance system using Azure AI Agent Service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js frontend
        "http://localhost:8501",  # Streamlit dashboard
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("="*60)
    logger.info("Disease Surveillance AI Agent System Starting...")
    logger.info("="*60)
    logger.info(f"API Documentation: http://localhost:8000/docs")
    logger.info(f"Alternative Docs: http://localhost:8000/redoc")
    logger.info("="*60)


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Disease Surveillance AI Agent System Shutting Down...")


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "message": "Disease Surveillance AI Agent System API",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat(),
            "docs": "/docs",
            "endpoints": {
                "chat": "/api/chat",
                "surveillance_status": "/api/surveillance/status",
                "anomalies": "/api/anomalies",
                "predictions": "/api/predictions",
                "alerts": "/api/alerts",
                "reports": "/api/reports",
                "thinking_logs": "/api/thinking-logs/{session_id}",
                "data_sources": "/api/data-sources"
            }
        }
    )


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "api": "up",
                "database": "checking...",
                "agents": "checking...",
                "plugins": "checking..."
            }
        }
    )


# Import and include routers
from api.endpoints import router as api_router
app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
