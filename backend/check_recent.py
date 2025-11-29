"""Check recent data"""
from utils.database_utils import DatabaseConnection

db = DatabaseConnection()
db.connect()
cursor = db.connection.cursor()

cursor.execute("SELECT COUNT(*) as count FROM anomaly_detections WHERE timestamp >= NOW() - INTERVAL '24 hours'")
result = cursor.fetchone()
print(f"Anomalies in last 24h: {result['count']}")

cursor.execute("SELECT COUNT(*) as count FROM outbreak_predictions WHERE created_date >= NOW() - INTERVAL '24 hours'")
result = cursor.fetchone()
print(f"Predictions in last 24h: {result['count']}")

cursor.execute("SELECT COUNT(*) as count FROM surveillance_alerts WHERE status = 'active'")
result = cursor.fetchone()
print(f"Active alerts: {result['count']}")

cursor.close()
db.disconnect()
