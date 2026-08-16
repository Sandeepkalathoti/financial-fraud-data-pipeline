from typing import Any


def prepare_for_snowflake(
    transactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Prepare fraud-scored transactions for Snowflake loading.
    """

    load_records: list[dict[str, Any]] = []

    for transaction in transactions:
        load_records.append(
            {
                "transaction_id": transaction["transaction_id"],
                "customer_id": transaction["customer_id"],
                "merchant_id": transaction["merchant_id"],
                "transaction_timestamp": transaction[
                    "transaction_timestamp"
                ],
                "amount": transaction["amount"],
                "currency": transaction["currency"],
                "transaction_type": transaction[
                    "transaction_type"
                ],
                "payment_method": transaction[
                    "payment_method"
                ],
                "city": transaction["city"],
                "status": transaction["status"],
                "risk_score": transaction["risk_score"],
                "risk_level": transaction["risk_level"],
                "fraud_reasons": ",".join(
                    transaction["fraud_reasons"]
                ),
                "is_suspicious": transaction[
                    "is_suspicious"
                ],
            }
        )

    return load_records
