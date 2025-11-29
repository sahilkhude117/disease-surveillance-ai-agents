"""Direct database test script"""
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')
print(f"Connection string: {DB_CONNECTION_STRING[:50]}...")

try:
    # Test connection
    conn = psycopg2.connect(DB_CONNECTION_STRING, cursor_factory=RealDictCursor)
    print("✅ Connected to database")
    
    cursor = conn.cursor()
    
    # Test anomalies table
    cursor.execute("SELECT COUNT(*) as count FROM anomaly_detections")
    result = cursor.fetchone()
    print(f"Anomalies count: {result['count']}")
    
    # Test predictions table
    cursor.execute("SELECT COUNT(*) as count FROM outbreak_predictions")
    result = cursor.fetchone()
    print(f"Predictions count: {result['count']}")
    
    # Test alerts table  
    cursor.execute("SELECT COUNT(*) as count FROM surveillance_alerts")
    result = cursor.fetchone()
    print(f"Alerts count: {result['count']}")
    
    # Test hospital data
    cursor.execute("SELECT COUNT(*) as count FROM hospital_surveillance_data")
    result = cursor.fetchone()
    print(f"Hospital records: {result['count']}")
    
    cursor.close()
    conn.close()
    print("✅ All tests passed")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
