-- Disease Surveillance AI Agent System - PostgreSQL Functions
-- Creates functions (stored procedures) for common database operations

-- =============================================
-- Function: log_surveillance_report
-- Description: Logs a generated surveillance report
-- =============================================
CREATE OR REPLACE FUNCTION log_surveillance_report(
    p_session_id VARCHAR(255),
    p_conversation_id VARCHAR(255),
    p_filename VARCHAR(500),
    p_blob_url TEXT,
    p_report_type VARCHAR(100)
)
RETURNS TABLE(result TEXT) AS $$
BEGIN
    INSERT INTO surveillance_reports (
        session_id,
        conversation_id,
        filename,
        blob_url,
        report_type,
        created_date
    )
    VALUES (
        p_session_id,
        p_conversation_id,
        p_filename,
        p_blob_url,
        p_report_type,
        NOW()
    );
    
    RETURN QUERY SELECT 'Report logged successfully'::TEXT;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION log_surveillance_report IS 'Logs a generated surveillance report to the database';

-- =============================================
-- Function: get_surveillance_data
-- Description: Retrieves surveillance data from all sources
-- =============================================
CREATE OR REPLACE FUNCTION get_surveillance_data(
    p_days INTEGER DEFAULT 7,
    p_region VARCHAR(100) DEFAULT NULL
)
RETURNS TABLE(
    data_source VARCHAR,
    timestamp TIMESTAMP,
    location VARCHAR,
    region VARCHAR,
    metric1 VARCHAR,
    metric2 INTEGER,
    metric3 VARCHAR,
    metric4 FLOAT
) AS $$
DECLARE
    v_start_date TIMESTAMP := NOW() - (p_days || ' days')::INTERVAL;
BEGIN
    -- Hospital data
    RETURN QUERY
    SELECT 
        'hospital'::VARCHAR AS data_source,
        h.timestamp,
        h.location::VARCHAR,
        h.region::VARCHAR,
        h.symptom_type::VARCHAR AS metric1,
        h.patient_count AS metric2,
        h.severity_level::VARCHAR AS metric3,
        NULL::FLOAT AS metric4
    FROM hospital_surveillance_data h
    WHERE h.timestamp >= v_start_date
        AND (p_region IS NULL OR h.region = p_region)
    ORDER BY h.timestamp DESC;
    
    -- Social media data
    RETURN QUERY
    SELECT 
        'social_media'::VARCHAR AS data_source,
        s.timestamp,
        s.location::VARCHAR,
        s.region::VARCHAR,
        s.platform::VARCHAR AS metric1,
        s.mention_count AS metric2,
        s.symptom_keywords::VARCHAR AS metric3,
        s.sentiment_score AS metric4
    FROM social_media_surveillance_data s
    WHERE s.timestamp >= v_start_date
        AND (p_region IS NULL OR s.region = p_region)
    ORDER BY s.timestamp DESC;
    
    -- Environmental data
    RETURN QUERY
    SELECT 
        'environmental'::VARCHAR AS data_source,
        e.timestamp,
        e.location::VARCHAR,
        e.region::VARCHAR,
        e.pollution_level::VARCHAR AS metric1,
        NULL::INTEGER AS metric2,
        NULL::VARCHAR AS metric3,
        e.air_quality_index AS metric4
    FROM environmental_surveillance_data e
    WHERE e.timestamp >= v_start_date
        AND (p_region IS NULL OR e.region = p_region)
    ORDER BY e.timestamp DESC;
    
    -- Pharmacy data
    RETURN QUERY
    SELECT 
        'pharmacy'::VARCHAR AS data_source,
        p.timestamp,
        p.location::VARCHAR,
        p.region::VARCHAR,
        p.medication_name::VARCHAR AS metric1,
        p.prescription_count AS metric2,
        p.medication_category::VARCHAR AS metric3,
        NULL::FLOAT AS metric4
    FROM pharmacy_surveillance_data p
    WHERE p.timestamp >= v_start_date
        AND (p_region IS NULL OR p.region = p_region)
    ORDER BY p.timestamp DESC;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_surveillance_data IS 'Retrieves surveillance data from all sources for a given time period and optional region';

-- =============================================
-- Function: get_anomaly_summary
-- Description: Gets summary of anomalies by region and severity
-- =============================================
CREATE OR REPLACE FUNCTION get_anomaly_summary(
    p_days INTEGER DEFAULT 7,
    p_region VARCHAR(100) DEFAULT NULL
)
RETURNS TABLE(
    region VARCHAR,
    severity VARCHAR,
    anomaly_type VARCHAR,
    data_source VARCHAR,
    anomaly_count BIGINT,
    avg_confidence FLOAT,
    latest_detection TIMESTAMP
) AS $$
DECLARE
    v_start_date TIMESTAMP := NOW() - (p_days || ' days')::INTERVAL;
