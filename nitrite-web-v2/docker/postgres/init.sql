-- Initialize PostgreSQL database
CREATE DATABASE IF NOT EXISTS nitrite;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- For text search

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE nitrite TO nitrite;

-- Add any initial SQL scripts here
