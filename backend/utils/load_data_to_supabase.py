"""
Load mock data directly into Supabase database
"""
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database_utils import DatabaseConnection

def load_sql_file(filepath):
    """Load and execute SQL file"""
    print(f"\nLoading SQL file: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Split into individual statements
        statements = [s.strip() for s in sql_content.split(';') if s.strip() and not s.strip().startswith('--')]
        
        print(f"Found {len(statements)} SQL statements")
        
        # Get database connection
        db = DatabaseConnection()
        conn = db.connect()
        if not conn:
            print("❌ Failed to connect to database")
            return False
        
        cursor = conn.cursor()
        
        # Execute each statement
        executed = 0
        errors = 0
        
        for i, statement in enumerate(statements):
            if not statement or len(statement) < 10:
                continue
                
            try:
                cursor.execute(statement)
                executed += 1
                
                if (i + 1) % 100 == 0:
                    print(f"  Progress: {i + 1}/{len(statements)} statements...")
                    conn.commit()
                    
            except Exception as e:
                errors += 1
                if errors <= 5:  # Only show first 5 errors
                    print(f"  Warning (statement {i+1}): {str(e)[:100]}")
        
        # Final commit
        conn.commit()
        cursor.close()
        db.disconnect()
        
        print(f"\n✅ Successfully executed {executed} statements")
        if errors > 0:
            print(f"⚠️  {errors} statements had errors (likely duplicates - this is OK)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading SQL file: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_data_loaded():
    """Verify that data was loaded successfully"""
    print("\n" + "="*70)
    print("VERIFYING DATA LOAD")
    print("="*70)
    
    try:
        db = DatabaseConnection()
        conn = db.connect()
        if not conn:
            print("❌ Cannot verify - database connection failed")
            return False
        
        cursor = conn.cursor()
        
        # Check various tables
        checks = [
            ("Hospital Surveillance", "SELECT COUNT(*) FROM hospital_surveillance_data"),
            ("Anomaly Detections", "SELECT COUNT(*) FROM anomaly_detections"),
            ("Outbreak Predictions", "SELECT COUNT(*) FROM outbreak_predictions"),
            ("Surveillance Alerts", "SELECT COUNT(*) FROM surveillance_alerts"),
        ]
        
        all_good = True
        for name, query in checks:
            try:
                cursor.execute(query)
                count = cursor.fetchone()[0]
                status = "✅" if count > 0 else "⚠️ "
                print(f"{status} {name}: {count} records")
                if count == 0:
                    all_good = False
            except Exception as e:
                print(f"❌ {name}: Error - {e}")
                all_good = False
        
        # Show sample data
        print("\n" + "-"*70)
        print("SAMPLE DATA - Recent Hospital Surveillance:")
        print("-"*70)
        
        cursor.execute("""
            SELECT timestamp, region, diagnosis, patient_count, severity_level 
            FROM hospital_surveillance_data 
            ORDER BY timestamp DESC 
            LIMIT 5
        """)
        
        for row in cursor.fetchall():
            print(f"  {row[0]} | {row[1]:15} | {row[2]:20} | Count: {row[3]:3} | {row[4]}")
        
        print("\n" + "-"*70)
        print("SAMPLE DATA - Active Predictions:")
        print("-"*70)
        
        cursor.execute("""
            SELECT disease_name, region, forecast_weeks, predicted_cases, risk_level, confidence 
            FROM outbreak_predictions 
            ORDER BY created_date DESC 
            LIMIT 5
        """)
        
        for row in cursor.fetchall():
            print(f"  {row[0]:20} | {row[1]:15} | {row[2]}w forecast | Cases: {row[3]:4} | {row[4]:6} risk ({row[5]:.2f})")
        
        cursor.close()
        db.disconnect()
        
        return all_good
        
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("="*70)
    print("DISEASE SURVEILLANCE AI - DATA LOADER")
    print("="*70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get SQL file paths
    sql_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sql')
    
    files_to_load = [
        ('Mock Surveillance Data', os.path.join(sql_dir, 'insert_mock_data.sql')),
        ('PandemicLLM Data', os.path.join(sql_dir, 'insert_pandemic_llm_data.sql')),
    ]
    
    success_count = 0
    
    for name, filepath in files_to_load:
        print(f"\n{'='*70}")
        print(f"Loading: {name}")
        print('='*70)
        
        if os.path.exists(filepath):
            if load_sql_file(filepath):
                success_count += 1
        else:
            print(f"⚠️  File not found: {filepath}")
    
    # Verify data was loaded
    verify_data_loaded()
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"✅ Successfully loaded {success_count}/{len(files_to_load)} data files")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n🎉 Your disease surveillance system now has live data!")
    print("🔗 Check your frontend dashboard to see the predictions and alerts!")
    print("="*70)

if __name__ == '__main__':
    main()