BEGIN
    RETURN QUERY
    SELECT 
        a.region::VARCHAR,
        a.severity::VARCHAR,
        a.anomaly_type::VARCHAR,
        a.data_source::VARCHAR,
        COUNT(*)::BIGINT AS anomaly_count,
        AVG(a.confidence)::FLOAT AS avg_confidence,
        MAX(a.timestamp)::TIMESTAMP AS latest_detection
    FROM anomaly_detections a
    WHERE a.timestamp >= v_start_date
        AND (p_region IS NULL OR a.region = p_region)
    GROUP BY a.region, a.severity, a.anomaly_type, a.data_source
    ORDER BY 
        CASE a.severity
            WHEN 'critical' THEN 1
            WHEN 'high' THEN 2
            WHEN 'medium' THEN 3
            WHEN 'low' THEN 4
            ELSE 5
        END,
        anomaly_count DESC;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_anomaly_summary IS 'Returns aggregated anomaly statistics grouped by region, severity, type and data source';

-- =============================================
-- Function: get_active_alerts
-- Description: Retrieves all active surveillance alerts
-- =============================================
CREATE OR REPLACE FUNCTION get_active_alerts(
    p_region VARCHAR(100) DEFAULT NULL,
    p_severity VARCHAR(50) DEFAULT NULL
)
RETURNS TABLE(
    alert_id VARCHAR,
    alert_type VARCHAR,
    severity VARCHAR,
    region VARCHAR,
    disease_name VARCHAR,
    message TEXT,
    audience VARCHAR,
    status VARCHAR,
    created_date TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.alert_id::VARCHAR,
        a.alert_type::VARCHAR,
        a.severity::VARCHAR,
        a.region::VARCHAR,
        a.disease_name::VARCHAR,
        a.message,
        a.audience::VARCHAR,
        a.status::VARCHAR,
        a.created_date
    FROM surveillance_alerts a
    WHERE a.status = 'active'
        AND (p_region IS NULL OR a.region = p_region)
        AND (p_severity IS NULL OR a.severity = p_severity)
    ORDER BY 
        CASE a.severity
            WHEN 'critical' THEN 1
            WHEN 'high' THEN 2
            WHEN 'medium' THEN 3
            WHEN 'low' THEN 4
            ELSE 5
        END,
        a.created_date DESC;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_active_alerts IS 'Retrieves all active surveillance alerts filtered by optional region and severity';

-- =============================================
-- Function: get_prediction_history
-- Description: Retrieves outbreak prediction history
-- =============================================
CREATE OR REPLACE FUNCTION get_prediction_history(
    p_disease_name VARCHAR(255) DEFAULT NULL,
    p_region VARCHAR(100) DEFAULT NULL,
    p_days INTEGER DEFAULT 30
)
RETURNS TABLE(
    prediction_id INTEGER,
    disease_name VARCHAR,
    region VARCHAR,
    forecast_weeks INTEGER,
    predicted_cases INTEGER,
    confidence FLOAT,
    risk_level VARCHAR,
    model_used VARCHAR,
    created_date TIMESTAMP
) AS $$
DECLARE
    v_start_date TIMESTAMP := NOW() - (p_days || ' days')::INTERVAL;
BEGIN
    RETURN QUERY
    SELECT 
        p.prediction_id,
        p.disease_name::VARCHAR,
        p.region::VARCHAR,
        p.forecast_weeks,
        p.predicted_cases,
        p.confidence,
        p.risk_level::VARCHAR,
        p.model_used::VARCHAR,
        p.created_date
    FROM outbreak_predictions p
    WHERE p.created_date >= v_start_date
        AND (p_disease_name IS NULL OR p.disease_name = p_disease_name)
        AND (p_region IS NULL OR p.region = p_region)
    ORDER BY p.created_date DESC;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_prediction_history IS 'Retrieves outbreak prediction history filtered by disease, region and time period';

-- =============================================
-- Function: get_thinking_logs
-- Description: Retrieves agent thinking logs for a session
-- =============================================
CREATE OR REPLACE FUNCTION get_thinking_logs(
    p_session_id VARCHAR(255) DEFAULT NULL,
    p_conversation_id VARCHAR(255) DEFAULT NULL,
    p_agent_name VARCHAR(100) DEFAULT NULL
)
RETURNS TABLE(
    thinking_id INTEGER,
    agent_name VARCHAR,
    thinking_stage VARCHAR,
    thought_content TEXT,
    thinking_stage_output TEXT,
    agent_output TEXT,
    conversation_id VARCHAR,
    session_id VARCHAR,
    user_query TEXT,
    status VARCHAR,
    created_date TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        t.thinking_id,
        t.agent_name::VARCHAR,
        t.thinking_stage::VARCHAR,
        t.thought_content,
        t.thinking_stage_output,
        t.agent_output,
        t.conversation_id::VARCHAR,
        t.session_id::VARCHAR,
        t.user_query,
        t.status::VARCHAR,
        t.created_date
    FROM agent_thinking_logs t
    WHERE (p_session_id IS NULL OR t.session_id = p_session_id)
        AND (p_conversation_id IS NULL OR t.conversation_id = p_conversation_id)
        AND (p_agent_name IS NULL OR t.agent_name = p_agent_name)
    ORDER BY t.created_date ASC;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_thinking_logs IS 'Retrieves AI agent thinking logs for transparency and debugging';

-- =============================================
-- Function: cleanup_old_data
-- Description: Archives or deletes old surveillance data
-- =============================================
CREATE OR REPLACE FUNCTION cleanup_old_data(
    p_days_to_keep INTEGER DEFAULT 90
)
RETURNS TABLE(
    total_records_deleted INTEGER,
    cutoff_date TIMESTAMP,
    cleanup_timestamp TIMESTAMP
) AS $$
DECLARE
    v_cutoff_date TIMESTAMP := NOW() - (p_days_to_keep || ' days')::INTERVAL;
    v_deleted_count INTEGER := 0;
    v_temp_count INTEGER;
BEGIN
    -- Delete old hospital data
    DELETE FROM hospital_surveillance_data WHERE timestamp < v_cutoff_date;
    GET DIAGNOSTICS v_temp_count = ROW_COUNT;
    v_deleted_count := v_deleted_count + v_temp_count;
    
    -- Delete old social media data
    DELETE FROM social_media_surveillance_data WHERE timestamp < v_cutoff_date;
    GET DIAGNOSTICS v_temp_count = ROW_COUNT;
    v_deleted_count := v_deleted_count + v_temp_count;
    
    -- Delete old environmental data
    DELETE FROM environmental_surveillance_data WHERE timestamp < v_cutoff_date;
    GET DIAGNOSTICS v_temp_count = ROW_COUNT;
    v_deleted_count := v_deleted_count + v_temp_count;
    
    -- Delete old pharmacy data
    DELETE FROM pharmacy_surveillance_data WHERE timestamp < v_cutoff_date;
    GET DIAGNOSTICS v_temp_count = ROW_COUNT;
    v_deleted_count := v_deleted_count + v_temp_count;
    
    -- Delete old anomaly detections
    DELETE FROM anomaly_detections WHERE timestamp < v_cutoff_date;
    GET DIAGNOSTICS v_temp_count = ROW_COUNT;
    v_deleted_count := v_deleted_count + v_temp_count;
    
    RETURN QUERY
    SELECT 
        v_deleted_count,
        v_cutoff_date,
        NOW()::TIMESTAMP;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION cleanup_old_data IS 'Deletes surveillance data older than specified days to keep database size manageable';

-- =============================================
-- Success Message
-- =============================================
DO $$
BEGIN
    RAISE NOTICE '';
    RAISE NOTICE '========================================';
    RAISE NOTICE '✓ All PostgreSQL Functions Created Successfully!';
    RAISE NOTICE '========================================';
    RAISE NOTICE '';
    RAISE NOTICE 'Functions created:';
    RAISE NOTICE '  1. log_surveillance_report';
    RAISE NOTICE '  2. get_surveillance_data';
    RAISE NOTICE '  3. get_anomaly_summary';
    RAISE NOTICE '  4. get_active_alerts';
    RAISE NOTICE '  5. get_prediction_history';
    RAISE NOTICE '  6. get_thinking_logs';
    RAISE NOTICE '  7. cleanup_old_data';
    RAISE NOTICE '';
    RAISE NOTICE 'Usage examples:';
    RAISE NOTICE '  SELECT * FROM get_active_alerts();';
    RAISE NOTICE '  SELECT * FROM get_anomaly_summary(7, ''Mumbai'');';
    RAISE NOTICE '  SELECT * FROM get_surveillance_data(30);';
    RAISE NOTICE '  SELECT * FROM get_thinking_logs(''SESSION-20250129-001'');';
    RAISE NOTICE '';
END $$;
