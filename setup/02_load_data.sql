-- =============================================================================
-- Trade Me Data Seekers Workshop - Load Data from Stage
-- =============================================================================
-- Prerequisites:
--   1. Run 01_create_objects.sql first to create database, schema, and tables
--   2. Upload CSV files to the internal stage:
--     snow stage copy ./setup/data_generation/output/  @workshop_data_stage --no-auto-compress --database TM_WORKSHOP --schema SAMPLEDATA
-- =============================================================================

SET DATABASE_NAME = 'TM_WORKSHOP';

USE DATABASE IDENTIFIER($DATABASE_NAME);
USE SCHEMA SAMPLEDATA;

-- TRUNCATE TABLE to allwo for data reload.
-- TRUNCATE TABLE USERS;
-- TRUNCATE TABLE  MARKETPLACE_LISTINGS;
-- TRUNCATE TABLE  MOTORS_LISTINGS;
-- TRUNCATE TABLE  PROPERTY_LISTINGS;
-- TRUNCATE TABLE  JOBS_LISTINGS;
-- TRUNCATE TABLE  CONTACTS;
-- TRUNCATE TABLE  AD_REVENUE;
-- TRUNCATE TABLE  APPLICATIONS;
-- =============================================================================
-- USERS
-- =============================================================================
COPY INTO USERS (user_id, username, first_name, last_name, business_name, user_segment, region, city, registration_date, preferences)
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
    FROM @workshop_data_stage/users.csv
)
FILE_FORMAT = csv_format
ON_ERROR = 'ABORT_STATEMENT';

-- =============================================================================
-- MARKETPLACE_LISTINGS
-- =============================================================================
COPY INTO MARKETPLACE_LISTINGS (
    listing_id, user_id, category, subcategory, title,
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
FILE_FORMAT = csv_format
ON_ERROR = 'ABORT_STATEMENT';

-- =============================================================================
-- MOTORS_LISTINGS
-- =============================================================================
COPY INTO MOTORS_LISTINGS (
    listing_id, user_id, vehicle_type, make, model,
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
FILE_FORMAT = csv_format
ON_ERROR = 'ABORT_STATEMENT';

-- =============================================================================
-- PROPERTY_LISTINGS
-- =============================================================================
COPY INTO PROPERTY_LISTINGS (
    listing_id, user_id, listing_type, property_type,
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
FILE_FORMAT = csv_format
ON_ERROR = 'ABORT_STATEMENT';

-- =============================================================================
-- JOBS_LISTINGS
-- =============================================================================
COPY INTO JOBS_LISTINGS (
    listing_id, user_id, industry, subcategory,
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
FILE_FORMAT = csv_format
ON_ERROR = 'ABORT_STATEMENT';

-- =============================================================================
-- CONTACTS
-- =============================================================================
COPY INTO CONTACTS (
    contact_id, listing_id, listing_source, user_id,
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
FILE_FORMAT = csv_format
ON_ERROR = 'ABORT_STATEMENT';

-- =============================================================================
-- AD_REVENUE
-- =============================================================================
COPY INTO AD_REVENUE (
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
FILE_FORMAT = csv_format
ON_ERROR = 'ABORT_STATEMENT';

-- =============================================================================
-- APPLICATIONS
-- =============================================================================
COPY INTO APPLICATIONS (
    application_id, listing_id, user_id,
    applied_date, status, source
)
FROM (
    SELECT
        $1::INT, $2::INT, $3::INT,
        $4::TIMESTAMP_NTZ, $5::VARCHAR, $6::VARCHAR
    FROM @workshop_data_stage/applications.csv
)
FILE_FORMAT = csv_format
ON_ERROR = 'ABORT_STATEMENT';

-- =============================================================================
-- Verification queries
-- =============================================================================
SELECT 'USERS' AS table_name, COUNT(*) AS row_count FROM USERS
UNION ALL SELECT 'MARKETPLACE_LISTINGS', COUNT(*) FROM MARKETPLACE_LISTINGS
UNION ALL SELECT 'MOTORS_LISTINGS', COUNT(*) FROM MOTORS_LISTINGS
UNION ALL SELECT 'PROPERTY_LISTINGS', COUNT(*) FROM PROPERTY_LISTINGS
UNION ALL SELECT 'JOBS_LISTINGS', COUNT(*) FROM JOBS_LISTINGS
UNION ALL SELECT 'CONTACTS', COUNT(*) FROM CONTACTS
UNION ALL SELECT 'AD_REVENUE', COUNT(*) FROM AD_REVENUE
UNION ALL SELECT 'APPLICATIONS', COUNT(*) FROM APPLICATIONS
ORDER BY table_name;
