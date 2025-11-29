"""Prediction plugin for forecasting disease spread using epidemiological models."""

import json
from datetime import datetime, timedelta
from utils.database_utils import save_prediction
import numpy as np


class PredictionPlugin:
    """Plugin for predicting disease outbreak spread."""
    
    def __init__(self, connection_string):
        self.connection_string = connection_string
    
    def predict_disease_spread(self, disease_name: str, region: str, 
                              horizon_weeks: int = 2, model_type: str = "auto") -> str:
        """Predicts disease spread using epidemiological models.
        
        Args:
            disease_name: Name of the disease (e.g., "Influenza", "COVID-19")
            region: Region for prediction (e.g., "Maharashtra", "Delhi")
            horizon_weeks: Prediction horizon in weeks (1-3, default 2)
            model_type: Model type - "seir", "sir", "time_series", or "auto" (default)
            
        Returns:
            JSON string with prediction results
        """
        try:
            print(f"Generating prediction for {disease_name} in {region} for {horizon_weeks} weeks")
            
            # For now, return a structured placeholder that agents can work with
            # TODO: Integrate PandemicLLM logic and actual forecasting models
            
            from utils.database_utils import get_surveillance_data
            
            # Get recent data for context
            recent_data = get_surveillance_data(
                self.connection_string,
                days=14,
                region=region
            )
            
            # Generate prediction structure
            prediction = {
                "prediction_timestamp": datetime.now().isoformat(),
                "disease": disease_name,
                "region": region,
                "horizon_weeks": horizon_weeks,
                "model_type": model_type,
                "forecast": self._generate_forecast(disease_name, region, horizon_weeks),
                "confidence_interval": {
                    "lower_bound": 0.75,
                    "upper_bound": 0.95,
                    "confidence_level": 0.90
                },
                "risk_assessment": self._assess_outbreak_risk(disease_name, region),
                "recommendations": self._generate_recommendations(disease_name, region, horizon_weeks)
            }
            
            # Save prediction to database
            try:
                save_prediction(
                    self.connection_string,
                    prediction_data={
                        "disease_name": disease_name,
                        "region": region,
                        "forecast_weeks": horizon_weeks,
                        "predicted_cases": prediction['forecast'].get('peak_cases', 0),
                        "confidence": prediction['confidence_interval']['confidence_level'],
                        "risk_level": prediction['risk_assessment']['overall_risk'],
                        "model_used": model_type,
                        "prediction_json": json.dumps(prediction)
                    },
                    session_id=datetime.now().strftime("%Y%m%d_%H%M%S")
                )
                print(f"Saved prediction to database")
            except Exception as save_error:
                print(f"Error saving prediction: {save_error}")
            
            return json.dumps(prediction, default=str)
            
        except Exception as e:
            print(f"Error in predict_disease_spread: {e}")
            import traceback
            traceback.print_exc()
            return json.dumps({
                "error": str(e),
                "status": "prediction_failed"
            })
    
    def _generate_forecast(self, disease_name: str, region: str, horizon_weeks: int) -> dict:
        """Generates forecast data structure.
        
        TODO: Replace with actual PandemicLLM integration
        """
        # Placeholder forecast generation
        base_cases = 100
        growth_rate = 1.15
        
        weekly_forecasts = []
        for week in range(1, horizon_weeks + 1):
            projected_cases = int(base_cases * (growth_rate ** week))
            weekly_forecasts.append({
                "week": week,
                "start_date": (datetime.now() + timedelta(weeks=week-1)).strftime("%Y-%m-%d"),
                "end_date": (datetime.now() + timedelta(weeks=week)).strftime("%Y-%m-%d"),
                "projected_cases": projected_cases,
                "projected_hospitalizations": int(projected_cases * 0.15),
                "projected_icu_admissions": int(projected_cases * 0.03),
                "reproductive_number": round(1.2 + (week * 0.1), 2)
            })
        
        return {
            "weekly_projections": weekly_forecasts,
            "peak_week": horizon_weeks,
            "peak_cases": weekly_forecasts[-1]['projected_cases'] if weekly_forecasts else 0,
            "total_projected_cases": sum(w['projected_cases'] for w in weekly_forecasts),
            "growth_trend": "increasing" if growth_rate > 1 else "decreasing"
        }
    
    def _assess_outbreak_risk(self, disease_name: str, region: str) -> dict:
        """Assesses outbreak risk level.
        
        TODO: Integrate with anomaly detection and real data
        """
        return {
            "overall_risk": "medium",
            "risk_score": 6.5,
            "risk_factors": [
                {
                    "factor": "Population Density",
                    "score": 7,
                    "impact": "high"
                },
                {
                    "factor": "Healthcare Capacity",
                    "score": 6,
                    "impact": "medium"
                },
                {
                    "factor": "Seasonal Patterns",
                    "score": 7,
                    "impact": "high"
                }
            ],
            "transmission_rate": "moderate",
            "containment_measures": ["social_distancing", "mask_mandates", "contact_tracing"]
        }
    
    def _generate_recommendations(self, disease_name: str, region: str, horizon_weeks: int) -> dict:
        """Generates intervention recommendations.
        
        TODO: Make recommendations dynamic based on prediction data
        """
        return {
            "immediate_actions": [
                "Increase hospital bed capacity by 20%",
                "Deploy additional medical personnel to affected areas",
                "Enhance contact tracing operations"
            ],
            "resource_allocation": {
                "additional_icu_beds": 50,
                "ventilators_needed": 20,
                "ppe_units": 10000,
                "testing_kits": 50000
            },
            "public_health_measures": [
                "Issue public health advisory",
                "Recommend mask-wearing in public spaces",
                "Limit large gatherings (>50 people)"
            ],
            "monitoring_priorities": [
                "Track hospital admission rates daily",
                "Monitor ICU capacity utilization",
                "Analyze social media sentiment for compliance"
            ]
        }
    
    def get_recent_predictions(self, days: int = 7, disease: str = None,
                              region: str = None) -> str:
        """Retrieves recent predictions from the database.
        
        Args:
            days: Number of days to look back
            disease: Optional disease filter
            region: Optional region filter
            
        Returns:
            JSON string with recent predictions
        """
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            
            conn = psycopg2.connect(self.connection_string)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT 
                    id as prediction_id, disease_name, region, forecast_weeks,
                    predicted_cases, confidence, risk_level, model_used,
                    prediction_json, created_date
                FROM outbreak_predictions
                WHERE created_date >= NOW() - INTERVAL '%s days'
            """
            params = [days]
            
            if disease:
                query += " AND disease_name = %s"
                params.append(disease)
            
            if region:
                query += " AND region = %s"
                params.append(region)
            
            query += " ORDER BY created_date DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            predictions = []
            for row in rows:
                predictions.append(dict(row))
            
            cursor.close()
            conn.close()
            
            result = {
                "query_timestamp": datetime.now().isoformat(),
                "time_period_days": days,
                "filters": {
                    "disease": disease,
                    "region": region
                },
                "total_predictions": len(predictions),
                "predictions": predictions
            }
            
            return json.dumps(result, default=str)
            
        except Exception as e:
            print(f"Error in get_recent_predictions: {e}")
            return json.dumps({"error": str(e)})
    
    def calculate_reproductive_number(self, disease_name: str, region: str, 
                                     days: int = 14) -> str:
        """Calculates the epidemic reproductive number (R0).
        
        Args:
            disease_name: Name of the disease
            region: Region for calculation
            days: Number of days of data to use (default 14)
            
        Returns:
            JSON string with R0 calculation
        """
        try:
            from utils.database_utils import get_surveillance_data
            
            # Get recent case data
            surveillance_data = get_surveillance_data(
                self.connection_string,
                days=days,
                region=region
            )
            
            # Placeholder R0 calculation
            # TODO: Implement actual epidemiological R0 calculation
            
            result = {
                "calculation_timestamp": datetime.now().isoformat(),
                "disease": disease_name,
                "region": region,
                "time_period_days": days,
                "r0_estimate": 1.35,
                "confidence_interval": {
                    "lower": 1.15,
                    "upper": 1.55,
                    "confidence_level": 0.95
                },
                "interpretation": "moderate_transmission",
                "trend": "stable",
                "notes": "R0 > 1 indicates outbreak is growing. R0 < 1 indicates outbreak is declining."
            }
            
            return json.dumps(result, default=str)
            
        except Exception as e:
            print(f"Error in calculate_reproductive_number: {e}")
            return json.dumps({"error": str(e)})
