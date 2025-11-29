-- Disease Surveillance AI Agent System - Sample Data (PostgreSQL)
-- Inserts realistic test data for development and testing

-- =============================================
-- Sample Hospital Surveillance Data
-- =============================================
DO $$
BEGIN
    RAISE NOTICE 'Inserting sample data...';
    RAISE NOTICE '';
    RAISE NOTICE 'Inserting hospital surveillance data...';
END $$;

INSERT INTO hospital_surveillance_data (timestamp, location, region, facility_name, symptom_type, patient_count, age_group, severity_level, diagnosis)
VALUES
    -- Mumbai region - Recent flu-like outbreak
    (NOW() - INTERVAL '2 hours', 'Mumbai', 'Mumbai', 'Lilavati Hospital', 'fever', 45, '18-45', 'moderate', 'Influenza A'),
    (NOW() - INTERVAL '2 hours', 'Mumbai', 'Mumbai', 'Lilavati Hospital', 'cough', 38, '18-45', 'mild', 'Upper Respiratory Infection'),
    (NOW() - INTERVAL '3 hours', 'Mumbai', 'Mumbai', 'JJ Hospital', 'fever', 52, '45-65', 'moderate', 'Influenza A'),
    (NOW() - INTERVAL '4 hours', 'Mumbai', 'Mumbai', 'KEM Hospital', 'respiratory_distress', 12, '65+', 'severe', 'Pneumonia'),
    (NOW() - INTERVAL '1 day', 'Mumbai', 'Mumbai', 'Breach Candy Hospital', 'fever', 28, '0-18', 'mild', 'Viral Fever'),
    (NOW() - INTERVAL '1 day', 'Mumbai', 'Mumbai', 'Hinduja Hospital', 'cough', 33, '18-45', 'mild', 'Bronchitis'),
    
    -- Delhi region - Dengue cases
    (NOW() - INTERVAL '1 hour', 'Delhi', 'Delhi', 'AIIMS Delhi', 'fever', 23, '18-45', 'high', 'Dengue Fever'),
    (NOW() - INTERVAL '2 hours', 'Delhi', 'Delhi', 'Max Hospital', 'fever', 18, '18-45', 'high', 'Dengue Fever'),
    (NOW() - INTERVAL '3 hours', 'Delhi', 'Delhi', 'Safdarjung Hospital', 'rash', 15, '0-18', 'moderate', 'Dengue Fever'),
    (NOW() - INTERVAL '1 day', 'Delhi', 'Delhi', 'Apollo Hospital', 'fever', 27, '45-65', 'high', 'Dengue Fever'),
    
    -- Bangalore region - Normal surveillance
    (NOW() - INTERVAL '1 hour', 'Bangalore', 'Bangalore', 'Manipal Hospital', 'fever', 8, '18-45', 'mild', 'Common Cold'),
    (NOW() - INTERVAL '2 hours', 'Bangalore', 'Bangalore', 'Apollo Hospitals', 'cough', 12, '45-65', 'mild', 'Seasonal Allergy'),
    (NOW() - INTERVAL '1 day', 'Bangalore', 'Bangalore', 'Fortis Hospital', 'fever', 6, '0-18', 'mild', 'Viral Infection'),
    
    -- Historical data (1 week ago)
    (NOW() - INTERVAL '7 days', 'Mumbai', 'Mumbai', 'Lilavati Hospital', 'fever', 15, '18-45', 'mild', 'Viral Fever'),
    (NOW() - INTERVAL '7 days', 'Delhi', 'Delhi', 'AIIMS Delhi', 'fever', 10, '18-45', 'moderate', 'Unknown'),
    (NOW() - INTERVAL '7 days', 'Bangalore', 'Bangalore', 'Manipal Hospital', 'cough', 7, '45-65', 'mild', 'Bronchitis')
ON CONFLICT DO NOTHING;

DO $$
DECLARE
    row_count INTEGER;
BEGIN
    GET DIAGNOSTICS row_count = ROW_COUNT;
    RAISE NOTICE '✓ Inserted % hospital records', row_count;
END $$;

-- =============================================
-- Sample Social Media Surveillance Data
-- =============================================
DO $$
BEGIN
    RAISE NOTICE 'Inserting social media surveillance data...';
END $$;

