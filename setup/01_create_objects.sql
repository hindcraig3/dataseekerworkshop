-- =============================================================================
-- Trade Me Data Seekers Workshop - Database Setup
-- =============================================================================
-- Usage: Set the DATABASE_NAME variable below, then execute this entire script.
-- =============================================================================

SET DATABASE_NAME = 'TM_WORKSHOP';

-- Create database and schema
CREATE DATABASE IF NOT EXISTS IDENTIFIER($DATABASE_NAME);
USE DATABASE IDENTIFIER($DATABASE_NAME);

CREATE SCHEMA IF NOT EXISTS IDENTIFIER($DATABASE_NAME).SAMPLEDATA;
USE SCHEMA SAMPLEDATA;

-- File format for CSV loading
CREATE OR REPLACE FILE FORMAT csv_format
    TYPE = 'CSV'
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    SKIP_HEADER = 1
    NULL_IF = ('NULL', '')
    FIELD_DELIMITER = ','
    ESCAPE_UNENCLOSED_FIELD = NONE;

-- Internal stage for data files
CREATE OR REPLACE STAGE workshop_data_stage
    FILE_FORMAT = csv_format;

-- =============================================================================
-- USERS
-- =============================================================================
CREATE OR REPLACE TABLE USERS (
    user_id             INT             NOT NULL,
    username            VARCHAR(200)    NOT NULL    COMMENT 'Login username - email or handle',
    first_name          VARCHAR(100)               COMMENT 'First name (Individual users only)',
    last_name           VARCHAR(100)               COMMENT 'Last name (Individual users only)',
    business_name       VARCHAR(200)               COMMENT 'Business name (Business/Power Seller only)',
    user_segment        VARCHAR(50)     NOT NULL    COMMENT 'Individual, Business, or Power Seller',
    region              VARCHAR(100)    NOT NULL    COMMENT 'NZ region',
    city                VARCHAR(100)    NOT NULL,
    registration_date   DATE            NOT NULL,
    preferences         VARIANT                    COMMENT 'JSON: notification prefs, interests, saved searches'
)
COMMENT = 'Trade Me registered users (anonymised for workshop)';

-- =============================================================================
-- MARKETPLACE_LISTINGS
-- =============================================================================
CREATE OR REPLACE TABLE MARKETPLACE_LISTINGS (
    listing_id          INT             NOT NULL,
    user_id             INT             NOT NULL    COMMENT 'FK to USERS',
    category            VARCHAR(100)    NOT NULL    COMMENT 'Top-level category',
    subcategory         VARCHAR(100)    NOT NULL,
    title               VARCHAR(500)    NOT NULL,
    condition           VARCHAR(50)     NOT NULL    COMMENT 'New, Used - Like New, Used - Good, Used - Average',
    asking_price        DECIMAL(12,2)              COMMENT 'Starting/asking price NZD',
    buy_now_price       DECIMAL(12,2)              COMMENT 'Buy Now price NZD, nullable',
    region              VARCHAR(100)    NOT NULL,
    city                VARCHAR(100)    NOT NULL,
    status              VARCHAR(50)     NOT NULL    COMMENT 'active, sold, closed, withdrawn',
    listed_date         TIMESTAMP_NTZ   NOT NULL,
    close_date          TIMESTAMP_NTZ              COMMENT 'Auction close or expiry',
    sold_date           TIMESTAMP_NTZ,
    shipping_available  BOOLEAN         NOT NULL,
    accepts_offers      BOOLEAN         NOT NULL,
    view_count          INT             NOT NULL    DEFAULT 0,
    watchlist_count     INT             NOT NULL    DEFAULT 0,
    bid_count           INT             NOT NULL    DEFAULT 0
)
COMMENT = 'General marketplace listings: buy/sell consumer goods';

