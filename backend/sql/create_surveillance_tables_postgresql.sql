
-- =============================================
-- 1. Hospital Surveillance Data Table
-- =============================================
CREATE TABLE IF NOT EXISTS hospital_surveillance_data (
    record_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    location VARCHAR(255) NOT NULL,
    region VARCHAR(100) NOT NULL,
    facility_name VARCHAR(255),
    symptom_type VARCHAR(100),
    patient_count INTEGER NOT NULL DEFAULT 0,
    age_group VARCHAR(50),
    severity_level VARCHAR(50),
    diagnosis VARCHAR(255),
    created_date TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_hospital_timestamp ON hospital_surveillance_data(timestamp);
CREATE INDEX IF NOT EXISTS idx_hospital_region ON hospital_surveillance_data(region);
CREATE INDEX IF NOT EXISTS idx_hospital_symptom ON hospital_surveillance_data(symptom_type);

-- =============================================
-- 2. Social Media Surveillance Data Table
-- =============================================
CREATE TABLE IF NOT EXISTS social_media_surveillance_data (
    record_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    location VARCHAR(255),
    region VARCHAR(100),
    platform VARCHAR(50),
    mention_count INTEGER NOT NULL DEFAULT 0,
    symptom_keywords TEXT,
    sentiment_score FLOAT,
    language VARCHAR(50),
    post_content TEXT,
    created_date TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_social_timestamp ON social_media_surveillance_data(timestamp);
CREATE INDEX IF NOT EXISTS idx_social_region ON social_media_surveillance_data(region);

-- =============================================
-- 3. Environmental Surveillance Data Table
-- =============================================
CREATE TABLE IF NOT EXISTS environmental_surveillance_data (
    record_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    location VARCHAR(255) NOT NULL,
    region VARCHAR(100) NOT NULL,
    air_quality_index FLOAT,
    water_quality_index FLOAT,
    temperature FLOAT,
    humidity FLOAT,
    pollution_level VARCHAR(50),
    weather_conditions VARCHAR(255),
    created_date TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_env_timestamp ON environmental_surveillance_data(timestamp);
CREATE INDEX IF NOT EXISTS idx_env_region ON environmental_surveillance_data(region);

-- =============================================
-- 4. Pharmacy Surveillance Data Table
-- =============================================
CREATE TABLE IF NOT EXISTS pharmacy_surveillance_data (
    record_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    location VARCHAR(255) NOT NULL,
    region VARCHAR(100) NOT NULL,
    pharmacy_name VARCHAR(255),
    medication_name VARCHAR(255),
    medication_category VARCHAR(100),
    prescription_count INTEGER NOT NULL DEFAULT 0,
    is_otc BOOLEAN NOT NULL DEFAULT FALSE,
    created_date TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_pharmacy_timestamp ON pharmacy_surveillance_data(timestamp);
CREATE INDEX IF NOT EXISTS idx_pharmacy_region ON pharmacy_surveillance_data(region);
CREATE INDEX IF NOT EXISTS idx_pharmacy_medication ON pharmacy_surveillance_data(medication_category);

-- =============================================
-- 5. Anomaly Detections Table
-- =============================================
CREATE TABLE IF NOT EXISTS anomaly_detections (
    anomaly_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    location VARCHAR(255) NOT NULL,
    region VARCHAR(100),
    anomaly_type VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    confidence FLOAT NOT NULL,
    data_source VARCHAR(100) NOT NULL,
    baseline_value FLOAT,
    current_value FLOAT,
    deviation_percent FLOAT,
    detection_method VARCHAR(100),
    metrics TEXT,
    session_id VARCHAR(255),
    created_date TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_anomaly_timestamp ON anomaly_detections(timestamp);
CREATE INDEX IF NOT EXISTS idx_anomaly_region ON anomaly_detections(region);
CREATE INDEX IF NOT EXISTS idx_anomaly_severity ON anomaly_detections(severity);
CREATE INDEX IF NOT EXISTS idx_anomaly_session ON anomaly_detections(session_id);

-- =============================================
-- 6. Outbreak Predictions Table
-- =============================================
CREATE TABLE IF NOT EXISTS outbreak_predictions (
    prediction_id SERIAL PRIMARY KEY,
    disease_name VARCHAR(255) NOT NULL,
    region VARCHAR(100) NOT NULL,
    forecast_weeks INTEGER NOT NULL,
    predicted_cases INTEGER,
    confidence FLOAT,
    risk_level VARCHAR(50),
    model_used VARCHAR(100),
    prediction_json TEXT,
    session_id VARCHAR(255),
    created_date TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_prediction_disease ON outbreak_predictions(disease_name);
CREATE INDEX IF NOT EXISTS idx_prediction_region ON outbreak_predictions(region);
CREATE INDEX IF NOT EXISTS idx_prediction_created ON outbreak_predictions(created_date);

-- =============================================
-- 7. Surveillance Alerts Table
-- =============================================
CREATE TABLE IF NOT EXISTS surveillance_alerts (
    alert_id VARCHAR(255) PRIMARY KEY,
    alert_type VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    region VARCHAR(100) NOT NULL,
    disease_name VARCHAR(255),
    message TEXT NOT NULL,
    audience VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    alert_json TEXT,
    session_id VARCHAR(255),
    created_date TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_date TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_alert_status ON surveillance_alerts(status);
CREATE INDEX IF NOT EXISTS idx_alert_severity ON surveillance_alerts(severity);
CREATE INDEX IF NOT EXISTS idx_alert_region ON surveillance_alerts(region);
CREATE INDEX IF NOT EXISTS idx_alert_disease ON surveillance_alerts(disease_name);

-- =============================================
-- 8. Surveillance Reports Table
-- =============================================
CREATE TABLE IF NOT EXISTS surveillance_reports (
    report_id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    conversation_id VARCHAR(255),
    filename VARCHAR(500) NOT NULL,
    blob_url TEXT,
    report_type VARCHAR(100) NOT NULL,
    created_date TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_report_session ON surveillance_reports(session_id);
CREATE INDEX IF NOT EXISTS idx_report_conversation ON surveillance_reports(conversation_id);
CREATE INDEX IF NOT EXISTS idx_report_type ON surveillance_reports(report_type);

-- =============================================
-- 9. Agent Thinking Logs Table
-- =============================================
CREATE TABLE IF NOT EXISTS agent_thinking_logs (
    thinking_id SERIAL PRIMARY KEY,
    agent_name VARCHAR(100) NOT NULL,
    thinking_stage VARCHAR(100) NOT NULL,
    thought_content TEXT,
    thinking_stage_output TEXT,
    agent_output TEXT,
    conversation_id VARCHAR(255),
    session_id VARCHAR(255),
    azure_agent_id VARCHAR(255),  -- Legacy field, kept for compatibility
    model_deployment_name VARCHAR(255),
    thread_id VARCHAR(255),
    user_query TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'success',
    created_date TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_thinking_agent ON agent_thinking_logs(agent_name);
CREATE INDEX IF NOT EXISTS idx_thinking_conversation ON agent_thinking_logs(conversation_id);
CREATE INDEX IF NOT EXISTS idx_thinking_session ON agent_thinking_logs(session_id);
CREATE INDEX IF NOT EXISTS idx_thinking_created ON agent_thinking_logs(created_date);

-- =============================================
-- 10. Chat Sessions Table
-- =============================================
CREATE TABLE IF NOT EXISTS chat_sessions (
    session_id VARCHAR(255) PRIMARY KEY,
    conversation_id VARCHAR(255),
    user_id VARCHAR(255),
    start_time TIMESTAMP NOT NULL DEFAULT NOW(),
    last_activity TIMESTAMP NOT NULL DEFAULT NOW(),
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    session_data TEXT
);

CREATE INDEX IF NOT EXISTS idx_session_user ON chat_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_session_status ON chat_sessions(status);
CREATE INDEX IF NOT EXISTS idx_session_activity ON chat_sessions(last_activity);

-- =============================================
-- Insert Sample Data
-- =============================================
INSERT INTO hospital_surveillance_data (region, location, facility_name, symptom_type, patient_count, severity_level, diagnosis)
VALUES 
    ('Mumbai', 'Mumbai Central', 'Lilavati Hospital', 'Respiratory', 25, 'moderate', 'Influenza'),
    ('Mumbai', 'Andheri', 'KEM Hospital', 'Respiratory', 18, 'moderate', 'Influenza'),
    ('Delhi', 'South Delhi', 'AIIMS Delhi', 'Fever', 30, 'high', 'Dengue'),
    ('Bangalore', 'Whitefield', 'Manipal Hospital', 'Respiratory', 12, 'low', 'Common Cold')
ON CONFLICT DO NOTHING;

INSERT INTO environmental_surveillance_data (region, location, air_quality_index, water_quality_index, temperature, humidity)
VALUES
    ('Mumbai', 'Mumbai Central', 85.5, 72.3, 32.5, 78.2),
    ('Delhi', 'South Delhi', 120.8, 65.0, 38.2, 55.6),
    ('Bangalore', 'Whitefield', 45.2, 88.5, 28.0, 62.4)
ON CONFLICT DO NOTHING;

-- =============================================
-- Comments for Documentation
-- =============================================
COMMENT ON TABLE hospital_surveillance_data IS 'Stores hospital visit and disease case data from healthcare facilities';
COMMENT ON TABLE social_media_surveillance_data IS 'Stores social media mentions and sentiment analysis related to health symptoms';
COMMENT ON TABLE environmental_surveillance_data IS 'Stores environmental factors like air quality, temperature that may affect health';
COMMENT ON TABLE pharmacy_surveillance_data IS 'Stores pharmacy medication sales data for outbreak detection';
COMMENT ON TABLE anomaly_detections IS 'Stores detected anomalies in surveillance data with severity and confidence scores';
COMMENT ON TABLE outbreak_predictions IS 'Stores disease outbreak predictions with forecast data';
COMMENT ON TABLE surveillance_alerts IS 'Stores generated alerts for public health officials';
COMMENT ON TABLE surveillance_reports IS 'Stores generated surveillance reports metadata';
COMMENT ON TABLE agent_thinking_logs IS 'Stores AI agent thinking process logs for transparency';
COMMENT ON TABLE chat_sessions IS 'Stores user chat session information';

-- =============================================
-- Success Message
-- =============================================
DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE '✓ Disease Surveillance Database Schema Created Successfully!';
    RAISE NOTICE '========================================';
    RAISE NOTICE '';
    RAISE NOTICE 'Tables created:';
    RAISE NOTICE '  1. hospital_surveillance_data';
    RAISE NOTICE '  2. social_media_surveillance_data';
    RAISE NOTICE '  3. environmental_surveillance_data';
    RAISE NOTICE '  4. pharmacy_surveillance_data';
    RAISE NOTICE '  5. anomaly_detections';
    RAISE NOTICE '  6. outbreak_predictions';
    RAISE NOTICE '  7. surveillance_alerts';
    RAISE NOTICE '  8. surveillance_reports';
    RAISE NOTICE '  9. agent_thinking_logs';
    RAISE NOTICE '  10. chat_sessions';
    RAISE NOTICE '';
    RAISE NOTICE 'Sample data inserted successfully!';
    RAISE NOTICE '';
    RAISE NOTICE 'Next steps:';
    RAISE NOTICE '  1. Update your .env file with Supabase connection string';
    RAISE NOTICE '  2. Test connection: python backend/utils/database_utils.py';
    RAISE NOTICE '  3. Run the application: python backend/main.py';
    RAISE NOTICE '';
END $$;