INSERT INTO social_media_surveillance_data (timestamp, location, region, platform, mention_count, symptom_keywords, sentiment_score, post_content)
VALUES
    (NOW() - INTERVAL '1 hour', 'Mumbai', 'Mumbai', 'Twitter', 247, 'fever,flu,sick', -0.65, 'Many people in Andheri area reporting fever and flu symptoms #MumbaiHealth'),
    (NOW() - INTERVAL '2 hours', 'Mumbai', 'Mumbai', 'Facebook', 189, 'cough,cold,sick', -0.52, 'Local clinics seeing surge in respiratory cases'),
    (NOW() - INTERVAL '3 hours', 'Mumbai', 'Mumbai', 'Instagram', 145, 'fever,headache', -0.48, 'Feeling unwell, lots of people around me are sick too'),
    (NOW() - INTERVAL '1 day', 'Mumbai', 'Mumbai', 'Twitter', 312, 'flu,hospital,emergency', -0.78, 'Hospitals in Mumbai reporting increased ER visits for flu-like symptoms'),
    
    (NOW() - INTERVAL '1 hour', 'Delhi', 'Delhi', 'Twitter', 198, 'dengue,fever,mosquito', -0.72, 'Dengue cases rising in South Delhi, be careful! #DengueAlert'),
    (NOW() - INTERVAL '2 hours', 'Delhi', 'Delhi', 'Facebook', 156, 'fever,dengue,rash', -0.68, 'My neighbor just tested positive for dengue, everyone stay safe'),
    (NOW() - INTERVAL '1 day', 'Delhi', 'Delhi', 'Twitter', 234, 'dengue,outbreak,warning', -0.85, 'Dengue outbreak confirmed in multiple Delhi localities'),
    
    (NOW() - INTERVAL '1 hour', 'Bangalore', 'Bangalore', 'Twitter', 45, 'allergy,pollen,sneeze', -0.25, 'Pollen levels high in Bangalore this week'),
    (NOW() - INTERVAL '1 day', 'Bangalore', 'Bangalore', 'Facebook', 38, 'cold,cough', -0.30, 'Weather changing, lots of people catching cold'),
    
    (NOW() - INTERVAL '7 days', 'Mumbai', 'Mumbai', 'Twitter', 87, 'fever,sick', -0.35, 'Some flu cases in the area'),
    (NOW() - INTERVAL '7 days', 'Delhi', 'Delhi', 'Twitter', 62, 'fever', -0.40, 'Not feeling well today')
ON CONFLICT DO NOTHING;

DO $$
DECLARE
    row_count INTEGER;
BEGIN
    GET DIAGNOSTICS row_count = ROW_COUNT;
    RAISE NOTICE '✓ Inserted % social media records', row_count;
END $$;

-- =============================================
-- Sample Environmental Surveillance Data
-- =============================================
DO $$
BEGIN
    RAISE NOTICE 'Inserting environmental surveillance data...';
END $$;

INSERT INTO environmental_surveillance_data (timestamp, location, region, air_quality_index, water_quality_index, temperature, humidity, pollution_level)
VALUES
    (NOW() - INTERVAL '1 hour', 'Dadar', 'Mumbai', 156, 8.2, 32.5, 78, 'moderate'),
    (NOW() - INTERVAL '2 hours', 'Bandra', 'Mumbai', 148, 8.4, 31.8, 76, 'moderate'),
    (NOW() - INTERVAL '3 hours', 'Andheri', 'Mumbai', 162, 8.1, 33.2, 79, 'unhealthy_sensitive'),
    (NOW() - INTERVAL '1 day', 'Colaba', 'Mumbai', 135, 8.6, 30.5, 75, 'moderate'),
    
    (NOW() - INTERVAL '1 hour', 'Connaught Place', 'Delhi', 189, 7.8, 28.5, 65, 'unhealthy'),
    (NOW() - INTERVAL '2 hours', 'Dwarka', 'Delhi', 195, 7.6, 29.2, 68, 'unhealthy'),
    (NOW() - INTERVAL '3 hours', 'Rohini', 'Delhi', 178, 7.9, 27.8, 62, 'unhealthy_sensitive'),
    (NOW() - INTERVAL '1 day', 'Saket', 'Delhi', 202, 7.5, 30.1, 70, 'unhealthy'),
    
    (NOW() - INTERVAL '1 hour', 'Koramangala', 'Bangalore', 92, 8.8, 26.5, 68, 'moderate'),
    (NOW() - INTERVAL '2 hours', 'Whitefield', 'Bangalore', 88, 8.9, 25.8, 65, 'moderate'),
    (NOW() - INTERVAL '3 hours', 'Indiranagar', 'Bangalore', 95, 8.7, 27.2, 70, 'moderate'),
    (NOW() - INTERVAL '1 day', 'JP Nagar', 'Bangalore', 82, 9.0, 24.5, 62, 'good'),
    
    (NOW() - INTERVAL '7 days', 'Dadar', 'Mumbai', 142, 8.3, 31.0, 74, 'moderate'),
    (NOW() - INTERVAL '7 days', 'Connaught Place', 'Delhi', 175, 7.8, 29.5, 66, 'unhealthy_sensitive'),
    (NOW() - INTERVAL '7 days', 'Koramangala', 'Bangalore', 85, 8.8, 25.0, 64, 'moderate')
