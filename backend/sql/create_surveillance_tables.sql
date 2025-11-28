-- Disease Surveillance AI Agent System - Database Schema
-- Creates all tables needed for disease surveillance monitoring

USE [YourDatabaseName];
GO

-- =============================================
-- 1. Hospital Surveillance Data Table
-- =============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='hospital_surveillance_data' AND xtype='U')
BEGIN
    CREATE TABLE hospital_surveillance_data (
        record_id INT IDENTITY(1,1) PRIMARY KEY,
        timestamp DATETIME NOT NULL DEFAULT GETDATE(),
        location VARCHAR(255) NOT NULL,
        region VARCHAR(100) NOT NULL,
        facility_name VARCHAR(255),
        symptom_type VARCHAR(100),
        patient_count INT NOT NULL DEFAULT 0,
        age_group VARCHAR(50),
        severity_level VARCHAR(50),
        diagnosis VARCHAR(255),
        created_date DATETIME NOT NULL DEFAULT GETDATE(),
        INDEX idx_timestamp (timestamp),
        INDEX idx_region (region),
        INDEX idx_symptom (symptom_type)
    );
    PRINT '✓ Created hospital_surveillance_data table';
END
GO

-- =============================================
-- 2. Social Media Surveillance Data Table
-- =============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='social_media_surveillance_data' AND xtype='U')
BEGIN
    CREATE TABLE social_media_surveillance_data (
        record_id INT IDENTITY(1,1) PRIMARY KEY,
        timestamp DATETIME NOT NULL DEFAULT GETDATE(),
        location VARCHAR(255),
        region VARCHAR(100),
        platform VARCHAR(50),
        mention_count INT NOT NULL DEFAULT 0,
        symptom_keywords VARCHAR(MAX),
        sentiment_score FLOAT,
        language VARCHAR(50),
        post_content VARCHAR(MAX),
        created_date DATETIME NOT NULL DEFAULT GETDATE(),
        INDEX idx_timestamp (timestamp),
        INDEX idx_region (region)
    );
    PRINT '✓ Created social_media_surveillance_data table';
END
GO

-- =============================================
-- 3. Environmental Surveillance Data Table
-- =============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='environmental_surveillance_data' AND xtype='U')
BEGIN
    CREATE TABLE environmental_surveillance_data (
        record_id INT IDENTITY(1,1) PRIMARY KEY,
        timestamp DATETIME NOT NULL DEFAULT GETDATE(),
        location VARCHAR(255) NOT NULL,
        region VARCHAR(100) NOT NULL,
        air_quality_index FLOAT,
        water_quality_index FLOAT,
        temperature FLOAT,
        humidity FLOAT,
        pollution_level VARCHAR(50),
        weather_conditions VARCHAR(255),
        created_date DATETIME NOT NULL DEFAULT GETDATE(),
        INDEX idx_timestamp (timestamp),
        INDEX idx_region (region)
    );
    PRINT '✓ Created environmental_surveillance_data table';
END
GO

-- =============================================
-- 4. Pharmacy Surveillance Data Table
-- =============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='pharmacy_surveillance_data' AND xtype='U')
BEGIN
    CREATE TABLE pharmacy_surveillance_data (
        record_id INT IDENTITY(1,1) PRIMARY KEY,
        timestamp DATETIME NOT NULL DEFAULT GETDATE(),
        location VARCHAR(255) NOT NULL,
        region VARCHAR(100) NOT NULL,
        pharmacy_name VARCHAR(255),
        medication_name VARCHAR(255),
        medication_category VARCHAR(100),
        prescription_count INT NOT NULL DEFAULT 0,
        is_otc BIT NOT NULL DEFAULT 0,
        created_date DATETIME NOT NULL DEFAULT GETDATE(),
        INDEX idx_timestamp (timestamp),
        INDEX idx_region (region),
        INDEX idx_medication (medication_category)
    );
    PRINT '✓ Created pharmacy_surveillance_data table';
END
GO

-- =============================================
-- 5. Anomaly Detections Table
-- =============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='anomaly_detections' AND xtype='U')
BEGIN
    CREATE TABLE anomaly_detections (
        anomaly_id INT IDENTITY(1,1) PRIMARY KEY,
        timestamp DATETIME NOT NULL,
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
        metrics VARCHAR(MAX),
        session_id VARCHAR(255),
        created_date DATETIME NOT NULL DEFAULT GETDATE(),
        INDEX idx_timestamp (timestamp),
        INDEX idx_region (region),
        INDEX idx_severity (severity),
        INDEX idx_session (session_id)
    );
    PRINT '✓ Created anomaly_detections table';
END
GO

