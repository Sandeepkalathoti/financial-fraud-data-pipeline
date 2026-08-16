# Financial Fraud Data Pipeline Architecture

## Overview

This project implements a financial transaction monitoring and fraud analytics pipeline.

The pipeline ingests transaction events, stores raw data in a data lake, processes and validates the transactions, applies fraud detection rules, loads the processed data into Snowflake, and prepares analytical models for reporting.

## Architecture

```text
                    Transaction Events
                           |
                           v
                     AWS Kinesis
                    Streaming Layer
                           |
                           v
                        AWS S3
                      Data Lake
                           |
                           v
                    AWS Glue / PySpark
                   ETL Processing Layer
                           |
              +------------+------------+
              |                         |
              v                         v
       Data Quality Checks        Fraud Detection
              |                         |
              +------------+------------+
                           |
                           v
                       Snowflake
                    Data Warehouse
                           |
                           v
                          dbt
                 Analytical Data Models
                           |
                           v
                       Power BI
                    Fraud Analytics
