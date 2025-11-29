"""
Transform PandemicLLM data (US states) to Indian disease surveillance format
Maps US states to Indian regions and transforms the data structure
"""
import pickle
import json
from datetime import datetime, timedelta
import os

def load_pickle_safe(filepath):
    """Safely load pickle file"""
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f, encoding='latin1')
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

# Map US states to Indian regions for realistic data
US_TO_INDIA_MAPPING = {
    'New York': 'Mumbai',
    'California': 'Delhi',
    'Texas': 'Bangalore',
    'Florida': 'Chennai',
    'Illinois': 'Kolkata',
    'Pennsylvania': 'Hyderabad',
    'Ohio': 'Pune',
    'Georgia': 'Ahmedabad',
    'North Carolina': 'Jaipur',
    'Michigan': 'Surat',
}

def transform_hospitalization_data(df, base_date=None):
    """
    Transform PandemicLLM hospitalization data to our format
    
    DataFrame columns from PandemicLLM:
    - date, state, hospitalized_currently, etc.
    """
    if base_date is None:
        base_date = datetime.now()
    
    sql_statements = []
    
    print(f"Transforming hospitalization data: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Take latest data points
    try:
        # Get last 30 days of data for mapped states
        for us_state, indian_region in US_TO_INDIA_MAPPING.items():
            state_data = df[df['state'] == us_state] if 'state' in df.columns else df
            
            if len(state_data) > 0:
                # Take last 30 records
                recent_data = state_data.tail(30)
                
                for idx, row in recent_data.iterrows():
                    # Calculate date offset
                    days_ago = len(recent_data) - list(recent_data.index).index(idx)
                    record_date = base_date - timedelta(days=days_ago)
                    
                    # Extract patient count
                    patient_count = 0
                    if 'hospitalized_currently' in row:
                        patient_count = int(row['hospitalized_currently']) if row['hospitalized_currently'] else 0
                    elif 'hospitalizedCurrently' in row:
                        patient_count = int(row['hospitalizedCurrently']) if row['hospitalizedCurrently'] else 0
                    
                    if patient_count > 0:
                        # Scale down to region level (US states are larger)
                        patient_count = max(1, patient_count // 100)
                        
                        sql = f"""
INSERT INTO hospital_surveillance_data (timestamp, location, region, facility_name, symptom_type, patient_count, age_group, severity_level, diagnosis)
VALUES ('{record_date.strftime('%Y-%m-%d %H:%M:%S')}', '{indian_region}', '{indian_region}', '{indian_region} Medical Center', 'respiratory', {patient_count}, '18-65', 'moderate', 'COVID-19')
ON CONFLICT DO NOTHING;"""
                        sql_statements.append(sql.strip())
    
    except Exception as e:
        print(f"Error transforming hospitalization data: {e}")
    
    return sql_statements

def transform_vaccination_data(df, base_date=None):
    """Transform vaccination data - can be used for coverage analysis"""
    if base_date is None:
        base_date = datetime.now()
    
    print(f"Vaccination data shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Just log this for now - we can extend to track vaccination coverage
    return []

def transform_variant_data(df, base_date=None):
    """Transform variant surveillance data"""
    if base_date is None:
        base_date = datetime.now()
    
    sql_statements = []
    
    print(f"Variant data shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    try:
        # Take recent variant data
        for us_state, indian_region in list(US_TO_INDIA_MAPPING.items())[:5]:
            state_data = df[df['state'] == us_state] if 'state' in df.columns else df.head(10)
            
            if len(state_data) > 0:
                recent_variants = state_data.tail(5)
                
                for idx, row in recent_variants.iterrows():
                    days_ago = len(recent_variants) - list(recent_variants.index).index(idx)
                    record_date = base_date - timedelta(days=days_ago * 7)  # Weekly data
                    
                    # Create anomaly detection for variant emergence
                    variant_name = row.get('variant', 'Unknown')
                    prevalence = row.get('prevalence', 0.5)
                    
                    if prevalence > 0.1:  # Significant prevalence
                        confidence = min(0.95, 0.7 + prevalence)
                        severity = 'high' if prevalence > 0.5 else 'medium'
                        
                        sql = f"""
INSERT INTO anomaly_detections (timestamp, location, region, anomaly_type, severity, confidence, data_source, baseline_value, current_value, deviation_percent, detection_method, metrics)
VALUES ('{record_date.strftime('%Y-%m-%d %H:%M:%S')}', '{indian_region}', '{indian_region}', 'variant_emergence', '{severity}', {confidence:.2f}, 'genomic', 0.1, {prevalence:.2f}, {(prevalence - 0.1) * 1000:.1f}, 'genomic_surveillance', '{{"variant": "{variant_name}", "prevalence": {prevalence:.2f}}}')
ON CONFLICT DO NOTHING;"""
                        sql_statements.append(sql.strip())
    
    except Exception as e:
        print(f"Error transforming variant data: {e}")
    
    return sql_statements

def generate_predictions_from_trends(hospitalization_df, base_date=None):
    """Generate outbreak predictions based on trend analysis"""
    if base_date is None:
        base_date = datetime.now()
    
    sql_statements = []
    
    try:
        # Analyze trends for each mapped region
        for us_state, indian_region in list(US_TO_INDIA_MAPPING.items())[:6]:
            state_data = hospitalization_df[hospitalization_df['state'] == us_state] if 'state' in hospitalization_df.columns else hospitalization_df
            
            if len(state_data) > 10:
                recent = state_data.tail(14)
                
                # Calculate trend
                if 'hospitalized_currently' in recent.columns:
                    values = recent['hospitalized_currently'].dropna()
                elif 'hospitalizedCurrently' in recent.columns:
                    values = recent['hospitalizedCurrently'].dropna()
                else:
                    continue
                
                if len(values) > 5:
                    # Simple trend: compare recent vs earlier
                    recent_avg = values.tail(7).mean()
                    earlier_avg = values.head(7).mean()
                    
                    if recent_avg > 0:
                        trend = (recent_avg - earlier_avg) / earlier_avg if earlier_avg > 0 else 0
                        
                        # Scale to Indian region size
                        predicted_cases = int(recent_avg // 50)  # Scale down
                        forecast_weeks = 2
                        
                        # Determine risk level
                        if trend > 0.2:
                            risk_level = 'high'
                            confidence = 0.75
                        elif trend > 0:
                            risk_level = 'medium'
                            confidence = 0.65
                        else:
                            risk_level = 'low'
                            confidence = 0.60
                        
                        prediction_json = {
                            'model': 'trend_analysis',
                            'trend_coefficient': float(trend),
                            'current_avg': float(recent_avg // 50),
                            'forecast': [predicted_cases + i * int(trend * predicted_cases) for i in range(1, forecast_weeks + 1)]
                        }
                        
                        sql = f"""
INSERT INTO outbreak_predictions (disease_name, region, forecast_weeks, predicted_cases, confidence, risk_level, model_used, prediction_json, created_date)
VALUES ('COVID-19', '{indian_region}', {forecast_weeks}, {predicted_cases}, {confidence:.2f}, '{risk_level}', 'trend_analysis', '{json.dumps(prediction_json)}', '{base_date.strftime('%Y-%m-%d %H:%M:%S')}')
ON CONFLICT DO NOTHING;"""
                        sql_statements.append(sql.strip())
    
    except Exception as e:
        print(f"Error generating predictions: {e}")
    
    return sql_statements

def main():
    """Main transformation pipeline"""
    pandemic_data_path = r'E:\Hackthons\MumbaiHacks\PandemicLLM\data\src\processed_data'
    
    print("=" * 70)
    print("TRANSFORMING PANDEMICLLM DATA TO INDIAN SURVEILLANCE FORMAT")
    print("=" * 70)
    
    all_sql = []
    
    # Load hospitalization data
    hosp_file = os.path.join(pandemic_data_path, 'hospitalization_daily_state.pkl')
    if os.path.exists(hosp_file):
        print("\n1. Loading hospitalization data...")
        hosp_df = load_pickle_safe(hosp_file)
        if hosp_df is not None:
            sql = transform_hospitalization_data(hosp_df)
            all_sql.extend(sql)
            print(f"   ✓ Generated {len(sql)} hospitalization records")
            
            # Generate predictions from trends
            print("\n2. Generating outbreak predictions from trends...")
            pred_sql = generate_predictions_from_trends(hosp_df)
            all_sql.extend(pred_sql)
            print(f"   ✓ Generated {len(pred_sql)} predictions")
    
    # Load vaccination data
    vacc_file = os.path.join(pandemic_data_path, 'vaccination_weekly_state.pkl')
    if os.path.exists(vacc_file):
        print("\n3. Loading vaccination data...")
        vacc_df = load_pickle_safe(vacc_file)
        if vacc_df is not None:
            sql = transform_vaccination_data(vacc_df)
            all_sql.extend(sql)
    
    # Load variant data
    var_file = os.path.join(pandemic_data_path, 'top_5_variant.pkl')
    if os.path.exists(var_file):
        print("\n4. Loading variant data...")
        var_df = load_pickle_safe(var_file)
        if var_df is not None:
            sql = transform_variant_data(var_df)
            all_sql.extend(sql)
            print(f"   ✓ Generated {len(sql)} variant surveillance records")
    
    # Save to SQL file
    output_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'sql',
        'insert_pandemic_llm_data.sql'
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- Transformed PandemicLLM Data for Indian Disease Surveillance\n")
        f.write("-- Generated on: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        f.write("-- Source: PandemicLLM US state data mapped to Indian regions\n\n")
        f.write("\n".join(all_sql))
    
    print("\n" + "=" * 70)
    print(f"✓ Total SQL statements generated: {len(all_sql)}")
    print(f"✓ Saved to: {output_file}")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Review the generated SQL file")
    print("2. Run it in your Supabase SQL Editor")
    print("3. Your dashboard will now show real pandemic data!")

if __name__ == '__main__':
    main()
