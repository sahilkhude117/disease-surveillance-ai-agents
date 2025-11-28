-- Disease Surveillance AI Agent System - Stored Procedures
-- Creates stored procedures for common database operations

USE [YourDatabaseName];
GO

-- =============================================
-- Stored Procedure: sp_LogSurveillanceReport
-- Description: Logs a generated surveillance report
-- =============================================
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_LogSurveillanceReport')
    DROP PROCEDURE sp_LogSurveillanceReport;
GO

CREATE PROCEDURE sp_LogSurveillanceReport
    @session_id VARCHAR(255),
    @conversation_id VARCHAR(255),
    @filename VARCHAR(500),
    @blob_url VARCHAR(MAX),
    @report_type VARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    
    INSERT INTO surveillance_reports (
        session_id,
        conversation_id,
        filename,
        blob_url,
        report_type,
        created_date
    )
    VALUES (
        @session_id,
        @conversation_id,
        @filename,
        @blob_url,
        @report_type,
        GETDATE()
    );
    
    SELECT 'Report logged successfully' AS Result;
END
GO
PRINT '✓ Created sp_LogSurveillanceReport';
GO

-- =============================================
-- Stored Procedure: sp_GetSurveillanceData
-- Description: Retrieves surveillance data from all sources
-- =============================================
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_GetSurveillanceData')
    DROP PROCEDURE sp_GetSurveillanceData;
GO

CREATE PROCEDURE sp_GetSurveillanceData
    @days INT = 7,
    @region VARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @start_date DATETIME = DATEADD(day, -@days, GETDATE());
    
    -- Hospital data
    SELECT 
        'hospital' AS data_source,
        timestamp,
        location,
        region,
        symptom_type,
        patient_count,
        age_group,
        severity_level
    FROM hospital_surveillance_data
    WHERE timestamp >= @start_date
        AND (@region IS NULL OR region = @region)
    ORDER BY timestamp DESC;
    
    -- Social media data
    SELECT 
        'social_media' AS data_source,
        timestamp,
        location,
        region,
        platform,
        mention_count,
        symptom_keywords,
        sentiment_score
    FROM social_media_surveillance_data
    WHERE timestamp >= @start_date
        AND (@region IS NULL OR region = @region)
    ORDER BY timestamp DESC;
    
    -- Environmental data
    SELECT 
        'environmental' AS data_source,
        timestamp,
        location,
        region,
        air_quality_index,
        water_quality_index,
        temperature,
        humidity,
        pollution_level
    FROM environmental_surveillance_data
    WHERE timestamp >= @start_date
        AND (@region IS NULL OR region = @region)
    ORDER BY timestamp DESC;
    
    -- Pharmacy data
    SELECT 
        'pharmacy' AS data_source,
        timestamp,
        location,
        region,
        medication_name,
        medication_category,
        prescription_count,
        is_otc
    FROM pharmacy_surveillance_data
    WHERE timestamp >= @start_date
        AND (@region IS NULL OR region = @region)
    ORDER BY timestamp DESC;
END
GO
PRINT '✓ Created sp_GetSurveillanceData';
GO

-- =============================================
-- Stored Procedure: sp_GetAnomalySummary
-- Description: Gets summary of anomalies by region and severity
-- =============================================
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_GetAnomalySummary')
    DROP PROCEDURE sp_GetAnomalySummary;
GO

CREATE PROCEDURE sp_GetAnomalySummary
    @days INT = 7,
    @region VARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @start_date DATETIME = DATEADD(day, -@days, GETDATE());
    
    SELECT 
        region,
        severity,
        anomaly_type,
        data_source,
        COUNT(*) AS anomaly_count,
        AVG(confidence) AS avg_confidence,
        MAX(timestamp) AS latest_detection
    FROM anomaly_detections
    WHERE timestamp >= @start_date
        AND (@region IS NULL OR region = @region)
    GROUP BY region, severity, anomaly_type, data_source
    ORDER BY severity DESC, anomaly_count DESC;
END
GO
PRINT '✓ Created sp_GetAnomalySummary';
GO

-- =============================================
-- Stored Procedure: sp_GetActiveAlerts
-- Description: Retrieves all active surveillance alerts
-- =============================================
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_GetActiveAlerts')
    DROP PROCEDURE sp_GetActiveAlerts;
GO

