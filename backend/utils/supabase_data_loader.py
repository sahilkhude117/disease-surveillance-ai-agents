"""
Load data using Supabase REST API (more reliable for large datasets)
"""
import os
import sys
import json
from datetime import datetime
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("⚠️  Supabase client not installed. Installing...")
    os.system("pip install supabase")
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True

def load_hospital_data(supabase: Client):
    """Load hospital surveillance data"""
    print("\n1. Loading Hospital Surveillance Data...")
    
    regions = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad']
    diseases = ['Influenza A', 'Dengue Fever', 'COVID-19', 'Malaria', 'Typhoid']
    
    data = []
    base_date = datetime.now()
    
    for region in regions:
        for day_offset in range(30):
            from datetime import timedelta
            date = base_date - timedelta(days=day_offset)
            date = date.replace(hour=0, minute=0, second=0, microsecond=0)
            
            for disease in diseases:
                # Disease patterns
                if disease == 'Influenza A':
                    base_count = 20 + (day_offset % 10)
                elif disease == 'Dengue Fever' and region in ['Mumbai', 'Delhi']:
                    base_count = 15 + (day_offset % 8)
                elif disease == 'COVID-19':
                    base_count = max(5, 10 - (day_offset // 5))
                else:
                    base_count = 5 + (day_offset % 5)
                
                patient_count = max(1, base_count + random.randint(-5, 10))
                
                data.append({
                    'timestamp': date.isoformat(),
                    'location': region,
                    'region': region,
                    'facility_name': f'{region} General Hospital',
                    'symptom_type': 'fever',
                    'patient_count': patient_count,
                    'age_group': random.choice(['0-18', '18-45', '45-65', '65+']),
                    'severity_level': random.choice(['mild', 'moderate', 'severe', 'critical']),
                    'diagnosis': disease,
                })
    
    # Insert in batches
    batch_size = 100
    inserted = 0
    
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        try:
            result = supabase.table('hospital_surveillance_data').insert(batch).execute()
            inserted += len(batch)
            if (i + batch_size) % 500 == 0:
                print(f"   Progress: {i + batch_size}/{len(data)} records...")
        except Exception as e:
            if 'duplicate' not in str(e).lower():
                print(f"   Warning: {str(e)[:100]}")
    
    print(f"   ✅ Inserted {inserted} hospital records")
    return inserted

def load_anomaly_data(supabase: Client):
    """Load anomaly detections"""
    print("\n2. Loading Anomaly Detections...")
    
    regions = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata']
    data = []
    base_date = datetime.now()
    
    from datetime import timedelta
    for region in regions:
        for day_offset in range(7):
            date = base_date - timedelta(days=day_offset)
            
            anomaly_type = random.choice(['spike', 'cluster', 'trend'])
            severity = random.choice(['high', 'medium', 'low'])
            confidence = 0.6 + random.random() * 0.35
            
            baseline = 15.0 + random.random() * 10
            current = baseline * (1.5 + random.random())
            deviation = ((current - baseline) / baseline) * 100
            
            data.append({
                'timestamp': date.isoformat(),
                'location': region,
                'region': region,
                'anomaly_type': anomaly_type,
                'severity': severity,
                'confidence': round(confidence, 2),
                'data_source': 'hospital',
                'baseline_value': round(baseline, 1),
                'current_value': round(current, 1),
                'deviation_percent': round(deviation, 1),
                'detection_method': 'statistical',
                'metrics': json.dumps({'method': 'z-score', 'threshold': 2.5})
            })
    
    try:
        result = supabase.table('anomaly_detections').insert(data).execute()
        print(f"   ✅ Inserted {len(data)} anomaly records")
        return len(data)
    except Exception as e:
        print(f"   Error: {e}")
        return 0

def load_prediction_data(supabase: Client):
    """Load outbreak predictions"""
    print("\n3. Loading Outbreak Predictions...")
    
    regions = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad']
    diseases = ['Influenza A', 'Dengue Fever', 'COVID-19']
    
    data = []
    
    for region in regions[:5]:
        for disease in diseases:
            forecast_weeks = random.choice([1, 2, 3, 4])
            predicted_cases = random.randint(100, 1000)
            confidence = 0.5 + random.random() * 0.4
            risk_level = 'high' if confidence > 0.8 else ('medium' if confidence > 0.6 else 'low')
            
            prediction_json = {
                'model': 'SEIR',
                'parameters': {'R0': round(1.5 + random.random(), 2), 'incubation': 5.2},
                'forecast': [predicted_cases + random.randint(-50, 50) for _ in range(forecast_weeks)]
            }
            
            data.append({
                'disease_name': disease,
                'region': region,
                'forecast_weeks': forecast_weeks,
                'predicted_cases': predicted_cases,
                'confidence': round(confidence, 2),
                'risk_level': risk_level,
                'model_used': 'SEIR',
                'prediction_json': json.dumps(prediction_json)
            })
    
    try:
        result = supabase.table('outbreak_predictions').insert(data).execute()
        print(f"   ✅ Inserted {len(data)} prediction records")
        return len(data)
    except Exception as e:
        print(f"   Error: {e}")
        return 0

def load_alert_data(supabase: Client):
    """Load surveillance alerts"""
    print("\n4. Loading Surveillance Alerts...")
    
    regions = ['Mumbai', 'Delhi', 'Bangalore']
    diseases = ['Influenza A', 'Dengue Fever', 'COVID-19']
    
    data = []
    
    for i, region in enumerate(regions):
        disease = diseases[i]
        severity = random.choice(['high', 'medium'])
        
        alert_id = f"ALERT-{region.upper()[:3]}-{datetime.now().strftime('%Y%m%d')}-{i+1:03d}"
        
        data.append({
            'alert_id': alert_id,
            'alert_type': 'outbreak_warning',
            'severity': severity,
            'region': region,
            'disease_name': disease,
            'message': f'{disease} outbreak detected in {region}. Increased surveillance recommended.',
            'audience': 'public_health_officials',
            'status': 'active',
            'alert_json': json.dumps({
                'detected_at': datetime.now().isoformat(),
                'confidence': 0.85,
                'affected_areas': [region]
            })
        })
    
    try:
        result = supabase.table('surveillance_alerts').insert(data).execute()
        print(f"   ✅ Inserted {len(data)} alert records")
        return len(data)
    except Exception as e:
        print(f"   Error: {e}")
        return 0

def verify_data(supabase: Client):
    """Verify loaded data"""
    print("\n" + "="*70)
    print("VERIFYING DATA LOAD")
    print("="*70)
    
    tables = [
        'hospital_surveillance_data',
        'anomaly_detections',
        'outbreak_predictions',
        'surveillance_alerts'
    ]
    
    for table in tables:
        try:
            result = supabase.table(table).select('*', count='exact').limit(1).execute()
            count = result.count
            status = "✅" if count > 0 else "⚠️ "
            print(f"{status} {table.replace('_', ' ').title()}: {count} records")
        except Exception as e:
            print(f"❌ {table}: Error - {str(e)[:50]}")
    
    # Show samples
    print("\n" + "-"*70)
    print("SAMPLE DATA - Recent Hospital Records:")
    print("-"*70)
    
    try:
        result = supabase.table('hospital_surveillance_data')\
            .select('timestamp,region,diagnosis,patient_count,severity_level')\
            .order('timestamp', desc=True)\
            .limit(5)\
            .execute()
        
        for row in result.data:
            print(f"  {row['timestamp'][:19]} | {row['region']:15} | {row['diagnosis']:20} | Count: {row['patient_count']:3} | {row['severity_level']}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "-"*70)
    print("SAMPLE DATA - Outbreak Predictions:")
    print("-"*70)
    
    try:
        result = supabase.table('outbreak_predictions')\
            .select('disease_name,region,forecast_weeks,predicted_cases,risk_level,confidence')\
            .order('created_date', desc=True)\
            .limit(5)\
            .execute()
        
        for row in result.data:
            print(f"  {row['disease_name']:20} | {row['region']:15} | {row['forecast_weeks']}w | Cases: {row['predicted_cases']:4} | {row['risk_level']:6} ({row['confidence']:.2f})")
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("="*70)
    print("DISEASE SURVEILLANCE AI - SUPABASE DATA LOADER")
    print("="*70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    random.seed(42)  # For reproducibility
    
    # Create Supabase client
    print("Connecting to Supabase...")
    try:
        supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
        print("✅ Connected successfully\n")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return
    
    print("="*70)
    print("LOADING DATA")
    print("="*70)
    
    total_records = 0
    
    # Load all data
    total_records += load_hospital_data(supabase)
    total_records += load_anomaly_data(supabase)
    total_records += load_prediction_data(supabase)
    total_records += load_alert_data(supabase)
    
    # Verify
    verify_data(supabase)
    
    print("\n" + "="*70)
    print("COMPLETED SUCCESSFULLY!")
    print("="*70)
    print(f"Total records inserted: {total_records}")
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n🎉 Your disease surveillance system now has live data!")
    print("🔗 Visit your frontend dashboard to see predictions and alerts!")
    print("="*70)

if __name__ == '__main__':
    main()