ON CONFLICT DO NOTHING;

DO $$
DECLARE
    row_count INTEGER;
BEGIN
    GET DIAGNOSTICS row_count = ROW_COUNT;
    RAISE NOTICE '✓ Inserted % environmental records', row_count;
END $$;

-- =============================================
-- Sample Pharmacy Surveillance Data
-- =============================================
DO $$
BEGIN
    RAISE NOTICE 'Inserting pharmacy surveillance data...';
END $$;

INSERT INTO pharmacy_surveillance_data (timestamp, location, region, pharmacy_name, medication_name, medication_category, prescription_count, is_otc)
VALUES
    -- Mumbai - Increased flu medication sales
    (NOW() - INTERVAL '1 hour', 'Andheri', 'Mumbai', 'Apollo Pharmacy', 'Paracetamol', 'antipyretic', 128, true),
    (NOW() - INTERVAL '1 hour', 'Andheri', 'Mumbai', 'Apollo Pharmacy', 'Cetirizine', 'antihistamine', 87, true),
    (NOW() - INTERVAL '2 hours', 'Dadar', 'Mumbai', 'MedPlus', 'Azithromycin', 'antibiotic', 45, false),
    (NOW() - INTERVAL '2 hours', 'Dadar', 'Mumbai', 'MedPlus', 'Cough Syrup', 'antitussive', 76, true),
    (NOW() - INTERVAL '3 hours', 'Bandra', 'Mumbai', 'Netmeds', 'Paracetamol', 'antipyretic', 142, true),
    (NOW() - INTERVAL '1 day', 'Colaba', 'Mumbai', 'PharmEasy', 'Ibuprofen', 'antipyretic', 95, true),
    
    -- Delhi - Dengue medication surge
    (NOW() - INTERVAL '1 hour', 'Connaught Place', 'Delhi', 'Apollo Pharmacy', 'Paracetamol', 'antipyretic', 156, true),
    (NOW() - INTERVAL '1 hour', 'Connaught Place', 'Delhi', 'Apollo Pharmacy', 'ORS', 'rehydration', 89, true),
    (NOW() - INTERVAL '2 hours', 'Dwarka', 'Delhi', 'MedPlus', 'Doxycycline', 'antibiotic', 34, false),
    (NOW() - INTERVAL '2 hours', 'Dwarka', 'Delhi', 'MedPlus', 'Platelet Support', 'supplement', 67, true),
    (NOW() - INTERVAL '1 day', 'Saket', 'Delhi', 'Netmeds', 'Paracetamol', 'antipyretic', 178, true),
    
    -- Bangalore - Normal patterns
    (NOW() - INTERVAL '1 hour', 'Koramangala', 'Bangalore', 'Apollo Pharmacy', 'Cetirizine', 'antihistamine', 45, true),
    (NOW() - INTERVAL '2 hours', 'Whitefield', 'Bangalore', 'MedPlus', 'Paracetamol', 'antipyretic', 52, true),
    (NOW() - INTERVAL '1 day', 'Indiranagar', 'Bangalore', 'Netmeds', 'Cough Syrup', 'antitussive', 38, true),
    
    -- Historical baseline (1 week ago)
    (NOW() - INTERVAL '7 days', 'Andheri', 'Mumbai', 'Apollo Pharmacy', 'Paracetamol', 'antipyretic', 48, true),
    (NOW() - INTERVAL '7 days', 'Connaught Place', 'Delhi', 'Apollo Pharmacy', 'Paracetamol', 'antipyretic', 52, true),
    (NOW() - INTERVAL '7 days', 'Koramangala', 'Bangalore', 'Apollo Pharmacy', 'Cetirizine', 'antihistamine', 35, true)
ON CONFLICT DO NOTHING;

