"""Data collection plugin for gathering health surveillance data from multiple sources."""

import json
from datetime import datetime, timedelta
from utils.database_utils import get_surveillance_data
from utils.data_processing import (
    aggregate_hospital_data,
    analyze_social_media_sentiment,
    process_environmental_data,
    analyze_pharmacy_trends
)


class DataCollectionPlugin:
    """Plugin for collecting and aggregating disease surveillance data."""
    
    def __init__(self, connection_string):
        self.connection_string = connection_string
    
    def get_health_data_sources(self, days: int = 7, region: str = None) -> str:
        """Retrieves and aggregates surveillance data from all sources.
        
        Args:
            days: Number of days of historical data to retrieve (default 7)
            region: Optional region filter (e.g., 'Maharashtra', 'Delhi')
            
        Returns:
            JSON string with aggregated data from all surveillance sources
        """
        try:
            print(f"Collecting surveillance data for last {days} days")
            
            # Get raw data from all sources
            surveillance_data = get_surveillance_data(
                self.connection_string,
                days=days,
                region=region
            )
            
            # Aggregate and process data from each source
            result = {
                "collection_timestamp": datetime.now().isoformat(),
                "time_period_days": days,
                "region": region or "all_regions",
                "data_sources": {}
            }
            
            # Hospital data
            if 'hospital' in surveillance_data and not surveillance_data['hospital'].empty:
                result['data_sources']['hospital'] = aggregate_hospital_data(
                    surveillance_data['hospital']
                )
                print(f"Hospital data: {len(surveillance_data['hospital'])} records")
            else:
                result['data_sources']['hospital'] = {"status": "no_data_available"}
            
            # Social media data
            if 'social_media' in surveillance_data and not surveillance_data['social_media'].empty:
                result['data_sources']['social_media'] = analyze_social_media_sentiment(
                    surveillance_data['social_media']
                )
                print(f"Social media data: {len(surveillance_data['social_media'])} records")
            else:
                result['data_sources']['social_media'] = {"status": "no_data_available"}
            
            # Environmental data
            if 'environmental' in surveillance_data and not surveillance_data['environmental'].empty:
                result['data_sources']['environmental'] = process_environmental_data(
                    surveillance_data['environmental']
                )
                print(f"Environmental data: {len(surveillance_data['environmental'])} records")
            else:
                result['data_sources']['environmental'] = {"status": "no_data_available"}
            
            # Pharmacy data
            if 'pharmacy' in surveillance_data and not surveillance_data['pharmacy'].empty:
                result['data_sources']['pharmacy'] = analyze_pharmacy_trends(
                    surveillance_data['pharmacy']
                )
                print(f"Pharmacy data: {len(surveillance_data['pharmacy'])} records")
            else:
                result['data_sources']['pharmacy'] = {"status": "no_data_available"}
            
            # Add data quality metrics
            result['data_quality'] = {
                "sources_available": sum(1 for v in result['data_sources'].values() 
                                       if v.get('status') != 'no_data_available'),
                "total_sources": 4,
                "completeness_percentage": round(
                    sum(1 for v in result['data_sources'].values() 
                        if v.get('status') != 'no_data_available') / 4 * 100, 2
                )
            }
            
            return json.dumps(result, default=str)
            
        except Exception as e:
            print(f"Error in get_health_data_sources: {e}")
            import traceback
            traceback.print_exc()
            return json.dumps({
                "error": str(e),
                "status": "data_collection_failed"
            })
    
    def get_hospital_data(self, days: int = 7, region: str = None) -> str:
        """Retrieves hospital surveillance data only.
        
        Args:
            days: Number of days of historical data
            region: Optional region filter
            
        Returns:
            JSON string with hospital data
        """
        try:
            surveillance_data = get_surveillance_data(
                self.connection_string,
                days=days,
                region=region
            )
            
            if 'hospital' not in surveillance_data or surveillance_data['hospital'].empty:
                return json.dumps({"status": "no_data_available"})
            
            result = aggregate_hospital_data(surveillance_data['hospital'])
            result['data_source'] = 'hospital'
            result['time_period_days'] = days
            
            return json.dumps(result, default=str)
            
        except Exception as e:
            print(f"Error in get_hospital_data: {e}")
            return json.dumps({"error": str(e)})
    
    def get_social_media_data(self, days: int = 7, region: str = None) -> str:
        """Retrieves social media surveillance data only.
        
        Args:
            days: Number of days of historical data
            region: Optional region filter
            
        Returns:
            JSON string with social media data
        """
        try:
            surveillance_data = get_surveillance_data(
                self.connection_string,
                days=days,
                region=region
            )
            
            if 'social_media' not in surveillance_data or surveillance_data['social_media'].empty:
                return json.dumps({"status": "no_data_available"})
            
            result = analyze_social_media_sentiment(surveillance_data['social_media'])
            result['data_source'] = 'social_media'
            result['time_period_days'] = days
            
            return json.dumps(result, default=str)
            
        except Exception as e:
            print(f"Error in get_social_media_data: {e}")
            return json.dumps({"error": str(e)})
    
    def get_environmental_data(self, days: int = 7, region: str = None) -> str:
        """Retrieves environmental surveillance data only.
        
        Args:
            days: Number of days of historical data
            region: Optional region filter
            
        Returns:
            JSON string with environmental data
        """
        try:
            surveillance_data = get_surveillance_data(
                self.connection_string,
                days=days,
                region=region
            )
            
            if 'environmental' not in surveillance_data or surveillance_data['environmental'].empty:
                return json.dumps({"status": "no_data_available"})
            
            result = process_environmental_data(surveillance_data['environmental'])
            result['data_source'] = 'environmental'
            result['time_period_days'] = days
            
            return json.dumps(result, default=str)
            
        except Exception as e:
            print(f"Error in get_environmental_data: {e}")
            return json.dumps({"error": str(e)})
    
    def get_pharmacy_data(self, days: int = 7, region: str = None) -> str:
        """Retrieves pharmacy surveillance data only.
        
        Args:
            days: Number of days of historical data
            region: Optional region filter
            
        Returns:
            JSON string with pharmacy data
        """
        try:
            surveillance_data = get_surveillance_data(
                self.connection_string,
                days=days,
                region=region
            )
            
            if 'pharmacy' not in surveillance_data or surveillance_data['pharmacy'].empty:
                return json.dumps({"status": "no_data_available"})
            
            result = analyze_pharmacy_trends(surveillance_data['pharmacy'])
            result['data_source'] = 'pharmacy'
            result['time_period_days'] = days
            
            return json.dumps(result, default=str)
            
        except Exception as e:
            print(f"Error in get_pharmacy_data: {e}")
            return json.dumps({"error": str(e)})
    
    def check_data_sources(self) -> str:
        """Checks the status and availability of all data sources.
        
        Returns:
            JSON string with data source status information
        """
        try:
            # Try to get 1 day of data from each source
            surveillance_data = get_surveillance_data(
                self.connection_string,
                days=1
            )
            
            status = {
                "check_timestamp": datetime.now().isoformat(),
                "sources": {
                    "hospital": {
                        "available": 'hospital' in surveillance_data and not surveillance_data['hospital'].empty,
                        "record_count": len(surveillance_data.get('hospital', [])) if 'hospital' in surveillance_data else 0
                    },
                    "social_media": {
                        "available": 'social_media' in surveillance_data and not surveillance_data['social_media'].empty,
                        "record_count": len(surveillance_data.get('social_media', [])) if 'social_media' in surveillance_data else 0
                    },
                    "environmental": {
                        "available": 'environmental' in surveillance_data and not surveillance_data['environmental'].empty,
                        "record_count": len(surveillance_data.get('environmental', [])) if 'environmental' in surveillance_data else 0
                    },
                    "pharmacy": {
                        "available": 'pharmacy' in surveillance_data and not surveillance_data['pharmacy'].empty,
                        "record_count": len(surveillance_data.get('pharmacy', [])) if 'pharmacy' in surveillance_data else 0
                    }
                }
            }
            
            # Calculate overall health
            available_count = sum(1 for v in status['sources'].values() if v['available'])
            status['overall_health'] = {
                "sources_online": available_count,
                "sources_total": 4,
                "health_percentage": round(available_count / 4 * 100, 2),
                "status": "healthy" if available_count >= 3 else "degraded" if available_count >= 2 else "critical"
            }
            
            return json.dumps(status, default=str)
            
        except Exception as e:
            print(f"Error in check_data_source_status: {e}")
            return json.dumps({
                "error": str(e),
                "overall_health": {"status": "error"}
            })
