from typing import Any


REQUIRED_FIELDS = {
    "transaction_id",
    "customer_id",
    "merchant_id",
    "transaction_timestamp",
    "amount",
    "currency",
    "transaction_type",
    "payment_method",
    "city",
    "status",
}


VALID_TRANSACTION_TYPES = {
    "PURCHASE",
    "REFUND",
    "WITHDRAWAL",
}


VALID_PAYMENT_METHODS = {
    "CARD",
    "UPI",
    "BANK_TRANSFER",
}


VALID_STATUSES = {
    "SUCCESS",
    "FAILED",
}


def validate_transaction(
    transaction: dict[str, Any],
) -> list[str]:
    """
    Validate a single financial transaction.

    Returns a list of validation errors.
    An empty list means the transaction is valid.
    """

    errors: list[str] = []

    missing_fields = REQUIRED_FIELDS - transaction.keys()

    if missing_fields:
        errors.append(
            f"Missing required fields: {sorted(missing_fields)}"
        )

    if not transaction.get("transaction_id"):
        errors.append(
            "transaction_id must not be empty"
        )

    if not transaction.get("customer_id"):
        errors.append(
            "customer_id must not be empty"
        )

    if not transaction.get("merchant_id"):
        errors.append(
            "merchant_id must not be empty"
        )

    try:
        amount = float(transaction["amount"])

        if amount <= 0:
            errors.append(
                "amount must be greater than 0"
            )

    except (KeyError, TypeError, ValueError):
        errors.append(
            "amount must be numeric"
        )

    if transaction.get("transaction_type") not in VALID_TRANSACTION_TYPES:
        errors.append(
            "invalid transaction_type"
        )

    if transaction.get("payment_method") not in VALID_PAYMENT_METHODS:
        errors.append(
            "invalid payment_method"
        )

    if transaction.get("status") not in VALID_STATUSES:
        errors.append(
            "invalid status"
        )

    if not transaction.get("currency"):
        errors.append(
            "currency must not be empty"
        )

    if not transaction.get("city"):
        errors.append(
            "city must not be empty"
        )

    if not transaction.get("transaction_timestamp"):
        errors.append(
            "transaction_timestamp must not be empty"
        )

    return errors


def validate_transactions(
    transactions: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    """
    Separate valid and invalid transactions.
    """

    valid_transactions: list[dict[str, Any]] = []

    invalid_transactions: list[dict[str, Any]] = []

    seen_transaction_ids: set[str] = set()

    for transaction in transactions:

        errors = validate_transaction(transaction)

        transaction_id = transaction.get(
            "transaction_id"
        )

        if transaction_id in seen_transaction_ids:
            errors.append(
                "duplicate transaction_id"
            )

        seen_transaction_ids.add(transaction_id)

        if errors:
            invalid_transactions.append(
                {
                    "transaction": transaction,
                    "errors": errors,
                }
            )
        else:
            valid_transactions.append(transaction)

    return (
        valid_transactions,
        invalid_transactions,
    )