DO $$
DECLARE
    row_count INTEGER;
BEGIN
    GET DIAGNOSTICS row_count = ROW_COUNT;
    RAISE NOTICE '✓ Inserted % pharmacy records', row_count;
END $$;

-- =============================================
-- Sample Anomaly Detections
-- =============================================
DO $$
BEGIN
    RAISE NOTICE 'Inserting anomaly detections...';
END $$;

INSERT INTO anomaly_detections (timestamp, location, region, anomaly_type, severity, confidence, data_source, baseline_value, current_value, deviation_percent, detection_method, metrics)
VALUES
    (NOW() - INTERVAL '1 hour', 'Mumbai', 'Mumbai', 'spike', 'high', 0.87, 'hospital', 15.0, 45.0, 200.0, 'statistical', 
     '{"symptom": "fever", "location": "Lilavati Hospital", "threshold_exceeded": true}'),
    
    (NOW() - INTERVAL '1 hour', 'Mumbai', 'Mumbai', 'spike', 'medium', 0.76, 'social_media', 87.0, 247.0, 184.0, 'ml_model',
     '{"platform": "Twitter", "keywords": ["fever", "flu"], "sentiment_drop": true}'),
    
    (NOW() - INTERVAL '2 hours', 'Mumbai', 'Mumbai', 'spike', 'high', 0.82, 'pharmacy', 48.0, 128.0, 167.0, 'statistical',
     '{"medication": "Paracetamol", "pharmacy_chain": "Apollo", "unusual_demand": true}'),
    
    (NOW() - INTERVAL '1 hour', 'Delhi', 'Delhi', 'spike', 'critical', 0.92, 'hospital', 10.0, 23.0, 130.0, 'statistical',
     '{"symptom": "dengue fever", "hospital": "AIIMS Delhi", "outbreak_indicator": true}'),
    
    (NOW() - INTERVAL '1 hour', 'Delhi', 'Delhi', 'spike', 'high', 0.85, 'social_media', 62.0, 198.0, 219.0, 'ml_model',
     '{"platform": "Twitter", "keywords": ["dengue", "fever"], "viral_spread": true}'),
    
    (NOW() - INTERVAL '2 hours', 'Delhi', 'Delhi', 'environmental', 'medium', 0.71, 'environmental', 175.0, 202.0, 15.4, 'temporal',
     '{"metric": "air_quality_index", "location": "Saket", "health_risk": "elevated"}')
ON CONFLICT DO NOTHING;

DO $$
DECLARE
    row_count INTEGER;
BEGIN
    GET DIAGNOSTICS row_count = ROW_COUNT;
    RAISE NOTICE '✓ Inserted % anomaly detections', row_count;
END $$;

-- =============================================
-- Sample Outbreak Predictions
-- =============================================
DO $$
BEGIN
    RAISE NOTICE 'Inserting outbreak predictions...';
END $$;

INSERT INTO outbreak_predictions (disease_name, region, forecast_weeks, predicted_cases, confidence, risk_level, model_used, prediction_json)
VALUES
    ('Influenza A', 'Mumbai', 2, 850, 0.78, 'high', 'SEIR',
     '{"r0": 2.3, "current_cases": 245, "growth_rate": 0.15, "intervention_impact": "low", "peak_week": 1}'),
    
    ('Influenza A', 'Mumbai', 4, 1200, 0.72, 'medium', 'SEIR',
     '{"r0": 2.3, "current_cases": 245, "growth_rate": 0.12, "intervention_impact": "medium", "peak_week": 2}'),
    
    ('Dengue Fever', 'Delhi', 2, 420, 0.85, 'critical', 'SEIR',
     '{"r0": 2.8, "current_cases": 156, "growth_rate": 0.22, "intervention_impact": "low", "peak_week": 1, "mosquito_density": "high"}'),
    
    ('Dengue Fever', 'Delhi', 4, 680, 0.79, 'high', 'SEIR',
     '{"r0": 2.8, "current_cases": 156, "growth_rate": 0.18, "intervention_impact": "medium", "peak_week": 2, "mosquito_density": "high"}'),
    
    ('Seasonal Flu', 'Bangalore', 2, 85, 0.65, 'low', 'SEIR',
     '{"r0": 1.4, "current_cases": 45, "growth_rate": 0.08, "intervention_impact": "low", "peak_week": 3}')
ON CONFLICT DO NOTHING;

DO $$
DECLARE
    row_count INTEGER;
