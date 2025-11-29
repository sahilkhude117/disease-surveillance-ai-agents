"""Anomaly detection plugin for identifying unusual disease patterns."""

import json
from datetime import datetime
from models.anomaly_detector import AnomalyDetector
from utils.database_utils import get_surveillance_data, save_anomaly_detection
from utils.data_processing import calculate_baseline_statistics


class AnomalyDetectionPlugin:
    """Plugin for detecting anomalies in surveillance data."""
    
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.detector = AnomalyDetector(threshold=0.75)
    
    def detect_anomalies(self, days: int = 7, region: str = None, 
                        detection_method: str = "all") -> str:
        """Detects anomalies in disease surveillance data.
        
        Args:
            days: Number of days of data to analyze (default 7)
            region: Optional region filter
            detection_method: Method to use - "statistical", "ml", "temporal", or "all" (default)
            
        Returns:
            JSON string with detected anomalies
        """
        try:
            print(f"Running anomaly detection with method: {detection_method}")
            
            # Get surveillance data
            surveillance_data = get_surveillance_data(
                self.connection_string,
                days=days,
                region=region
            )
            
            # Calculate baseline for each data source
            baseline_weeks = 8  # Use 8 weeks for baseline
            baseline_data = get_surveillance_data(
                self.connection_string,
                days=baseline_weeks * 7,
                region=region
            )
            
            all_anomalies = []
            
            # Process each data source
            for source_name, source_key in [
                ('Hospital Visits', 'hospital'),
                ('Social Media', 'social_media'),
                ('Environmental', 'environmental'),
                ('Pharmacy Sales', 'pharmacy')
            ]:
                if source_key not in surveillance_data or surveillance_data[source_key].empty:
                    print(f"No data available for {source_name}")
                    continue
                
                # Fit baseline if we have historical data
                if source_key in baseline_data and not baseline_data[source_key].empty:
                    baseline_stats = calculate_baseline_statistics(
                        baseline_data[source_key],
                        lookback_weeks=baseline_weeks
                    )
                    self.detector.fit_baseline(baseline_data[source_key], source_name)
                
                current_data = surveillance_data[source_key]
                
                # Run anomaly detection based on method
                if detection_method == "statistical":
                    anomalies = self.detector.detect_statistical_anomalies(
                        current_data, 
                        source_name,
                        method='zscore'
                    )
                elif detection_method == "ml":
                    anomalies = self.detector.detect_ml_anomalies(
                        current_data,
                        source_name
                    )
                elif detection_method == "temporal":
                    anomalies = self.detector.detect_temporal_anomalies(
                        current_data,
                        source_name
                    )
                else:  # "all"
                    anomalies = self.detector.detect_all_anomalies(
                        current_data,
                        source_name
                    )
                
                all_anomalies.extend(anomalies)
            
            # Save anomalies to database
            if all_anomalies:
                try:
                    save_anomaly_detection(
                        self.connection_string,
                        all_anomalies,
                        session_id=datetime.now().strftime("%Y%m%d_%H%M%S")
                    )
                    print(f"Saved {len(all_anomalies)} anomalies to database")
                except Exception as save_error:
                    print(f"Error saving anomalies: {save_error}")
            
            # Prepare result
            result = {
                "detection_timestamp": datetime.now().isoformat(),
                "time_period_days": days,
                "region": region or "all_regions",
                "detection_method": detection_method,
                "total_anomalies_detected": len(all_anomalies),
                "anomalies": all_anomalies,
                "severity_breakdown": {
                    "critical": sum(1 for a in all_anomalies if a.get('severity') == 'critical'),
                    "high": sum(1 for a in all_anomalies if a.get('severity') == 'high'),
                    "medium": sum(1 for a in all_anomalies if a.get('severity') == 'medium'),
                    "low": sum(1 for a in all_anomalies if a.get('severity') == 'low')
                }
            }
            
            return json.dumps(result, default=str)
            
        except Exception as e:
            print(f"Error in detect_anomalies: {e}")
            import traceback
            traceback.print_exc()
            return json.dumps({
                "error": str(e),
                "status": "anomaly_detection_failed"
            })
    
    def detect_statistical_anomalies(self, days: int = 7, region: str = None,
                                    method: str = "zscore") -> str:
        """Detects anomalies using statistical methods (Z-score, IQR, Modified Z-score).
        
        Args:
            days: Number of days of data to analyze
            region: Optional region filter
            method: Statistical method - "zscore", "iqr", or "modified_zscore"
            
        Returns:
            JSON string with detected anomalies
        """
        return self.detect_anomalies(days, region, "statistical")
    
    def detect_ml_anomalies(self, days: int = 7, region: str = None) -> str:
        """Detects anomalies using ML-based Isolation Forest.
        
        Args:
            days: Number of days of data to analyze
            region: Optional region filter
            
        Returns:
            JSON string with detected anomalies
        """
        return self.detect_anomalies(days, region, "ml")
    
    def detect_temporal_anomalies(self, days: int = 7, region: str = None) -> str:
        """Detects temporal anomalies like rapid increases or sustained trends.
        
        Args:
            days: Number of days of data to analyze
            region: Optional region filter
            
        Returns:
            JSON string with detected anomalies
        """
        return self.detect_anomalies(days, region, "temporal")
    
    def get_recent_anomalies(self, days: int = 7, severity: str = None, 
                            region: str = None) -> str:
        """Retrieves recent anomaly detections from the database.
        
        Args:
            days: Number of days to look back
            severity: Optional severity filter (critical, high, medium, low)
            region: Optional region filter
            
        Returns:
            JSON string with recent anomalies
        """
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            
            conn = psycopg2.connect(self.connection_string)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Build query with filters
            query = """
                SELECT 
                    anomaly_id, timestamp, location, anomaly_type, severity,
                    confidence, data_source, baseline_value, current_value,
                    deviation_percent, detection_method, metrics, created_date
                FROM anomaly_detections
                WHERE created_date >= NOW() - INTERVAL '%s days'
            """
            params = [days]
            
            if severity:
                query += " AND severity = %s"
                params.append(severity)
            
            if region:
                query += " AND location LIKE %s"
                params.append(f"%{region}%")
            
            query += " ORDER BY created_date DESC, confidence DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            anomalies = []
            for row in rows:
                anomalies.append(dict(row))
            
            cursor.close()
            conn.close()
            
            result = {
                "query_timestamp": datetime.now().isoformat(),
                "time_period_days": days,
                "filters": {
                    "severity": severity,
                    "region": region
                },
                "total_anomalies": len(anomalies),
                "anomalies": anomalies
            }
            
            return json.dumps(result, default=str)
            
        except Exception as e:
            print(f"Error in get_recent_anomalies: {e}")
            return json.dumps({"error": str(e)})
    
    def update_baseline(self, lookback_weeks: int = 8, region: str = None) -> str:
        """Updates the baseline statistics for anomaly detection.
        
        Args:
            lookback_weeks: Number of weeks to use for baseline calculation
            region: Optional region filter
            
        Returns:
            JSON string with update status
        """
        try:
            # Get baseline data
            baseline_data = get_surveillance_data(
                self.connection_string,
                days=lookback_weeks * 7,
                region=region
            )
            
            updated_sources = []
            
            for source_name, source_key in [
                ('Hospital Visits', 'hospital'),
                ('Social Media', 'social_media'),
                ('Environmental', 'environmental'),
                ('Pharmacy Sales', 'pharmacy')
            ]:
                if source_key in baseline_data and not baseline_data[source_key].empty:
                    self.detector.fit_baseline(baseline_data[source_key], source_name)
                    updated_sources.append(source_name)
                    print(f"Updated baseline for {source_name}")
            
            result = {
                "update_timestamp": datetime.now().isoformat(),
                "lookback_weeks": lookback_weeks,
                "region": region or "all_regions",
                "updated_sources": updated_sources,
                "status": "success" if updated_sources else "no_data_available"
            }
            
            return json.dumps(result, default=str)
            
        except Exception as e:
            print(f"Error in update_baseline: {e}")
            return json.dumps({
                "error": str(e),
                "status": "baseline_update_failed"
            })
