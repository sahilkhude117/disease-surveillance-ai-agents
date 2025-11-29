"""Database utility functions for disease surveillance."""

import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from datetime import datetime
from typing import Optional, Dict, List, Any
from config.settings import settings


class DatabaseConnection:
    """Manages database connections for disease surveillance data."""
    
    def __init__(self, connection_string: Optional[str] = None):
        """Initialize database connection.
        
        Args:
            connection_string: Database connection string. Uses settings if not provided.
        """
        self.connection_string = connection_string or settings.DB_CONNECTION_STRING
        self.connection = None
    
    def connect(self):
        """Establish database connection."""
        try:
            self.connection = psycopg2.connect(
                self.connection_string,
                cursor_factory=RealDictCursor
            )
            return self.connection
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def disconnect(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query: str, params: tuple = None) -> pd.DataFrame:
        """Execute a SELECT query and return results as DataFrame.
        
        Args:
            query: SQL query to execute
            params: Query parameters
            
        Returns:
            DataFrame with query results
        """
        try:
            if not self.connection:
                self.connect()
            
            if params:
                df = pd.read_sql(query, self.connection, params=params)
            else:
                df = pd.read_sql(query, self.connection)
            
            return df
        except Exception as e:
            print(f"Error executing query: {e}")
            raise
    
    def execute_non_query(self, query: str, params: tuple = None) -> int:
        """Execute an INSERT, UPDATE, or DELETE query.
        
        Args:
            query: SQL query to execute
            params: Query parameters (use %s placeholders for PostgreSQL)
            
        Returns:
            Number of rows affected
        """
        try:
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            self.connection.commit()
            rowcount = cursor.rowcount
            cursor.close()
            return rowcount
        except Exception as e:
            print(f"Error executing non-query: {e}")
            if self.connection:
                self.connection.rollback()
            raise
    
    def execute_stored_procedure(self, proc_name: str, params: tuple = None) -> pd.DataFrame:
        """Execute a PostgreSQL function and return results.
        
        Args:
            proc_name: Name of PostgreSQL function
            params: Function parameters
            
        Returns:
            DataFrame with function results
        """
        try:
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor()
            # PostgreSQL function call syntax
            if params:
                placeholders = ','.join(['%s' for _ in params])
                cursor.execute(f"SELECT * FROM {proc_name}({placeholders})", params)
            else:
                cursor.execute(f"SELECT * FROM {proc_name}()")
            
            # Fetch results if available
            try:
                columns = [column[0] for column in cursor.description]
                rows = cursor.fetchall()
                df = pd.DataFrame.from_records(rows, columns=columns)
                cursor.close()
                return df
            except:
                # No results to fetch
                cursor.close()
                return pd.DataFrame()
        except Exception as e:
            print(f"Error executing PostgreSQL function: {e}")
            raise
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()


def get_surveillance_data(connection_string: str, region: Optional[str] = None, 
                         days: int = 7) -> Dict[str, pd.DataFrame]:
    """Retrieve surveillance data from database.
    
    Args:
        connection_string: Database connection string
        region: Optional region filter
        days: Number of days of historical data to retrieve
        
    Returns:
        Dictionary of DataFrames with surveillance data by source type
    """
    with DatabaseConnection(connection_string) as db:
        # Build WHERE clause (PostgreSQL syntax)
        where_clause = f"WHERE created_date >= NOW() - INTERVAL '{days} days'"
        if region:
            where_clause += f" AND region = '{region}'"
        
        # Note: Using try-except for each query to handle missing tables gracefully
        result = {}
        
        # Get hospital data
        try:
            hospital_query = f"""
                SELECT * FROM hospital_surveillance_data
                {where_clause}
                ORDER BY created_date DESC
            """
            result['hospital'] = db.execute_query(hospital_query)
        except Exception as e:
            print(f"No hospital data available: {e}")
            result['hospital'] = pd.DataFrame()
        
        # Get social media data
        try:
            social_query = f"""
                SELECT * FROM social_media_surveillance_data
                {where_clause}
                ORDER BY created_date DESC
            """
            result['social_media'] = db.execute_query(social_query)
        except Exception as e:
            print(f"No social media data available: {e}")
            result['social_media'] = pd.DataFrame()
        
        # Get environmental data
        try:
            env_query = f"""
                SELECT * FROM environmental_surveillance_data
                {where_clause}
                ORDER BY created_date DESC
            """
            result['environmental'] = db.execute_query(env_query)
        except Exception as e:
            print(f"No environmental data available: {e}")
            result['environmental'] = pd.DataFrame()
        
        # Get pharmacy data
        try:
            pharmacy_query = f"""
                SELECT * FROM pharmacy_surveillance_data
                {where_clause}
                ORDER BY created_date DESC
            """
            result['pharmacy'] = db.execute_query(pharmacy_query)
        except Exception as e:
            print(f"No pharmacy data available: {e}")
            result['pharmacy'] = pd.DataFrame()
        
        return result


