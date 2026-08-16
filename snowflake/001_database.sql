-- Create database for financial fraud analytics

CREATE DATABASE IF NOT EXISTS FRAUD_ANALYTICS_DB;

-- Use the database

USE DATABASE FRAUD_ANALYTICS_DB;

-- Raw transaction schema

CREATE SCHEMA IF NOT EXISTS RAW;

-- Curated analytical schema

CREATE SCHEMA IF NOT EXISTS CURATED;
