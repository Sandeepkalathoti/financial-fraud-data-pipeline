from datetime import datetime
from typing import Any


def transform_transactions(
    transactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Clean and standardize financial transaction records.
    """

    transformed: list[dict[str, Any]] = []

    for transaction in transactions:
        record = {
            "transaction_id": str(
                transaction["transaction_id"]
            ).strip(),

            "customer_id": str(
                transaction["customer_id"]
            ).strip(),

            "merchant_id": str(
                transaction["merchant_id"]
            ).strip(),

            "transaction_timestamp": datetime.fromisoformat(
                transaction["transaction_timestamp"].replace(
                    "Z", "+00:00"
                )
            ),

            "amount": float(transaction["amount"]),

            "currency": str(
                transaction["currency"]
            ).upper().strip(),

            "transaction_type": str(
                transaction["transaction_type"]
            ).upper().strip(),

            "payment_method": str(
                transaction["payment_method"]
            ).upper().strip(),

            "city": str(
                transaction["city"]
            ).strip(),

            "status": str(
                transaction["status"]
            ).upper().strip(),
        }

        transformed.append(record)

    return transformed