-- =============================================================================
-- MOTORS_LISTINGS
-- =============================================================================
CREATE OR REPLACE TABLE MOTORS_LISTINGS (
    listing_id          INT             NOT NULL,
    user_id             INT             NOT NULL    COMMENT 'FK to USERS',
    vehicle_type        VARCHAR(50)     NOT NULL    COMMENT 'Car, SUV, Ute, Van, Motorcycle, Boat, Motorhome',
    make                VARCHAR(100)    NOT NULL,
    model               VARCHAR(100)    NOT NULL,
    year                INT             NOT NULL,
    mileage_km          INT                        COMMENT 'Odometer reading',
    fuel_type           VARCHAR(50)     NOT NULL    COMMENT 'Petrol, Diesel, Electric, Hybrid, LPG',
    transmission        VARCHAR(50)     NOT NULL    COMMENT 'Manual, Automatic, CVT',
    body_type           VARCHAR(50)     NOT NULL    COMMENT 'Sedan, Hatchback, Wagon, SUV, Coupe, Convertible, Ute',
    colour              VARCHAR(50),
    engine_cc           INT                        COMMENT 'Engine displacement in cc',
    registration_status VARCHAR(100)    NOT NULL    COMMENT 'Registered, On Hold, Expired, Imported',
    asking_price        DECIMAL(12,2)   NOT NULL,
    region              VARCHAR(100)    NOT NULL,
    city                VARCHAR(100)    NOT NULL,
    status              VARCHAR(50)     NOT NULL    COMMENT 'active, sold, expired, withdrawn',
    listed_date         TIMESTAMP_NTZ   NOT NULL,
    sold_date           TIMESTAMP_NTZ,
    view_count          INT             NOT NULL    DEFAULT 0,
    watchlist_count     INT             NOT NULL    DEFAULT 0,
    enquiry_count       INT             NOT NULL    DEFAULT 0
)
COMMENT = 'Vehicle listings: cars, motorcycles, boats, motorhomes';

-- =============================================================================
-- PROPERTY_LISTINGS
-- =============================================================================
CREATE OR REPLACE TABLE PROPERTY_LISTINGS (
    listing_id          INT             NOT NULL,
    user_id             INT             NOT NULL    COMMENT 'FK to USERS - typically agent (Business)',
    listing_type        VARCHAR(50)     NOT NULL    COMMENT 'Sale, Rent, Auction, Tender, Deadline Sale',
    property_type       VARCHAR(50)     NOT NULL    COMMENT 'House, Apartment, Townhouse, Section, Lifestyle, Rural, Unit',
    bedrooms            INT,
    bathrooms           INT,
    parking_spaces      INT,
    land_area_sqm       DECIMAL(10,1),
    floor_area_sqm      DECIMAL(10,1),
    year_built          INT,
    region              VARCHAR(100)    NOT NULL,
    city                VARCHAR(100)    NOT NULL,
    suburb              VARCHAR(100),
    asking_price        DECIMAL(14,2)              COMMENT 'Nullable for By Negotiation / Tender',
    price_display       VARCHAR(100)    NOT NULL    COMMENT 'Display string: $1,200,000 or By Negotiation',
    status              VARCHAR(50)     NOT NULL    COMMENT 'active, sold, under_offer, withdrawn, expired',
    listed_date         TIMESTAMP_NTZ   NOT NULL,
    sold_date           TIMESTAMP_NTZ,
    view_count          INT             NOT NULL    DEFAULT 0,
    enquiry_count       INT             NOT NULL    DEFAULT 0,
    rateable_value      VARCHAR(50)                COMMENT 'Council RV e.g. $980,000'
)
COMMENT = 'Property listings: residential and commercial sale/rent';

-- =============================================================================
-- JOBS_LISTINGS
-- =============================================================================
CREATE OR REPLACE TABLE JOBS_LISTINGS (
    listing_id          INT             NOT NULL,
    user_id             INT             NOT NULL    COMMENT 'FK to USERS - employer or recruiter',
    industry            VARCHAR(100)    NOT NULL,
    subcategory         VARCHAR(100)    NOT NULL    COMMENT 'Role subcategory e.g. Management Accountants',
    role_type           VARCHAR(50)     NOT NULL    COMMENT 'Permanent, Contract, Temporary',
    employment_type     VARCHAR(50)     NOT NULL    COMMENT 'Full Time, Part Time, Casual',
    title               VARCHAR(500)    NOT NULL    COMMENT 'Job title as listed',
    salary_min          DECIMAL(12,2)              COMMENT 'Nullable if Negotiable',
    salary_max          DECIMAL(12,2),
    salary_display      VARCHAR(100)    NOT NULL    COMMENT '$80k-$100k, Negotiable, $45/hour',
    region              VARCHAR(100)    NOT NULL,
    city                VARCHAR(100)    NOT NULL,
    status              VARCHAR(50)     NOT NULL    COMMENT 'active, closed, filled, expired',
    listed_date         TIMESTAMP_NTZ   NOT NULL,
    close_date          TIMESTAMP_NTZ              COMMENT 'Application deadline',
    remote_option       BOOLEAN         NOT NULL,
    experience_level    VARCHAR(50)     NOT NULL    COMMENT 'Entry, Mid, Senior, Executive',
    view_count          INT             NOT NULL    DEFAULT 0,
    application_count   INT             NOT NULL    DEFAULT 0
)
COMMENT = 'Job listings across all industries';

