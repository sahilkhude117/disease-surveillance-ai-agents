"""Test the anomaly query directly"""
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')

try:
    conn = psycopg2.connect(DB_CONNECTION_STRING, cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    
    # Test the query like the endpoint does
    query = """
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
        WHERE timestamp >= NOW() - INTERVAL '%s days'
        ORDER BY timestamp DESC, severity DESC
    """
    
    print("Executing query with days=7...")
    cursor.execute(query, (7,))
    results = cursor.fetchall()
    
    print(f"Found {len(results)} results")
    
    # Convert like the endpoint does
    results = [
        {k: v.isoformat() if hasattr(v, 'isoformat') else v for k, v in dict(row).items()}
        for row in results
    ]
    
    if results:
        print("\nFirst result:")
        for k, v in results[0].items():
            print(f"  {k}: {v}")
    
    cursor.close()
    conn.close()
    print("\n✅ Query executed successfully")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
