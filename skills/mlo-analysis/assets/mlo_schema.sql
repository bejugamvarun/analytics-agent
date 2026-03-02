-- MLO Data Schema Reference
-- This SQL schema describes the key tables for MLO analysis

-- Main MLO fact table
CREATE OR REPLACE TABLE liquidity.mlo_daily (
    report_date DATE NOT NULL,
    cusip VARCHAR(9) NOT NULL,
    entity_id VARCHAR(20) NOT NULL,
    flb_code VARCHAR(10) NOT NULL,
    product_type VARCHAR(50),
    geography VARCHAR(3),
    
    -- Core MLO metrics
    mlo_amount DECIMAL(18, 2),
    stress_scenario VARCHAR(20),
    confidence_level DECIMAL(5, 4),
    
    -- Metadata
    load_timestamp TIMESTAMP_NTZ,
    source_system VARCHAR(50),
    data_quality_flag VARCHAR(1),
    
    PRIMARY KEY (report_date, cusip, entity_id, stress_scenario)
);

-- Hierarchy dimension
CREATE OR REPLACE TABLE liquidity.hierarchy_dim (
    cusip VARCHAR(9) PRIMARY KEY,
    security_name VARCHAR(200),
    flb_code VARCHAR(10),
    flb_name VARCHAR(100),
    entity_id VARCHAR(20),
    entity_name VARCHAR(100),
    product_type VARCHAR(50),
    asset_class VARCHAR(50)
);

-- Typical variance query pattern
-- SELECT 
--     h.entity_name,
--     h.flb_name,
--     curr.cusip,
--     h.security_name,
--     prior.mlo_amount as prior_mlo,
--     curr.mlo_amount as current_mlo,
--     (curr.mlo_amount - prior.mlo_amount) as variance,
--     ((curr.mlo_amount - prior.mlo_amount) / NULLIF(prior.mlo_amount, 0)) * 100 as variance_pct
-- FROM liquidity.mlo_daily curr
-- JOIN liquidity.mlo_daily prior 
--     ON curr.cusip = prior.cusip 
--     AND curr.entity_id = prior.entity_id
--     AND curr.stress_scenario = prior.stress_scenario
-- JOIN liquidity.hierarchy_dim h ON curr.cusip = h.cusip
-- WHERE curr.report_date = :current_date
--     AND prior.report_date = :prior_date
--     AND curr.stress_scenario = 'BASELINE'
-- ORDER BY ABS(variance) DESC
-- LIMIT 50;
