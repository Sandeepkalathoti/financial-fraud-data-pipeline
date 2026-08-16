from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from fraud_pipeline.fraud_rules import apply_fraud_rules
from fraud_pipeline.ingest import load_transactions
from fraud_pipeline.load import prepare_for_snowflake
from fraud_pipeline.quality import validate_transactions
from fraud_pipeline.transform import transform_transactions


def extract_task():
    transactions = load_transactions()

    print(f"Extracted {len(transactions)} transactions")

    return transactions


def transform_task(**context):
    transactions = context["ti"].xcom_pull(
        task_ids="extract_transactions"
    )

    transformed = transform_transactions(
        transactions
    )

    print(
        f"Transformed {len(transformed)} transactions"
    )

    return transformed


def quality_task(**context):
    transactions = context["ti"].xcom_pull(
        task_ids="transform_transactions"
    )

    valid_transactions, invalid_transactions = (
        validate_transactions(transactions)
    )

    print(
        f"Valid transactions: {len(valid_transactions)}"
    )

    print(
        f"Invalid transactions: {len(invalid_transactions)}"
    )

    if invalid_transactions:
        for record in invalid_transactions:
            print(record)

    return valid_transactions


def fraud_detection_task(**context):
    transactions = context["ti"].xcom_pull(
        task_ids="quality_check"
    )

    fraud_scored = apply_fraud_rules(
        transactions
    )

    high_risk_count = sum(
        1
        for transaction in fraud_scored
        if transaction["is_suspicious"]
    )

    print(
        f"High-risk transactions: {high_risk_count}"
    )

    return fraud_scored


def load_task(**context):
    transactions = context["ti"].xcom_pull(
        task_ids="fraud_detection"
    )

    records = prepare_for_snowflake(
        transactions
    )

    print(
        f"Prepared {len(records)} records for Snowflake"
    )

    return records


default_args = {
    "owner": "data-engineering",
    "retries": 2,
}


with DAG(
    dag_id="financial_fraud_pipeline",
    default_args=default_args,
    description="Financial transaction fraud detection pipeline",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=[
        "fraud",
        "financial",
        "data-engineering",
    ],
) as dag:

    extract_transactions = PythonOperator(
        task_id="extract_transactions",
        python_callable=extract_task,
    )

    transform_transactions_task = PythonOperator(
        task_id="transform_transactions",
        python_callable=transform_task,
    )

    quality_check = PythonOperator(
        task_id="quality_check",
        python_callable=quality_task,
    )

    fraud_detection = PythonOperator(
        task_id="fraud_detection",
        python_callable=fraud_detection_task,
    )

    load_to_snowflake = PythonOperator(
        task_id="load_to_snowflake",
        python_callable=load_task,
    )

    (
        extract_transactions
        >> transform_transactions_task
        >> quality_check
        >> fraud_detection
        >> load_to_snowflake
    )