BEGIN
    GET DIAGNOSTICS row_count = ROW_COUNT;
    RAISE NOTICE '✓ Inserted % outbreak predictions', row_count;
END $$;

-- =============================================
-- Sample Surveillance Alerts
-- =============================================
DO $$
BEGIN
    RAISE NOTICE 'Inserting surveillance alerts...';
END $$;

INSERT INTO surveillance_alerts (alert_id, alert_type, severity, region, disease_name, message, audience, status, alert_json)
VALUES
    ('ALERT-MUM-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-001', 'outbreak_warning', 'high', 'Mumbai', 'Influenza A',
     'Significant increase in flu-like symptoms detected across Mumbai hospitals. 200% spike in fever cases reported.',
     'health_officials,healthcare_providers', 'active',
     '{"affected_areas": ["Andheri", "Dadar", "Bandra"], "cases": 245, "trend": "rising", "recommendations": ["increase_surveillance", "prepare_resources"]}'),
    
    ('ALERT-DEL-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-001', 'outbreak_warning', 'critical', 'Delhi', 'Dengue Fever',
     'CRITICAL: Dengue outbreak confirmed in South Delhi. 130% increase in confirmed cases over baseline.',
     'health_officials,healthcare_providers,public', 'active',
     '{"affected_areas": ["Saket", "Dwarka", "Rohini"], "cases": 156, "trend": "rapidly_rising", "mosquito_control": "urgent", "recommendations": ["vector_control", "public_awareness", "hospital_preparedness"]}'),
    
    ('ALERT-MUM-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-002', 'resource_alert', 'medium', 'Mumbai', 'Influenza A',
     'Increased demand for antipyretic medications detected. Pharmacies reporting 167% increase in Paracetamol sales.',
     'health_officials,healthcare_providers', 'active',
     '{"medication": "Paracetamol", "supply_status": "adequate", "trend": "increasing_demand", "recommendations": ["monitor_stock"]}')
ON CONFLICT (alert_id) DO NOTHING;

DO $$
DECLARE
    row_count INTEGER;
BEGIN
    GET DIAGNOSTICS row_count = ROW_COUNT;
    RAISE NOTICE '✓ Inserted % surveillance alerts', row_count;
END $$;

-- =============================================
-- Sample Chat Session
-- =============================================
DO $$
BEGIN
    RAISE NOTICE 'Inserting sample chat session...';
END $$;

INSERT INTO chat_sessions (session_id, conversation_id, user_id, start_time, last_activity, status, session_data)
VALUES
    ('SESSION-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-001', 
     'CONV-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-001',
     'admin',
     NOW() - INTERVAL '1 hour',
     NOW(),
     'active',
     '{"user_query": "Analyze current disease surveillance status for Mumbai", "agents_involved": ["DATA_COLLECTION", "ANOMALY_DETECTION", "PREDICTION"], "alerts_generated": 1}')
ON CONFLICT (session_id) DO NOTHING;

DO $$
DECLARE
    row_count INTEGER;
BEGIN
    GET DIAGNOSTICS row_count = ROW_COUNT;
    RAISE NOTICE '✓ Inserted % chat session', row_count;
END $$;

-- =============================================
-- Final Summary
-- =============================================
DO $$
BEGIN
    RAISE NOTICE '';
    RAISE NOTICE '========================================';
    RAISE NOTICE '✓ All Sample Data Inserted Successfully!';
    RAISE NOTICE '========================================';
    RAISE NOTICE '';
    RAISE NOTICE 'Data Summary:';
    RAISE NOTICE '- Hospital records: 16 entries';
    RAISE NOTICE '- Social media records: 11 entries';
    RAISE NOTICE '- Environmental records: 15 entries';
    RAISE NOTICE '- Pharmacy records: 17 entries';
    RAISE NOTICE '- Anomaly detections: 6 entries';
    RAISE NOTICE '- Outbreak predictions: 5 entries';
    RAISE NOTICE '- Surveillance alerts: 3 entries';
    RAISE NOTICE '- Chat sessions: 1 entry';
    RAISE NOTICE '';
    RAISE NOTICE 'Sample scenarios included:';
    RAISE NOTICE '✓ Mumbai: Influenza A outbreak (high severity)';
    RAISE NOTICE '✓ Delhi: Dengue fever outbreak (critical severity)';
    RAISE NOTICE '✓ Bangalore: Normal surveillance patterns (low risk)';
    RAISE NOTICE '';
END $$;
