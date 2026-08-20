-- =============================================================================
-- Trade Me Data Seekers Workshop - Load Data from Stage
-- =============================================================================
-- Prerequisites:
--   1. Run 01_create_objects.sql first to create database, schema, and tables
--   2. Upload CSV files to the internal stage using CLI or manually upload via Snowsight:
--     snow stage copy ./setup/data_generation/output/  @workshop_data_stage --no-auto-compress --database ANALYTICS --schema SANDBOX
-- =============================================================================

SET DATABASE_NAME = 'ANALYTICS';
SET SCHEMA_NAME = 'SANDBOX';

USE DATABASE IDENTIFIER($DATABASE_NAME);
USE SCHEMA IDENTIFIER($SCHEMA_NAME);

-- TRUNCATE TABLE to allow for data reload.
-- TRUNCATE TABLE MEMBERS;
-- TRUNCATE TABLE  MARKETPLACE_LISTINGS;
-- TRUNCATE TABLE  MOTORS_LISTINGS;
-- TRUNCATE TABLE  PROPERTY_LISTINGS;
-- TRUNCATE TABLE  JOBS_LISTINGS;
-- TRUNCATE TABLE  CONTACTS;
-- TRUNCATE TABLE  AD_REVENUE;
-- TRUNCATE TABLE  APPLICATIONS;

-- =============================================================================
-- MEMBERS
-- =============================================================================
COPY INTO WORKSHOP__MEMBERS (member_id, membername, first_name, last_name, business_name, member_segment, region, city, registration_date, preferences)
FROM (
    SELECT
        $1::INT,
        $2::VARCHAR,
        NULLIF($3, 'NULL')::VARCHAR,
        NULLIF($4, 'NULL')::VARCHAR,
        NULLIF($5, 'NULL')::VARCHAR,
        $6::VARCHAR,
        $7::VARCHAR,
        $8::VARCHAR,
        $9::DATE,
        PARSE_JSON($10)
    FROM @workshop_data_stage/members.csv
)
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1 NULL_IF = ('NULL', '') FIELD_DELIMITER = ',' ESCAPE_UNENCLOSED_FIELD = NONE)
ON_ERROR = 'ABORT_STATEMENT';

-- =============================================================================
-- MARKETPLACE_LISTINGS
-- =============================================================================
COPY INTO WORKSHOP__MARKETPLACE_LISTINGS (
    listing_id, member_id, category, subcategory, title,
    condition, asking_price, buy_now_price, region, city,
    status, listed_date, close_date, sold_date,
    shipping_available, accepts_offers, view_count, watchlist_count, bid_count
)
FROM (
    SELECT
        $1::INT, $2::INT, $3::VARCHAR, $4::VARCHAR, $5::VARCHAR,
        $6::VARCHAR, $7::DECIMAL(12,2), NULLIF($8, 'NULL')::DECIMAL(12,2),
        $9::VARCHAR, $10::VARCHAR,
        $11::VARCHAR, $12::TIMESTAMP_NTZ, $13::TIMESTAMP_NTZ,
        NULLIF($14, 'NULL')::TIMESTAMP_NTZ,
        $15::BOOLEAN, $16::BOOLEAN, $17::INT, $18::INT, $19::INT
    FROM @workshop_data_stage/marketplace_listings.csv
)
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1 NULL_IF = ('NULL', '') FIELD_DELIMITER = ',' ESCAPE_UNENCLOSED_FIELD = NONE)
ON_ERROR = 'ABORT_STATEMENT';

-- =============================================================================
-- MOTORS_LISTINGS
-- =============================================================================
COPY INTO WORKSHOP__MOTORS_LISTINGS (
    listing_id, member_id, vehicle_type, make, model,
    year, mileage_km, fuel_type, transmission, body_type,
    colour, engine_cc, registration_status, asking_price,
    region, city, status, listed_date, sold_date,
    view_count, watchlist_count, enquiry_count
)
FROM (
    SELECT
        $1::INT, $2::INT, $3::VARCHAR, $4::VARCHAR, $5::VARCHAR,
        $6::INT, $7::INT, $8::VARCHAR, $9::VARCHAR, $10::VARCHAR,
        $11::VARCHAR, NULLIF($12, 'NULL')::INT, $13::VARCHAR, $14::DECIMAL(12,2),
        $15::VARCHAR, $16::VARCHAR, $17::VARCHAR, $18::TIMESTAMP_NTZ,
        NULLIF($19, 'NULL')::TIMESTAMP_NTZ,
        $20::INT, $21::INT, $22::INT
    FROM @workshop_data_stage/motors_listings.csv
)
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1 NULL_IF = ('NULL', '') FIELD_DELIMITER = ',' ESCAPE_UNENCLOSED_FIELD = NONE)
ON_ERROR = 'ABORT_STATEMENT';

-- =============================================================================
-- PROPERTY_LISTINGS
-- =============================================================================
COPY INTO WORKSHOP__PROPERTY_LISTINGS (
    listing_id, member_id, listing_type, property_type,
    bedrooms, bathrooms, parking_spaces, land_area_sqm,
    floor_area_sqm, year_built, region, city, suburb,
    asking_price, price_display, status, listed_date, sold_date,
    view_count, enquiry_count, rateable_value
)
FROM (
    SELECT
        $1::INT, $2::INT, $3::VARCHAR, $4::VARCHAR,
        NULLIF($5, 'NULL')::INT, NULLIF($6, 'NULL')::INT,
        NULLIF($7, 'NULL')::INT, NULLIF($8, 'NULL')::DECIMAL(10,1),
        NULLIF($9, 'NULL')::DECIMAL(10,1), NULLIF($10, 'NULL')::INT,
        $11::VARCHAR, $12::VARCHAR, $13::VARCHAR,
        NULLIF($14, 'NULL')::DECIMAL(14,2), $15::VARCHAR, $16::VARCHAR,
        $17::TIMESTAMP_NTZ, NULLIF($18, 'NULL')::TIMESTAMP_NTZ,
        $19::INT, $20::INT, NULLIF($21, 'NULL')::VARCHAR
    FROM @workshop_data_stage/property_listings.csv
)
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1 NULL_IF = ('NULL', '') FIELD_DELIMITER = ',' ESCAPE_UNENCLOSED_FIELD = NONE)
ON_ERROR = 'ABORT_STATEMENT';

