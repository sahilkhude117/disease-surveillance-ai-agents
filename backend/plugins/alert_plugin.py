"""Alert plugin for generating and managing disease surveillance alerts."""

import json
from datetime import datetime
from utils.database_utils import save_alert


class AlertPlugin:
    """Plugin for generating and managing surveillance alerts."""
    
    def __init__(self, connection_string):
        self.connection_string = connection_string
    
    def generate_alert(self, alert_type: str, severity: str, region: str,
                      disease_name: str, message: str, audience: str = "all") -> str:
        """Generates a disease surveillance alert.
        
        Args:
            alert_type: Type of alert (e.g., "outbreak", "anomaly", "prediction")
            severity: Severity level ("critical", "high", "medium", "low")
            region: Affected region
            disease_name: Name of the disease
            message: Alert message content
            audience: Target audience ("officials", "providers", "public", "schools", "all")
            
        Returns:
            JSON string with alert details
        """
        try:
            print(f"Generating {severity} alert for {disease_name} in {region}")
            
            # Create alert structure
            alert = {
                "alert_id": f"ALERT_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "timestamp": datetime.now().isoformat(),
                "alert_type": alert_type,
                "severity": severity,
                "region": region,
                "disease": disease_name,
                "message": message,
                "audience": audience,
                "status": "active",
                "response_actions": self._generate_response_actions(severity, alert_type),
                "communication_channels": self._get_communication_channels(audience),
                "expiry_date": self._calculate_expiry(severity)
            }
            
            # Generate audience-specific messages
            alert['audience_messages'] = self._generate_audience_messages(
                alert_type, severity, region, disease_name, message, audience
            )
            
            # Save alert to database
            try:
                save_alert(
                    self.connection_string,
                    alert_data={
                        "alert_type": alert_type,
                        "severity": severity,
                        "region": region,
                        "disease_name": disease_name,
                        "message": message,
                        "audience": audience,
                        "status": "active",
                        "alert_json": json.dumps(alert)
                    },
                    session_id=datetime.now().strftime("%Y%m%d_%H%M%S")
                )
                print(f"Saved alert to database: {alert['alert_id']}")
            except Exception as save_error:
                print(f"Error saving alert: {save_error}")
            
            return json.dumps(alert, default=str)
            
        except Exception as e:
            print(f"Error in generate_alert: {e}")
            import traceback
            traceback.print_exc()
            return json.dumps({
                "error": str(e),
                "status": "alert_generation_failed"
            })
    
    def _generate_response_actions(self, severity: str, alert_type: str) -> list:
        """Generates recommended response actions based on severity."""
        actions = {
            "critical": [
                "Activate emergency response teams immediately",
                "Deploy rapid response medical units",
                "Establish emergency treatment centers",
                "Implement mandatory containment measures",
                "Issue emergency public health orders"
            ],
            "high": [
                "Increase hospital readiness levels",
                "Enhance surveillance monitoring",
                "Activate contact tracing protocols",
                "Prepare additional medical resources",
                "Issue public health advisories"
            ],
            "medium": [
                "Monitor situation closely",
                "Increase data collection frequency",
                "Review healthcare capacity",
                "Prepare contingency plans",
                "Alert healthcare providers"
            ],
            "low": [
                "Continue routine surveillance",
                "Monitor for escalation signs",
                "Maintain standard protocols",
                "Update stakeholders"
            ]
        }
        
        return actions.get(severity, actions['medium'])
    
    def _get_communication_channels(self, audience: str) -> list:
        """Determines appropriate communication channels for audience."""
        channels = {
            "officials": ["email", "secure_portal", "emergency_hotline"],
            "providers": ["email", "provider_network", "medical_alerts"],
            "public": ["social_media", "news_media", "public_website", "sms"],
            "schools": ["email", "school_portal", "parent_notification"],
            "all": ["email", "social_media", "news_media", "public_website"]
        }
        
        return channels.get(audience, channels['all'])
    
    def _calculate_expiry(self, severity: str) -> str:
        """Calculates alert expiry based on severity."""
        from datetime import timedelta
        
        expiry_days = {
            "critical": 1,
            "high": 3,
            "medium": 7,
            "low": 14
        }
        
        days = expiry_days.get(severity, 7)
        expiry_date = datetime.now() + timedelta(days=days)
        return expiry_date.isoformat()
    
    def _generate_audience_messages(self, alert_type: str, severity: str, 
                                   region: str, disease_name: str, 
                                   message: str, audience: str) -> dict:
        """Generates tailored messages for different audiences."""
        messages = {}
        
        if audience in ["officials", "all"]:
            messages["officials"] = {
                "subject": f"{severity.upper()} ALERT: {disease_name} - {region}",
                "body": f"""
OFFICIAL HEALTH ALERT

Alert Type: {alert_type}
Severity: {severity}
Disease: {disease_name}
Region: {region}

SITUATION SUMMARY:
{message}

RECOMMENDED ACTIONS:
- Review attached technical briefing
- Activate appropriate response protocols
- Coordinate with regional health authorities
- Monitor situation updates via secure portal

This is an official health alert. Immediate action may be required.
                """.strip(),
                "attachments": ["technical_briefing.pdf", "data_summary.xlsx"]
            }
        
        if audience in ["providers", "all"]:
            messages["providers"] = {
                "subject": f"Clinical Alert: {disease_name} in {region}",
                "body": f"""
CLINICAL ALERT FOR HEALTHCARE PROVIDERS

Disease: {disease_name}
Affected Region: {region}
Alert Level: {severity}

CLINICAL GUIDANCE:
{message}

PROVIDER ACTIONS:
- Increase vigilance for symptomatic patients
- Follow enhanced infection control protocols
- Report suspected cases immediately
- Review clinical guidelines at [portal link]

For clinical questions, contact: health.alert@surveillance.gov
                """.strip()
            }
        
        if audience in ["public", "all"]:
            messages["public"] = {
                "subject": f"Health Advisory: {disease_name}",
                "body": f"""
PUBLIC HEALTH ADVISORY

The health department is monitoring increased {disease_name} activity in {region}.

WHAT YOU NEED TO KNOW:
{message}

WHAT YOU CAN DO:
- Practice good hygiene (handwashing, sanitization)
- Stay home if you feel unwell
- Seek medical attention if symptoms develop
- Follow local health guidelines

For more information: www.health.gov/alerts
                """.strip()
            }
        
        if audience in ["schools", "all"]:
            messages["schools"] = {
                "subject": f"School Health Notice: {disease_name}",
                "body": f"""
SCHOOL HEALTH NOTICE

Disease Activity: {disease_name}
Region: {region}
Alert Level: {severity}

SITUATION:
{message}

SCHOOL ACTIONS:
- Monitor student absences for illness patterns
- Enhance cleaning and sanitation protocols
- Review illness reporting procedures
- Communicate with parents as needed

Contact school health coordinator for guidance.
                """.strip()
            }
        
        return messages
    
    def get_active_alerts(self, region: str = None, severity: str = None, 
                         disease: str = None) -> str:
        """Retrieves active alerts from the database.
        
        Args:
            region: Optional region filter
            severity: Optional severity filter
            disease: Optional disease filter
            
        Returns:
            JSON string with active alerts
        """
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            
            conn = psycopg2.connect(self.connection_string)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT 
                    alert_id, alert_type, severity, region, disease_name,
                    message, audience, status, alert_json, created_date
                FROM surveillance_alerts
                WHERE status = 'active'
            """
            params = []
            
            if region:
                query += " AND region = %s"
                params.append(region)
            
            if severity:
                query += " AND severity = %s"
                params.append(severity)
            
            if disease:
                query += " AND disease_name = %s"
                params.append(disease)
            
            query += " ORDER BY CASE severity WHEN 'critical' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 ELSE 4 END, created_date DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            alerts = []
            for row in rows:
                alerts.append(dict(row))
            
            cursor.close()
            conn.close()
            
            result = {
                "query_timestamp": datetime.now().isoformat(),
                "filters": {
                    "region": region,
                    "severity": severity,
                    "disease": disease
                },
                "total_active_alerts": len(alerts),
                "alerts_by_severity": {
                    "critical": sum(1 for a in alerts if a.get('severity') == 'critical'),
                    "high": sum(1 for a in alerts if a.get('severity') == 'high'),
                    "medium": sum(1 for a in alerts if a.get('severity') == 'medium'),
                    "low": sum(1 for a in alerts if a.get('severity') == 'low')
                },
                "alerts": alerts
            }
            
            return json.dumps(result, default=str)
            
        except Exception as e:
            print(f"Error in get_active_alerts: {e}")
            return json.dumps({"error": str(e)})
    
    def update_alert_status(self, alert_id: str, new_status: str, 
                           notes: str = None) -> str:
        """Updates the status of an alert.
        
        Args:
            alert_id: ID of the alert to update
            new_status: New status ("active", "resolved", "expired", "cancelled")
            notes: Optional notes about the status change
            
        Returns:
            JSON string with update result
        """
        try:
            import psycopg2
            
            conn = psycopg2.connect(self.connection_string)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE surveillance_alerts
                SET status = %s, 
                    updated_date = NOW()
                WHERE alert_id = %s
            """, (new_status, alert_id))
            
            rows_affected = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            
            result = {
                "update_timestamp": datetime.now().isoformat(),
                "alert_id": alert_id,
                "new_status": new_status,
                "notes": notes,
                "success": rows_affected > 0,
                "rows_affected": rows_affected
            }
            
            return json.dumps(result, default=str)
            
        except Exception as e:
            print(f"Error in update_alert_status: {e}")
            return json.dumps({"error": str(e)})
