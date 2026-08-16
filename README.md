# Financial Fraud Data Pipeline

An end-to-end data engineering project for processing financial transaction data, applying fraud detection rules, and preparing analytical datasets for fraud monitoring.

## Project Overview

This project demonstrates a production-style financial transaction pipeline.

The pipeline:

1. Ingests transaction events from JSONL data.
2. Validates transaction records.
3. Cleans and transforms the data using Python.
4. Applies rule-based fraud detection.
5. Assigns risk scores and risk levels.
6. Prepares processed data for Snowflake.
7. Uses Apache Airflow for workflow orchestration.
8. Uses Snowflake for analytical storage.
9. Uses automated tests for data quality and fraud rules.
10. Uses GitHub Actions for continuous integration.

## Architecture

```text
Transaction Events
        |
        v
    AWS Kinesis
        |
        v
     Amazon S3
        |
        v
 AWS Glue / PySpark
        |
        +----------------+
        |                |
        v                v
 Data Quality      Fraud Detection
        |                |
        +-------+--------+
                |
                v
            Snowflake
                |
                v
               dbt
                |
                v
            Power BI

##Current Local Pipeline

The repository currently implements the core processing and fraud detection logic locally using Python and JSONL sample data.
JSONL Transaction Data
        |
        v
      Ingest
        |
        v
     Transform
        |
        v
   Quality Checks
        |
        v
  Fraud Detection
        |
        v
Prepare for Snowflake

#Technology Stack

| Technology     | Purpose                         |
| -------------- | ------------------------------- |
| Python         | ETL and fraud detection logic   |
| AWS Kinesis    | Streaming transaction ingestion |
| Amazon S3      | Data lake storage               |
| AWS Glue       | ETL processing                  |
| PySpark        | Distributed processing          |
| Snowflake      | Data warehouse                  |
| dbt            | Analytical transformations      |
| Apache Airflow | Workflow orchestration          |
| SQL            | Data modeling and analytics     |
| Pytest         | Automated testing               |
| Docker         | Local development               |
| GitHub Actions | CI/CD                           |
| Power BI       | Fraud analytics dashboard       |

#Repository Structure

financial-fraud-data-pipeline/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── dags/
│   └── fraud_pipeline_dag.py
│
├── data/
│   └── sample/
│       └── transactions.jsonl
│
├── docs/
│   └── architecture.md
│
├── src/
│   └── fraud_pipeline/
│       ├── config.py
│       ├── fraud_rules.py
│       ├── ingest.py
│       ├── load.py
│       ├── quality.py
│       └── transform.py
│
├── snowflake/
│   ├── 001_database.sql
│   ├── 002_raw_tables.sql
│   ├── 003_dimensions.sql
│   ├── 004_fact_transactions.sql
│   └── 005_fraud_analytics.sql
│
├── tests/
│   ├── test_fraud_rules.py
│   └── test_quality.py
│
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
├── .env.example
└── .gitignore

#ETL Workflow
1. Ingestion
Transaction records are read from JSONL input data.
The ingestion layer:
Reads transaction records.
Parses JSON objects.
Validates the JSON structure.
Returns transactions as Python dictionaries.

2. Transformation
The transformation layer standardizes the raw transaction data.
Transformations include:
Trimming identifiers.
Standardizing uppercase fields.
Converting transaction amounts to numeric values.
Converting timestamps into timezone-aware datetime values.
Standardizing currency and transaction attributes.

3. Data Quality
The quality layer validates:
Required transaction fields.
Transaction ID.
Customer ID.
Merchant ID.
Transaction amount.
Transaction type.
Payment method.
Transaction status.
Duplicate transaction IDs.
Invalid transactions are separated from valid transactions.

4. Fraud Detection
The fraud detection layer applies rule-based scoring.
Current rules include:
High-value transaction
Transactions greater than or equal to the configured threshold receive additional risk points.
Default threshold:
10000 INR
Rapid transactions
Multiple transactions from the same customer within a short time window are flagged.
Default window:
5 minutes
Multiple failed transactions
Repeated failed transactions from the same customer within a short period increase the risk score.
Risk Levels
0 - 39     LOW
40 - 69    MEDIUM
70+        HIGH

A transaction with a score of 70 or more is marked as suspicious.

##Sample Fraud Scenarios
The sample dataset contains transactions designed to demonstrate fraud detection scenarios.
Examples include:
High-value transactions.
Repeated failed transactions.
Multiple transactions within a short period.
High-value transactions occurring close together.

##Snowflake Data Model
Database
FRAUD_ANALYTICS_DB

Schemas
RAW
CURATED

Raw Table
TRANSACTIONS_RAW

Dimension Tables
DIM_CUSTOMER
DIM_MERCHANT

Fact Table
FACT_TRANSACTIONS

Analytics Views
DAILY_FRAUD_SUMMARY
CUSTOMER_FRAUD_SUMMARY
MERCHANT_FRAUD_SUMMARY
REGIONAL_FRAUD_SUMMARY
HIGH_RISK_TRANSACTIONS

##Airflow Pipeline
The Airflow DAG orchestrates the processing flow:

Extract
   |
   v
Transform
   |
   v
Quality Check
   |
   v
Fraud Detection
   |
   v
Load Preparation

DAG ID:
financial_fraud_pipeline
Testing

The project uses Pytest for automated testing.

##Tests cover:
High-value transaction detection.
Normal transaction detection.
Rapid transaction detection.
Multiple failed transaction detection.
Risk score calculation.
Fraud risk classification.
Transaction validation.
Invalid transaction amounts.
Invalid transaction types.
Invalid payment methods.
Invalid statuses.
Duplicate transaction detection.

##Run tests locally:
pytest
Docker

The project includes Docker Compose configuration for local Airflow development.
Start the environment:
docker compose up -d

Airflow UI:
http://localhost:8080

Environment Configuration
Create a local .env file using .env.example as a template.
Do not commit real credentials or secrets to GitHub.

Example:
AWS_REGION=ap-south-1
S3_BUCKET=your-s3-bucket
KINESIS_STREAM=financial-transactions

SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
CI/CD

##GitHub Actions runs the automated test suite when code is pushed to the main branch or when a pull request is created.

Workflow:
Git Push / Pull Request
          |
          v
    Checkout Code
          |
          v
    Setup Python
          |
          v
 Install Project
          |
          v
       Run Pytest

##Future Enhancements
Integrate real AWS Kinesis streaming.
Store raw transaction events in Amazon S3.
Add AWS Glue PySpark processing.
Implement actual Snowflake loading.
Add dbt models.
Add incremental processing.
Add real-time fraud monitoring.
Add fraud alert notifications.
Add Power BI dashboard.
Add Terraform infrastructure.
Add advanced machine-learning fraud detection.
Add monitoring and observability.

##Project Goal

The goal of this project is to demonstrate practical data engineering skills across data ingestion, data quality, transformation, fraud detection, data warehousing, orchestration, testing, cloud services, and CI/CD.