-- =============================================
-- 6. Outbreak Predictions Table
-- =============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='outbreak_predictions' AND xtype='U')
BEGIN
    CREATE TABLE outbreak_predictions (
        prediction_id INT IDENTITY(1,1) PRIMARY KEY,
        disease_name VARCHAR(255) NOT NULL,
        region VARCHAR(100) NOT NULL,
        forecast_weeks INT NOT NULL,
        predicted_cases INT,
        confidence FLOAT,
        risk_level VARCHAR(50),
        model_used VARCHAR(100),
        prediction_json VARCHAR(MAX),
        session_id VARCHAR(255),
        created_date DATETIME NOT NULL DEFAULT GETDATE(),
        INDEX idx_disease (disease_name),
        INDEX idx_region (region),
        INDEX idx_created (created_date)
    );
    PRINT '✓ Created outbreak_predictions table';
END
GO

-- =============================================
-- 7. Surveillance Alerts Table
-- =============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='surveillance_alerts' AND xtype='U')
BEGIN
    CREATE TABLE surveillance_alerts (
        alert_id VARCHAR(255) PRIMARY KEY,
        alert_type VARCHAR(100) NOT NULL,
        severity VARCHAR(50) NOT NULL,
        region VARCHAR(100) NOT NULL,
        disease_name VARCHAR(255),
        message VARCHAR(MAX) NOT NULL,
        audience VARCHAR(100) NOT NULL,
        status VARCHAR(50) NOT NULL DEFAULT 'active',
        alert_json VARCHAR(MAX),
        session_id VARCHAR(255),
        created_date DATETIME NOT NULL DEFAULT GETDATE(),
        updated_date DATETIME,
        INDEX idx_status (status),
        INDEX idx_severity (severity),
        INDEX idx_region (region),
        INDEX idx_disease (disease_name)
    );
    PRINT '✓ Created surveillance_alerts table';
END
GO

-- =============================================
-- 8. Surveillance Reports Table
-- =============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='surveillance_reports' AND xtype='U')
BEGIN
    CREATE TABLE surveillance_reports (
        report_id INT IDENTITY(1,1) PRIMARY KEY,
        session_id VARCHAR(255) NOT NULL,
        conversation_id VARCHAR(255),
        filename VARCHAR(500) NOT NULL,
        blob_url VARCHAR(MAX),
        report_type VARCHAR(100) NOT NULL,
        created_date DATETIME NOT NULL DEFAULT GETDATE(),
        INDEX idx_session (session_id),
        INDEX idx_conversation (conversation_id),
        INDEX idx_type (report_type)
    );
    PRINT '✓ Created surveillance_reports table';
END
GO

-- =============================================
-- 9. Agent Thinking Logs Table
-- =============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='agent_thinking_logs' AND xtype='U')
BEGIN
    CREATE TABLE agent_thinking_logs (
        thinking_id INT IDENTITY(1,1) PRIMARY KEY,
        agent_name VARCHAR(100) NOT NULL,
        thinking_stage VARCHAR(100) NOT NULL,
        thought_content VARCHAR(MAX),
        thinking_stage_output VARCHAR(MAX),
        agent_output VARCHAR(MAX),
        conversation_id VARCHAR(255),
        session_id VARCHAR(255),
        azure_agent_id VARCHAR(255),
        model_deployment_name VARCHAR(255),
        thread_id VARCHAR(255),
        user_query VARCHAR(MAX),
        status VARCHAR(50) NOT NULL DEFAULT 'success',
        created_date DATETIME NOT NULL DEFAULT GETDATE(),
        INDEX idx_agent (agent_name),
        INDEX idx_conversation (conversation_id),
        INDEX idx_session (session_id),
        INDEX idx_created (created_date)
    );
    PRINT '✓ Created agent_thinking_logs table';
END
GO

-- =============================================
-- 10. Chat Sessions Table
-- =============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='chat_sessions' AND xtype='U')
BEGIN
    CREATE TABLE chat_sessions (
        session_id VARCHAR(255) PRIMARY KEY,
        conversation_id VARCHAR(255),
        user_id VARCHAR(255),
        start_time DATETIME NOT NULL DEFAULT GETDATE(),
        last_activity DATETIME NOT NULL DEFAULT GETDATE(),
        status VARCHAR(50) NOT NULL DEFAULT 'active',
        session_data VARCHAR(MAX),
        INDEX idx_user (user_id),
        INDEX idx_status (status),
        INDEX idx_activity (last_activity)
    );
    PRINT '✓ Created chat_sessions table';
END
GO

PRINT '';
PRINT '========================================';
PRINT '✓ Disease Surveillance Database Schema Created Successfully!';
PRINT '========================================';
PRINT '';
PRINT 'Tables created:';
PRINT '  1. hospital_surveillance_data';
PRINT '  2. social_media_surveillance_data';
PRINT '  3. environmental_surveillance_data';
PRINT '  4. pharmacy_surveillance_data';
PRINT '  5. anomaly_detections';
PRINT '  6. outbreak_predictions';
PRINT '  7. surveillance_alerts';
PRINT '  8. surveillance_reports';
PRINT '  9. agent_thinking_logs';
PRINT '  10. chat_sessions';
PRINT '';
GO