-- =============================================================================
-- JOBS_LISTINGS
-- =============================================================================
COPY INTO WORKSHOP__JOBS_LISTINGS (
    listing_id, member_id, industry, subcategory,
    role_type, employment_type, title, salary_min,
    salary_max, salary_display, region, city, status,
    listed_date, close_date, remote_option, experience_level,
    view_count, application_count
)
FROM (
    SELECT
        $1::INT, $2::INT, $3::VARCHAR, $4::VARCHAR,
        $5::VARCHAR, $6::VARCHAR, $7::VARCHAR,
        NULLIF($8, 'NULL')::DECIMAL(12,2), NULLIF($9, 'NULL')::DECIMAL(12,2),
        $10::VARCHAR, $11::VARCHAR, $12::VARCHAR, $13::VARCHAR,
        $14::TIMESTAMP_NTZ, $15::TIMESTAMP_NTZ, $16::BOOLEAN, $17::VARCHAR,
        $18::INT, $19::INT
    FROM @workshop_data_stage/jobs_listings.csv
)
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1 NULL_IF = ('NULL', '') FIELD_DELIMITER = ',' ESCAPE_UNENCLOSED_FIELD = NONE)
ON_ERROR = 'ABORT_STATEMENT';

-- =============================================================================
-- CONTACTS
-- =============================================================================
COPY INTO WORKSHOP__CONTACTS (
    contact_id, listing_id, listing_source, member_id,
    product_area, reason, created_date, resolved_date,
    resolution_time_hours, description, metadata
)
FROM (
    SELECT
        $1::INT, NULLIF($2, 'NULL')::INT, NULLIF($3, 'NULL')::VARCHAR, $4::INT,
        $5::VARCHAR, $6::VARCHAR, $7::TIMESTAMP_NTZ,
        NULLIF($8, 'NULL')::TIMESTAMP_NTZ,
        NULLIF($9, 'NULL')::DECIMAL(8,2), $10::VARCHAR, PARSE_JSON($11)
    FROM @workshop_data_stage/contacts.csv
)
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1 NULL_IF = ('NULL', '') FIELD_DELIMITER = ',' ESCAPE_UNENCLOSED_FIELD = NONE)
ON_ERROR = 'ABORT_STATEMENT';

-- =============================================================================
-- AD_REVENUE
-- =============================================================================
COPY INTO WORKSHOP__AD_REVENUE (
    ad_id, campaign_id, listing_id, listing_source,
    product_area, ad_type, impressions, clicks,
    revenue, event_date, campaign_metadata
)
FROM (
    SELECT
        $1::INT, $2::VARCHAR, $3::INT, $4::VARCHAR,
        $5::VARCHAR, $6::VARCHAR, $7::INT, $8::INT,
        $9::DECIMAL(10,2), $10::DATE, PARSE_JSON($11)
    FROM @workshop_data_stage/ad_revenue.csv
)
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1 NULL_IF = ('NULL', '') FIELD_DELIMITER = ',' ESCAPE_UNENCLOSED_FIELD = NONE)
ON_ERROR = 'ABORT_STATEMENT';

-- =============================================================================
-- APPLICATIONS
-- =============================================================================
COPY INTO WORKSHOP__APPLICATIONS (
    application_id, listing_id, member_id,
    applied_date, status, source
)
FROM (
    SELECT
        $1::INT, $2::INT, $3::INT,
        $4::TIMESTAMP_NTZ, $5::VARCHAR, $6::VARCHAR
    FROM @workshop_data_stage/applications.csv
)
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1 NULL_IF = ('NULL', '') FIELD_DELIMITER = ',' ESCAPE_UNENCLOSED_FIELD = NONE)
ON_ERROR = 'ABORT_STATEMENT';

-- =============================================================================
-- Verification queries
-- =============================================================================
SELECT 'WORKSHOP__MEMBERS' AS table_name, COUNT(*) AS row_count FROM WORKSHOP__MEMBERS
UNION ALL SELECT 'WORKSHOP__MARKETPLACE_LISTINGS', COUNT(*) FROM WORKSHOP__MARKETPLACE_LISTINGS
UNION ALL SELECT 'WORKSHOP__MOTORS_LISTINGS', COUNT(*) FROM WORKSHOP__MOTORS_LISTINGS
UNION ALL SELECT 'WORKSHOP__PROPERTY_LISTINGS', COUNT(*) FROM WORKSHOP__PROPERTY_LISTINGS
UNION ALL SELECT 'WORKSHOP__JOBS_LISTINGS', COUNT(*) FROM WORKSHOP__JOBS_LISTINGS
UNION ALL SELECT 'WORKSHOP__CONTACTS', COUNT(*) FROM WORKSHOP__CONTACTS
UNION ALL SELECT 'WORKSHOP__AD_REVENUE', COUNT(*) FROM WORKSHOP__AD_REVENUE
UNION ALL SELECT 'WORKSHOP__APPLICATIONS', COUNT(*) FROM WORKSHOP__APPLICATIONS
ORDER BY table_name;