def save_anomaly_detection(connection_string: str, anomalies: List[Dict[str, Any]], 
                          session_id: str = None) -> int:
    """Save detected anomalies to database.
    
    Args:
        connection_string: Database connection string
        anomalies: List of anomaly dictionaries
        session_id: Optional session ID
        
    Returns:
        Number of rows inserted
    """
    with DatabaseConnection(connection_string) as db:
        # PostgreSQL uses %s placeholders and NOW() instead of GETDATE()
        insert_query = """
            INSERT INTO anomaly_detections 
            (timestamp, location, anomaly_type, severity, confidence, 
             data_source, baseline_value, current_value, deviation_percent, 
             detection_method, metrics, session_id, created_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        
        rows_affected = 0
        for anomaly in anomalies:
            params = (
                anomaly.get('timestamp'),
                anomaly.get('location'),
                anomaly.get('type'),
                anomaly.get('severity'),
                anomaly.get('confidence'),
                anomaly.get('data_source'),
                anomaly.get('baseline_value'),
                anomaly.get('current_value'),
                anomaly.get('deviation_percent'),
                anomaly.get('detection_method'),
                str(anomaly.get('metrics', {})),
                session_id
            )
            try:
                rows_affected += db.execute_non_query(insert_query, params)
            except Exception as e:
                print(f"Error saving anomaly: {e}")
        
        return rows_affected


def save_prediction(connection_string: str, prediction_data: Dict[str, Any], 
                   session_id: str = None) -> int:
    """Save outbreak prediction to database.
    
    Args:
        connection_string: Database connection string
        prediction_data: Prediction data dictionary
        session_id: Optional session ID
        
    Returns:
        Number of rows inserted
    """
    with DatabaseConnection(connection_string) as db:
        # PostgreSQL uses %s placeholders and NOW()
        insert_query = """
            INSERT INTO outbreak_predictions
            (disease_name, region, forecast_weeks, predicted_cases, confidence,
             risk_level, model_used, prediction_json, session_id, created_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        
        params = (
            prediction_data.get('disease_name'),
            prediction_data.get('region'),
            prediction_data.get('forecast_weeks'),
            prediction_data.get('predicted_cases'),
            prediction_data.get('confidence'),
            prediction_data.get('risk_level'),
            prediction_data.get('model_used'),
            prediction_data.get('prediction_json'),
            session_id
        )
        
        try:
            return db.execute_non_query(insert_query, params)
        except Exception as e:
            print(f"Error saving prediction: {e}")
            return 0


def save_alert(connection_string: str, alert_data: Dict[str, Any], 
               session_id: str = None) -> int:
    """Save alert to database.
    
    Args:
        connection_string: Database connection string
        alert_data: Alert data dictionary
        session_id: Optional session ID
        
    Returns:
        Number of rows inserted
    """
    with DatabaseConnection(connection_string) as db:
        # PostgreSQL uses %s placeholders and NOW()
        insert_query = """
            INSERT INTO surveillance_alerts
            (alert_id, alert_type, severity, region, disease_name, message,
             audience, status, alert_json, session_id, created_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        
        params = (
            alert_data.get('alert_id') or f"ALERT_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            alert_data.get('alert_type'),
            alert_data.get('severity'),
            alert_data.get('region'),
            alert_data.get('disease_name'),
            alert_data.get('message'),
            alert_data.get('audience'),
            alert_data.get('status', 'active'),
            alert_data.get('alert_json'),
            session_id
        )
        
        try:
            return db.execute_non_query(insert_query, params)
        except Exception as e:
            print(f"Error saving alert: {e}")
            return 0


def get_thinking_logs(connection_string: str, session_id: str, 
                     conversation_id: Optional[str] = None) -> pd.DataFrame:
    """Retrieve thinking logs for a session.
    
    Args:
        connection_string: Database connection string
        session_id: Session ID
        conversation_id: Optional conversation ID filter
        
    Returns:
        DataFrame with thinking logs
    """
    with DatabaseConnection(connection_string) as db:
        # PostgreSQL uses %s placeholders
        query = """
            SELECT * FROM agent_thinking_logs
            WHERE session_id = %s
        """
        params = [session_id]
        
        if conversation_id:
            query += " AND conversation_id = %s"
            params.append(conversation_id)
        
        query += " ORDER BY created_date ASC"
        
        return db.execute_query(query, tuple(params))
