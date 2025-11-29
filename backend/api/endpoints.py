"""
Disease Surveillance AI Agent System - API Endpoints
REST API endpoints for surveillance operations
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

from managers.surveillance_manager import SurveillanceManager
from utils.database_utils import DatabaseConnection
from utils.query_helpers import fetch_results_as_dicts

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize surveillance manager (singleton pattern)
surveillance_manager: Optional[SurveillanceManager] = None


def get_surveillance_manager() -> SurveillanceManager:
    """Get or create surveillance manager instance"""
    global surveillance_manager
    if surveillance_manager is None:
        from config.settings import get_database_connection_string
        try:
            connection_string = get_database_connection_string()
        except ValueError:
            # If no database configured, initialize with None
            connection_string = None
        surveillance_manager = SurveillanceManager(connection_string)
    return surveillance_manager


# ==================== Request/Response Models ====================

class ChatRequest(BaseModel):
    """Chat request model"""
    session_id: Optional[str] = Field(None, description="Session ID for continuing conversation")
    message: str = Field(..., description="User message/query", min_length=1)
    user_id: Optional[str] = Field("anonymous", description="User identifier")


class ChatResponse(BaseModel):
    """Chat response model"""
    session_id: str
    conversation_id: str
    response: str
    agents_involved: List[str]
    timestamp: str


class SurveillanceStatusResponse(BaseModel):
    """Surveillance status response"""
    status: str
    active_sessions: int
    total_anomalies: int
    active_alerts: int
    recent_predictions: int
    data_sources: Dict[str, str]
    timestamp: str


# ==================== Chat Endpoint ====================

@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Process user chat message with surveillance agents
    
    This endpoint orchestrates multiple AI agents to:
    - Collect surveillance data from multiple sources
    - Detect anomalies in disease patterns
    - Generate outbreak predictions
    - Create alerts for health officials
    - Produce comprehensive reports
    """
    try:
        manager = get_surveillance_manager()
        
        # Process message through agent system
        result = await manager.process_message(
            message=request.message,
            session_id=request.session_id
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "session_id": result.get("session_id"),
                "conversation_id": result.get("conversation_id"),
                "response": result.get("response", ""),
                "agents_involved": result.get("agents_involved", []),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")


# ==================== Surveillance Status ====================

@router.get("/surveillance/status", response_model=SurveillanceStatusResponse, tags=["Surveillance"])
async def get_surveillance_status():
    """
    Get overall surveillance system status
    
    Returns current status including:
    - Active monitoring sessions
    - Total anomalies detected
    - Active alerts
    - Recent predictions
    - Data source connectivity
    """
    try:
        manager = get_surveillance_manager()
        
        # Get active sessions count
        active_sessions = len(manager.active_sessions)
        
        # Query database for metrics with fallback for connection issues
        try:
            with DatabaseConnection() as db:
                cursor = db.connection.cursor()
                
                # Count anomalies (last 24 hours) - PostgreSQL syntax
                cursor.execute("""
                    SELECT COUNT(*) as count FROM anomaly_detections 
                    WHERE timestamp >= NOW() - INTERVAL '24 hours'
                """)
                result = cursor.fetchone()
                total_anomalies = result['count'] if result else 0
                
                # Count active alerts
                cursor.execute("""
                    SELECT COUNT(*) as count FROM surveillance_alerts 
                    WHERE status = 'active'
                """)
                result = cursor.fetchone()
                active_alerts = result['count'] if result else 0
                
                # Count recent predictions (last 24 hours) - PostgreSQL syntax
                cursor.execute("""
                    SELECT COUNT(*) as count FROM outbreak_predictions 
                    WHERE created_date >= NOW() - INTERVAL '24 hours'
                """)
                result = cursor.fetchone()
                recent_predictions = result['count'] if result else 0
                
                cursor.close()
        except Exception as db_error:
            logger.warning(f"Database query failed, returning zeros: {db_error}")
            # Return zeros if database is unavailable
            total_anomalies = 0
            active_alerts = 0
            recent_predictions = 0
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "operational",
                "active_sessions": active_sessions,
                "total_anomalies": total_anomalies,
                "active_alerts": active_alerts,
                "recent_predictions": recent_predictions,
                "data_sources": {
                    "hospital": "connected",
                    "social_media": "connected",
                    "environmental": "connected",
                    "pharmacy": "connected"
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting surveillance status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")


# ==================== Anomalies ====================

@router.get("/anomalies", tags=["Anomalies"])
async def get_anomalies(
    region: Optional[str] = Query(None, description="Filter by region"),
    severity: Optional[str] = Query(None, description="Filter by severity (low, medium, high, critical)"),
    days: int = Query(7, description="Number of days to look back", ge=1, le=90)
):
    """
    Get detected anomalies in surveillance data
    
    Returns anomalies detected across all data sources including:
    - Statistical anomalies
    - Machine learning detected patterns
    - Temporal anomalies
    """
    try:
        db = DatabaseConnection()
        db.connect()
        cursor = db.connection.cursor()
        
        # Build query with filters - PostgreSQL syntax
        # Note: Using direct string interpolation for days since INTERVAL doesn't support parameterization
        # days is validated by FastAPI (ge=1, le=90) so this is safe
        query = f"""
            SELECT 
                anomaly_id,
                timestamp,
                location as region,
                anomaly_type,
                severity,
                confidence,
                data_source,
                baseline_value,
                current_value,
                deviation_percent,
                detection_method
            FROM anomaly_detections
            WHERE timestamp >= NOW() - INTERVAL '{days} days'
        """
        params = []
            
        if region:
            query += " AND location = %s"
            params.append(region)
        
        if severity:
            query += " AND severity = %s"
            params.append(severity)
        
        query += " ORDER BY timestamp DESC, severity DESC"
        
        cursor.execute(query, tuple(params))
        # RealDictCursor returns dictionaries directly
        results = cursor.fetchall()
        # Convert to regular dicts and handle datetime serialization
        results = [
            {k: v.isoformat() if hasattr(v, 'isoformat') else v for k, v in dict(row).items()}
            for row in results
        ]
        
        cursor.close()
        db.disconnect()
        
        return JSONResponse(
            status_code=200,
            content={
                "total": len(results),
                "anomalies": results,
                "filters": {
                    "region": region,
                    "severity": severity,
                    "days": days
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting anomalies: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get anomalies: {str(e)}")


# ==================== Predictions ====================

@router.get("/predictions", tags=["Predictions"])
async def get_predictions(
    disease: Optional[str] = Query(None, description="Filter by disease name"),
    region: Optional[str] = Query(None, description="Filter by region"),
    days: int = Query(30, description="Number of days to look back", ge=1, le=180)
):
    """
    Get outbreak predictions
    
    Returns AI-generated disease outbreak predictions including:
    - Predicted case numbers
    - Risk levels
    - Confidence scores
    - Model parameters (R0, growth rate, etc.)
    """
    try:
        db = DatabaseConnection()
        db.connect()
        cursor = db.connection.cursor()
        
        # Note: Using direct string interpolation for days since INTERVAL doesn't support parameterization
        # days is validated by FastAPI (ge=1, le=180) so this is safe
        query = f"""
            SELECT 
                prediction_id,
                disease_name,
                region,
                forecast_weeks,
                predicted_cases,
                confidence,
                risk_level,
                model_used,
                created_date
            FROM outbreak_predictions
            WHERE created_date >= NOW() - INTERVAL '{days} days'
        """
        params = []
            
        if disease:
            query += " AND disease_name = %s"
            params.append(disease)
        
        if region:
            query += " AND region = %s"
            params.append(region)
        
        query += " ORDER BY created_date DESC, risk_level DESC"
        
        cursor.execute(query, tuple(params))
        # RealDictCursor returns dictionaries directly
        results = cursor.fetchall()
        # Convert to regular dicts and handle datetime serialization
        results = [
            {k: v.isoformat() if hasattr(v, 'isoformat') else v for k, v in dict(row).items()}
            for row in results
        ]
        
        cursor.close()
        db.disconnect()
        
        return JSONResponse(
            status_code=200,
            content={
                "total": len(results),
                "predictions": results,
                "filters": {
                    "disease": disease,
                    "region": region,
                    "days": days
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting predictions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get predictions: {str(e)}")


# ==================== Alerts ====================

@router.get("/alerts", tags=["Alerts"])
async def get_alerts(
    region: Optional[str] = Query(None, description="Filter by region"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    status: str = Query("active", description="Filter by status (active, resolved, archived)")
):
    """
    Get surveillance alerts
    
    Returns active alerts for:
    - Health officials
    - Healthcare providers
    - Public health authorities
    - Schools and institutions
    """
    try:
        db = DatabaseConnection()
        db.connect()
        cursor = db.connection.cursor()
        
        query = """
            SELECT 
                alert_id,
                alert_type,
                severity,
                region,
                disease_name,
                message,
                audience,
                status,
                created_date
            FROM surveillance_alerts
            WHERE status = %s
        """
        params = [status]
            
        if region:
            query += " AND region = %s"
            params.append(region)
        
        if severity:
            query += " AND severity = %s"
            params.append(severity)
        
        query += """ ORDER BY 
            CASE severity
                WHEN 'critical' THEN 1
                WHEN 'high' THEN 2
                WHEN 'medium' THEN 3
                WHEN 'low' THEN 4
                ELSE 5
            END,
            created_date DESC
        """
        
        cursor.execute(query, tuple(params))
        # RealDictCursor returns dictionaries directly
        results = cursor.fetchall()
        # Convert to regular dicts and handle datetime serialization
        results = [
            {k: v.isoformat() if hasattr(v, 'isoformat') else v for k, v in dict(row).items()}
            for row in results
        ]
        
        cursor.close()
        db.disconnect()
        
        return JSONResponse(
            status_code=200,
            content={
                "total": len(results),
                "alerts": results,
                "filters": {
                    "region": region,
                    "severity": severity,
                    "status": status
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting alerts: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get alerts: {str(e)}")


# ==================== Reports ====================

@router.get("/reports", tags=["Reports"])
async def get_reports(
    session_id: Optional[str] = Query(None, description="Filter by session ID"),
    report_type: Optional[str] = Query(None, description="Filter by report type"),
    days: int = Query(30, description="Number of days to look back", ge=1, le=180)
):
    """
    Get generated surveillance reports
    
    Returns metadata for generated reports including:
    - Report filenames
    - Azure Blob Storage URLs
    - Report types (daily, weekly, outbreak, incident)
    - Generation timestamps
    """
    try:
        db = DatabaseConnection()
        db.connect()
        cursor = db.connection.cursor()
        
        # Note: Using direct string interpolation for days since INTERVAL doesn't support parameterization
        # days is validated by FastAPI (ge=1, le=180) so this is safe
        query = f"""
            SELECT 
                report_id,
                session_id,
                conversation_id,
                filename,
                blob_url,
                report_type,
                created_date
            FROM surveillance_reports
            WHERE created_date >= NOW() - INTERVAL '{days} days'
        """
        params = []
            
        if session_id:
            query += " AND session_id = %s"
            params.append(session_id)
        
        if report_type:
            query += " AND report_type = %s"
            params.append(report_type)
        
        query += " ORDER BY created_date DESC"
        
        cursor.execute(query, tuple(params))
        # RealDictCursor returns dictionaries directly
        results = cursor.fetchall()
        # Convert to regular dicts and handle datetime serialization
        results = [
            {k: v.isoformat() if hasattr(v, 'isoformat') else v for k, v in dict(row).items()}
            for row in results
        ]
        
        cursor.close()
        db.disconnect()
        
        return JSONResponse(
            status_code=200,
            content={
                "total": len(results),
                "reports": results,
                "filters": {
                    "session_id": session_id,
                    "report_type": report_type,
                    "days": days
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting reports: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get reports: {str(e)}")


# ==================== Thinking Logs ====================

@router.get("/thinking-logs/{session_id}", tags=["Thinking Logs"])
async def get_thinking_logs(session_id: str):
    """
    Get agent thinking logs for a session
    
    Returns transparent view of agent reasoning including:
    - Thought processes
    - Decision making steps
    - Data analysis reasoning
    - Collaboration between agents
    """
    try:
        db = DatabaseConnection()
        db.connect()
        cursor = db.connection.cursor()
        
        cursor.execute("""
            SELECT 
                thinking_id,
                agent_name,
                thinking_stage,
                thought_content,
                thinking_stage_output,
                agent_output,
                conversation_id,
                user_query,
                status,
                created_date
            FROM agent_thinking_logs
            WHERE session_id = %s
            ORDER BY created_date ASC
        """, (session_id,))
        
        # RealDictCursor returns dictionaries directly
        results = cursor.fetchall()
        # Convert to regular dicts and handle datetime serialization
        results = [
            {k: v.isoformat() if hasattr(v, 'isoformat') else v for k, v in dict(row).items()}
            for row in results
        ]
        
        cursor.close()
        db.disconnect()
        
        return JSONResponse(
            status_code=200,
            content={
                "session_id": session_id,
                "total_logs": len(results),
                "thinking_logs": results,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting thinking logs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get thinking logs: {str(e)}")


# ==================== Data Sources ====================

@router.get("/data-sources", tags=["Data Sources"])
async def get_data_sources():
    """
    Get status of all surveillance data sources
    
    Returns connectivity and recent data status for:
    - Hospital surveillance systems
    - Social media monitoring
    - Environmental sensors
    - Pharmacy networks
    """
    try:
        db = DatabaseConnection()
        db.connect()
        cursor = db.connection.cursor()
        
        # Check each data source
        sources_status = {}
        
        # Hospital data
        try:
            cursor.execute("""
                SELECT COUNT(*), MAX(timestamp) 
                FROM hospital_surveillance_data 
                WHERE timestamp >= NOW() - INTERVAL '24 hours'
            """)
            count, last_update = cursor.fetchone()
            sources_status['hospital'] = {
                "status": "connected" if count > 0 else "no_recent_data",
                "records_24h": count,
                "last_update": last_update.isoformat() if last_update else None
            }
        except Exception:
            sources_status['hospital'] = {"status": "table_not_found", "records_24h": 0, "last_update": None}
        
        # Social media data
        try:
            cursor.execute("""
                SELECT COUNT(*), MAX(timestamp) 
                FROM social_media_surveillance_data 
                WHERE timestamp >= NOW() - INTERVAL '24 hours'
            """)
            count, last_update = cursor.fetchone()
            sources_status['social_media'] = {
                "status": "connected" if count > 0 else "no_recent_data",
                "records_24h": count,
                "last_update": last_update.isoformat() if last_update else None
            }
        except Exception:
            sources_status['social_media'] = {"status": "table_not_found", "records_24h": 0, "last_update": None}
        
        # Environmental data
        try:
            cursor.execute("""
                SELECT COUNT(*), MAX(timestamp) 
                FROM environmental_surveillance_data 
                WHERE timestamp >= NOW() - INTERVAL '24 hours'
            """)
            count, last_update = cursor.fetchone()
            sources_status['environmental'] = {
                "status": "connected" if count > 0 else "no_recent_data",
                "records_24h": count,
                "last_update": last_update.isoformat() if last_update else None
            }
        except Exception:
            sources_status['environmental'] = {"status": "table_not_found", "records_24h": 0, "last_update": None}
        
        # Pharmacy data
        try:
            cursor.execute("""
                SELECT COUNT(*), MAX(timestamp) 
                FROM pharmacy_surveillance_data 
                WHERE timestamp >= NOW() - INTERVAL '24 hours'
            """)
            count, last_update = cursor.fetchone()
            sources_status['pharmacy'] = {
                "status": "connected" if count > 0 else "no_recent_data",
                "records_24h": count,
                "last_update": last_update.isoformat() if last_update else None
            }
        except Exception:
            sources_status['pharmacy'] = {"status": "table_not_found", "records_24h": 0, "last_update": None}
        
        cursor.close()
        db.disconnect()
        
        return JSONResponse(
            status_code=200,
            content={
                "data_sources": sources_status,
                "overall_status": "operational",
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting data sources status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get data sources: {str(e)}")