CREATE PROCEDURE sp_GetActiveAlerts
    @region VARCHAR(100) = NULL,
    @severity VARCHAR(50) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        alert_id,
        alert_type,
        severity,
        region,
        disease_name,
        message,
        audience,
        status,
        created_date
    FROM surveillance_alerts
    WHERE status = 'active'
        AND (@region IS NULL OR region = @region)
        AND (@severity IS NULL OR severity = @severity)
    ORDER BY 
        CASE severity
            WHEN 'critical' THEN 1
            WHEN 'high' THEN 2
            WHEN 'medium' THEN 3
            WHEN 'low' THEN 4
            ELSE 5
        END,
        created_date DESC;
END
GO
PRINT '✓ Created sp_GetActiveAlerts';
GO

-- =============================================
-- Stored Procedure: sp_GetPredictionHistory
-- Description: Retrieves outbreak prediction history
-- =============================================
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_GetPredictionHistory')
    DROP PROCEDURE sp_GetPredictionHistory;
GO

CREATE PROCEDURE sp_GetPredictionHistory
    @disease_name VARCHAR(255) = NULL,
    @region VARCHAR(100) = NULL,
    @days INT = 30
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @start_date DATETIME = DATEADD(day, -@days, GETDATE());
    
    SELECT 
        prediction_id,
        disease_name,
        region,
        forecast_weeks,
        predicted_cases,
        confidence,
        risk_level,
        model_used,
        created_date
    FROM outbreak_predictions
    WHERE created_date >= @start_date
        AND (@disease_name IS NULL OR disease_name = @disease_name)
        AND (@region IS NULL OR region = @region)
    ORDER BY created_date DESC;
END
GO
PRINT '✓ Created sp_GetPredictionHistory';
GO

-- =============================================
-- Stored Procedure: sp_GetThinkingLogs
-- Description: Retrieves agent thinking logs for a session
-- =============================================
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_GetThinkingLogs')
    DROP PROCEDURE sp_GetThinkingLogs;
GO

CREATE PROCEDURE sp_GetThinkingLogs
    @session_id VARCHAR(255) = NULL,
    @conversation_id VARCHAR(255) = NULL,
    @agent_name VARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        thinking_id,
        agent_name,
        thinking_stage,
        thought_content,
        thinking_stage_output,
        agent_output,
        conversation_id,
        session_id,
        user_query,
        status,
        created_date
    FROM agent_thinking_logs
    WHERE (@session_id IS NULL OR session_id = @session_id)
        AND (@conversation_id IS NULL OR conversation_id = @conversation_id)
        AND (@agent_name IS NULL OR agent_name = @agent_name)
    ORDER BY created_date ASC;
END
GO
PRINT '✓ Created sp_GetThinkingLogs';
GO

-- =============================================
-- Stored Procedure: sp_CleanupOldData
-- Description: Archives or deletes old surveillance data
-- =============================================
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_CleanupOldData')
    DROP PROCEDURE sp_CleanupOldData;
GO

CREATE PROCEDURE sp_CleanupOldData
    @days_to_keep INT = 90
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @cutoff_date DATETIME = DATEADD(day, -@days_to_keep, GETDATE());
    DECLARE @deleted_count INT = 0;
    
    -- Delete old hospital data
    DELETE FROM hospital_surveillance_data WHERE timestamp < @cutoff_date;
    SET @deleted_count = @deleted_count + @@ROWCOUNT;
    
    -- Delete old social media data
    DELETE FROM social_media_surveillance_data WHERE timestamp < @cutoff_date;
    SET @deleted_count = @deleted_count + @@ROWCOUNT;
    
    -- Delete old environmental data
    DELETE FROM environmental_surveillance_data WHERE timestamp < @cutoff_date;
    SET @deleted_count = @deleted_count + @@ROWCOUNT;
    
    -- Delete old pharmacy data
    DELETE FROM pharmacy_surveillance_data WHERE timestamp < @cutoff_date;
    SET @deleted_count = @deleted_count + @@ROWCOUNT;
    
    -- Delete old anomaly detections
    DELETE FROM anomaly_detections WHERE timestamp < @cutoff_date;
    SET @deleted_count = @deleted_count + @@ROWCOUNT;
    
    SELECT 
        @deleted_count AS total_records_deleted,
        @cutoff_date AS cutoff_date,
        GETDATE() AS cleanup_timestamp;
END
GO
PRINT '✓ Created sp_CleanupOldData';
GO

PRINT '';
PRINT '========================================';
PRINT '✓ All Stored Procedures Created Successfully!';
PRINT '========================================';
GO
