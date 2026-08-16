import os


DATA_FILE = os.getenv(
    "DATA_FILE",
    "data/sample/transactions.jsonl",
)

HIGH_VALUE_THRESHOLD = float(
    os.getenv("HIGH_VALUE_THRESHOLD", "10000")
)

RAPID_TRANSACTION_WINDOW_MINUTES = int(
    os.getenv("RAPID_TRANSACTION_WINDOW_MINUTES", "5")
)

MAX_TRANSACTIONS_IN_WINDOW = int(
    os.getenv("MAX_TRANSACTIONS_IN_WINDOW", "3")
)

SNOWFLAKE_DATABASE = os.getenv(
    "SNOWFLAKE_DATABASE",
    "FRAUD_ANALYTICS_DB",
)

SNOWFLAKE_RAW_SCHEMA = os.getenv(
    "SNOWFLAKE_RAW_SCHEMA",
    "RAW",
)

SNOWFLAKE_CURATED_SCHEMA = os.getenv(
    "SNOWFLAKE_CURATED_SCHEMA",
    "CURATED",
)
