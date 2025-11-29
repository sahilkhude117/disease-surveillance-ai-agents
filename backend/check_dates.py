"""Check data timestamps"""
from utils.database_utils import DatabaseConnection

db = DatabaseConnection()
db.connect()
cursor = db.connection.cursor()

cursor.execute("SELECT MAX(timestamp) as latest, MIN(timestamp) as earliest, COUNT(*) as total FROM anomaly_detections")
result = cursor.fetchone()
print(f"Anomalies - Total: {result['total']}, Earliest: {result['earliest']}, Latest: {result['latest']}")

cursor.execute("SELECT MAX(created_date) as latest, MIN(created_date) as earliest, COUNT(*) as total FROM outbreak_predictions")
result = cursor.fetchone()
print(f"Predictions - Total: {result['total']}, Earliest: {result['earliest']}, Latest: {result['latest']}")

cursor.execute("SELECT MAX(created_date) as latest, MIN(created_date) as earliest, COUNT(*) as total FROM surveillance_alerts")
result = cursor.fetchone()
print(f"Alerts - Total: {result['total']}, Earliest: {result['earliest']}, Latest: {result['latest']}")

cursor.close()
db.disconnect()
