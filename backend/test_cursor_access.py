"""Test the surveillance status query logic"""
from utils.database_utils import DatabaseConnection

db = DatabaseConnection()
db.connect()
cursor = db.connection.cursor()

# Test the exact query from the endpoint
cursor.execute("""
    SELECT COUNT(*) as count FROM anomaly_detections 
    WHERE timestamp >= NOW() - INTERVAL '24 hours'
""")
result = cursor.fetchone()
print(f"Query result type: {type(result)}")
print(f"Query result: {result}")
print(f"Access by key 'count': {result['count']}")

try:
    print(f"Access by index [0]: {result[0]}")
except:
    print("Cannot access by index [0]")

cursor.close()
db.disconnect()
