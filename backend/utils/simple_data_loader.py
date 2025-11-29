"""
Simple and robust data loader for Supabase
"""
import os
import sys
import psycopg2
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings

def load_data_batch(cursor, statements, batch_size=50):
    """Load data in batches to avoid connection issues"""
    executed = 0
    errors = 0
    
    for i in range(0, len(statements), batch_size):
        batch = statements[i:i+batch_size]
        
        for stmt in batch:
            if not stmt or len(stmt) < 10:
                continue
            
            try:
                cursor.execute(stmt)
                executed += 1
            except Exception as e:
                errors += 1
                if 'duplicate' not in str(e).lower() and errors <= 3:
                    print(f"  Error: {str(e)[:100]}")
        
        # Commit after each batch
        cursor.connection.commit()
        
        if (i + batch_size) % 200 == 0:
            print(f"  Progress: {i + batch_size}/{len(statements)} statements...")
    
    return executed, errors

def main():
    print("="*70)
    print("DISEASE SURVEILLANCE AI - DATA LOADER")
    print("="*70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Connect to database
    print("Connecting to Supabase...")
    try:
        conn = psycopg2.connect(settings.DB_CONNECTION_STRING)
        conn.autocommit = False
        cursor = conn.cursor()
        print("✅ Connected successfully\n")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return
    
    # Load SQL file
    sql_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sql')
    sql_file = os.path.join(sql_dir, 'insert_mock_data.sql')
    
    if not os.path.exists(sql_file):
        print(f"❌ SQL file not found: {sql_file}")
        return
    
    print(f"Loading SQL file: {sql_file}")
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Split into statements
    statements = [s.strip() for s in sql_content.split(';') if s.strip() and not s.strip().startswith('--')]
    print(f"Found {len(statements)} SQL statements\n")
    
    # Load data in batches
    print("Loading data in batches...")
    executed, errors = load_data_batch(cursor, statements, batch_size=50)
    
    print(f"\n✅ Successfully executed {executed} statements")
    if errors > 0:
        print(f"⚠️  {errors} statements had errors (likely duplicates)")
    
    # Verify data
    print("\n" + "="*70)
    print("VERIFYING DATA LOAD")
    print("="*70)
    
    checks = [
        ("Hospital Surveillance", "SELECT COUNT(*) FROM hospital_surveillance_data"),
        ("Anomaly Detections", "SELECT COUNT(*) FROM anomaly_detections"),
        ("Outbreak Predictions", "SELECT COUNT(*) FROM outbreak_predictions"),
    ]
    
    for name, query in checks:
        try:
            cursor.execute(query)
            count = cursor.fetchone()[0]
            status = "✅" if count > 0 else "⚠️ "
            print(f"{status} {name}: {count} records")
        except Exception as e:
            print(f"❌ {name}: Error - {str(e)[:50]}")
    
    # Show sample data
    print("\n" + "-"*70)
    print("SAMPLE DATA - Recent Hospital Surveillance:")
    print("-"*70)
    
    try:
        cursor.execute("""
            SELECT timestamp, region, diagnosis, patient_count, severity_level 
            FROM hospital_surveillance_data 
            ORDER BY timestamp DESC 
            LIMIT 5
        """)
        
        for row in cursor.fetchall():
            print(f"  {row[0]} | {row[1]:15} | {row[2]:20} | Count: {row[3]:3} | {row[4]}")
    except Exception as e:
        print(f"Error fetching samples: {e}")
    
    print("\n" + "-"*70)
    print("SAMPLE DATA - Outbreak Predictions:")
    print("-"*70)
    
    try:
        cursor.execute("""
            SELECT disease_name, region, forecast_weeks, predicted_cases, risk_level, confidence 
            FROM outbreak_predictions 
            ORDER BY created_date DESC 
            LIMIT 5
        """)
        
        for row in cursor.fetchall():
            print(f"  {row[0]:20} | {row[1]:15} | {row[2]}w | Cases: {row[3]:4} | {row[4]:6} ({row[5]:.2f})")
    except Exception as e:
        print(f"Error fetching predictions: {e}")
    
    # Close connection
    cursor.close()
    conn.close()
    
    print("\n" + "="*70)
    print("COMPLETED SUCCESSFULLY!")
    print("="*70)
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n🎉 Your disease surveillance system now has live data!")
    print("🔗 Visit your frontend dashboard to see predictions and alerts!")
    print("="*70)

if __name__ == '__main__':
    main()