-- =============================================================================
-- CONTACTS
-- =============================================================================
CREATE OR REPLACE TABLE CONTACTS (
    contact_id              INT             NOT NULL,
    listing_id              INT                        COMMENT 'FK to one of the 4 listing tables',
    listing_source          VARCHAR(50)                COMMENT 'marketplace, motors, property, jobs',
    user_id                 INT             NOT NULL   COMMENT 'FK to USERS - person who raised contact',
    product_area            VARCHAR(50)     NOT NULL   COMMENT 'Marketplace, Motors, Property, Jobs',
    reason                  VARCHAR(100)    NOT NULL   COMMENT 'Billing, Fraud, Technical, Listing Quality, Delivery, Account',
    created_date            TIMESTAMP_NTZ   NOT NULL,
    resolved_date           TIMESTAMP_NTZ,
    resolution_time_hours   DECIMAL(8,2),
    description             VARCHAR(1000),
    metadata                VARIANT                    COMMENT 'JSON: channel, priority, agent_id, tags, escalated'
)
COMMENT = 'Customer support contacts linked to listings';

-- =============================================================================
-- AD_REVENUE
-- =============================================================================
CREATE OR REPLACE TABLE AD_REVENUE (
    ad_id               INT             NOT NULL,
    campaign_id         VARCHAR(50)     NOT NULL,
    listing_id          INT                        COMMENT 'FK to one of the 4 listing tables',
    listing_source      VARCHAR(50)                COMMENT 'marketplace, motors, property, jobs',
    product_area        VARCHAR(50)     NOT NULL,
    ad_type             VARCHAR(50)     NOT NULL   COMMENT 'Featured, Highlight, Gallery, Banner, Sponsored',
    impressions         INT             NOT NULL,
    clicks              INT             NOT NULL,
    revenue             DECIMAL(10,2)   NOT NULL   COMMENT 'Revenue in NZD',
    event_date          DATE            NOT NULL,
    campaign_metadata   VARIANT                    COMMENT 'JSON: advertiser_name, budget, target_audience, duration_days'
)
COMMENT = 'Daily advertising revenue events across all product areas';

-- =============================================================================
-- APPLICATIONS
-- =============================================================================
CREATE OR REPLACE TABLE APPLICATIONS (
    application_id      INT             NOT NULL,
    listing_id          INT             NOT NULL   COMMENT 'FK to JOBS_LISTINGS',
    user_id             INT             NOT NULL   COMMENT 'FK to USERS - applicant',
    applied_date        TIMESTAMP_NTZ   NOT NULL,
    status              VARCHAR(50)     NOT NULL   COMMENT 'submitted, viewed, shortlisted, rejected',
    source              VARCHAR(50)     NOT NULL   COMMENT 'Trade Me, Direct, Referral'
)
COMMENT = 'Job applications submitted against Jobs listings';


)
COMMENT = 'Job applications submitted against Jobs listings';

-- ============================================================
-- ROLE SETUP
-- ============================================================

-- Create the TMWORKSHOP role
USE SECURITYADMIN;
CREATE ROLE IF NOT EXISTS TMWORKSHOP
    COMMENT = 'Role for Trade Me Workshop users';

-- Grant privileges on the DATABASE
GRANT USAGE ON DATABASE TMWORKSHOP_DB TO ROLE TMWORKSHOP;

-- Grant privileges on the SCHEMA
GRANT USAGE ON SCHEMA TMWORKSHOP_DB.PUBLIC TO ROLE TMWORKSHOP;

-- Grant privileges on all TABLES in the schema
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA TMWORKSHOP_DB.PUBLIC TO ROLE TMWORKSHOP;

-- Ensure future tables also receive the grants
GRANT SELECT, INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA TMWORKSHOP_DB.PUBLIC TO ROLE TMWORKSHOP;

-- Grant the TMWORKSHOP role to SYSADMIN
GRANT ROLE TMWORKSHOP TO ROLE SYSADMIN;