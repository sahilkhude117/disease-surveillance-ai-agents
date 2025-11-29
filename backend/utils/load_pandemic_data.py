"""
Load and transform PandemicLLM data to disease surveillance format
"""
import pickle
import json
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_pickle_safe(filepath):
    """Safely load pickle file handling version issues"""
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f, encoding='latin1')
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def transform_to_surveillance_data(pandemic_data_path):
    """
    Transform PandemicLLM data to our surveillance database format
    
    Returns SQL INSERT statements for:
    - hospital_surveillance_data
    - anomaly_detections
    - outbreak_predictions
    """
    
    base_path = pandemic_data_path
    
    # Load all available data files
    data_files = {
        'confirmed_cases': os.path.join(base_path, 'confimed_cases_daily_state.pkl'),
        'hospitalizations': os.path.join(base_path, 'hospitalization_daily_state.pkl'),
        'vaccinations': os.path.join(base_path, 'vaccination_weekly_state.pkl'),
        'variants': os.path.join(base_path, 'top_5_variant.pkl'),
        'final_data': os.path.join(base_path, 'final_data.pkl'),
    }
    
    print("Loading PandemicLLM data files...")
    loaded_data = {}
    
    for name, filepath in data_files.items():
        if os.path.exists(filepath):
            data = load_pickle_safe(filepath)
            if data is not None:
                loaded_data[name] = data
                print(f"✓ Loaded {name}: {type(data)}")
                
                # Print structure info
                if isinstance(data, dict):
                    print(f"  Keys: {list(data.keys())[:5]}...")
                elif hasattr(data, 'shape'):
                    print(f"  Shape: {data.shape}")
                elif hasattr(data, '__len__'):
                    print(f"  Length: {len(data)}")
        else:
            print(f"✗ File not found: {filepath}")
    
    return loaded_data

def generate_mock_surveillance_data():
    """
    Generate realistic mock data based on Indian regions
    This provides immediate data while we work on integrating PandemicLLM data
    """
    
    regions = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad']
    diseases = ['Influenza A', 'Dengue Fever', 'COVID-19', 'Malaria', 'Typhoid']
    
    # Generate data for last 30 days
    base_date = datetime.now()
    
    sql_statements = []
    
    # Hospital surveillance data
    print("\nGenerating hospital surveillance data...")
    for region in regions:
        for day_offset in range(30):
            date = base_date - timedelta(days=day_offset)
            
            # Simulate disease patterns
            for disease in diseases:
                # Base case count varies by disease and region
                if disease == 'Influenza A':
                    base_count = 20 + (day_offset % 10)  # Seasonal pattern
                elif disease == 'Dengue Fever' and region in ['Mumbai', 'Delhi']:
                    base_count = 15 + (day_offset % 8)
                elif disease == 'COVID-19':
                    base_count = 10 - (day_offset // 5)  # Declining trend
                else:
                    base_count = 5 + (day_offset % 5)
                
                # Add some randomness
                import random
                patient_count = max(1, base_count + random.randint(-5, 10))
                
                severity = random.choice(['mild', 'moderate', 'severe', 'critical'])
                age_group = random.choice(['0-18', '18-45', '45-65', '65+'])
                
                sql = f"""
INSERT INTO hospital_surveillance_data (timestamp, location, region, facility_name, symptom_type, patient_count, age_group, severity_level, diagnosis)
VALUES ('{date.strftime('%Y-%m-%d %H:%M:%S')}', '{region}', '{region}', '{region} General Hospital', 'fever', {patient_count}, '{age_group}', '{severity}', '{disease}')
ON CONFLICT DO NOTHING;
"""
                sql_statements.append(sql.strip())
    
    # Anomaly detections
    print("Generating anomaly detections...")
    for region in ['Mumbai', 'Delhi', 'Bangalore']:
        date = base_date - timedelta(hours=random.randint(1, 24))
        
        anomaly_types = ['spike', 'cluster', 'trend']
        severities = ['high', 'medium', 'low']
        
        anomaly_type = random.choice(anomaly_types)
        severity = random.choice(severities)
        confidence = 0.6 + random.random() * 0.35
        
        baseline = 15.0 + random.random() * 10
        current = baseline * (1.5 + random.random())
        deviation = ((current - baseline) / baseline) * 100
        
        sql = f"""
INSERT INTO anomaly_detections (timestamp, location, region, anomaly_type, severity, confidence, data_source, baseline_value, current_value, deviation_percent, detection_method, metrics)
VALUES ('{date.strftime('%Y-%m-%d %H:%M:%S')}', '{region}', '{region}', '{anomaly_type}', '{severity}', {confidence:.2f}, 'hospital', {baseline:.1f}, {current:.1f}, {deviation:.1f}, 'statistical', '{{"method": "z-score", "threshold": 2.5}}')
ON CONFLICT DO NOTHING;
"""
        sql_statements.append(sql.strip())
    
    # Outbreak predictions
    print("Generating outbreak predictions...")
    for region in regions[:5]:  # Top 5 regions
        for disease in ['Influenza A', 'Dengue Fever', 'COVID-19']:
            forecast_weeks = random.choice([1, 2, 3, 4])
            predicted_cases = random.randint(100, 1000)
            confidence = 0.5 + random.random() * 0.4
            risk_level = 'high' if confidence > 0.8 else ('medium' if confidence > 0.6 else 'low')
            
            prediction_json = {
                'model': 'SEIR',
                'parameters': {'R0': 1.5 + random.random(), 'incubation': 5.2},
                'forecast': [predicted_cases + random.randint(-50, 50) for _ in range(forecast_weeks)]
            }
            
            sql = f"""
INSERT INTO outbreak_predictions (disease_name, region, forecast_weeks, predicted_cases, confidence, risk_level, model_used, prediction_json)
VALUES ('{disease}', '{region}', {forecast_weeks}, {predicted_cases}, {confidence:.2f}, '{risk_level}', 'SEIR', '{json.dumps(prediction_json)}')
ON CONFLICT DO NOTHING;
"""
            sql_statements.append(sql.strip())
    
    return sql_statements

if __name__ == '__main__':
    import random
    random.seed(42)  # For reproducibility
    
    # Try to load PandemicLLM data
    pandemic_data_path = r'E:\Hackthons\MumbaiHacks\PandemicLLM\data\src\processed_data'
    
    if os.path.exists(pandemic_data_path):
        print("=" * 60)
        print("LOADING PANDEMICLLM DATA")
        print("=" * 60)
        loaded_data = transform_to_surveillance_data(pandemic_data_path)
        
        print("\n" + "=" * 60)
        print("Data loaded successfully!")
        print(f"Available datasets: {list(loaded_data.keys())}")
        print("=" * 60)
    
    # Generate mock data
    print("\n" + "=" * 60)
    print("GENERATING MOCK SURVEILLANCE DATA")
    print("=" * 60)
    
    sql_statements = generate_mock_surveillance_data()
    
    # Save to SQL file
    output_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'sql',
        'insert_mock_data.sql'
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- Generated Mock Surveillance Data\n")
        f.write("-- Generated on: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n")
        f.write("\n".join(sql_statements))
    
    print(f"\n✓ Generated {len(sql_statements)} SQL statements")
    print(f"✓ Saved to: {output_file}")
    print("\nRun this SQL file in your Supabase SQL Editor to populate the database!")
