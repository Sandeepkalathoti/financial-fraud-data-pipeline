from datetime import datetime, timezone

from fraud_pipeline.quality import (
    validate_transaction,
    validate_transactions,
)


def valid_transaction():
    return {
        "transaction_id": "TXN1001",
        "customer_id": "CUST001",
        "merchant_id": "MERCH001",
        "transaction_timestamp": datetime(
            2026,
            8,
            16,
            10,
            0,
            tzinfo=timezone.utc,
        ),
        "amount": 500.0,
        "currency": "INR",
        "transaction_type": "PURCHASE",
        "payment_method": "CARD",
        "city": "Hyderabad",
        "status": "SUCCESS",
    }


def test_valid_transaction():
    transaction = valid_transaction()

    errors = validate_transaction(transaction)

    assert errors == []


def test_negative_amount():
    transaction = valid_transaction()
    transaction["amount"] = -100

    errors = validate_transaction(transaction)

    assert "amount must be greater than 0" in errors


def test_invalid_transaction_type():
    transaction = valid_transaction()
    transaction["transaction_type"] = "INVALID"

    errors = validate_transaction(transaction)

    assert "invalid transaction_type" in errors


def test_invalid_payment_method():
    transaction = valid_transaction()
    transaction["payment_method"] = "CASH"

    errors = validate_transaction(transaction)

    assert "invalid payment_method" in errors


def test_invalid_status():
    transaction = valid_transaction()
    transaction["status"] = "UNKNOWN"

    errors = validate_transaction(transaction)

    assert "invalid status" in errors


def test_missing_customer_id():
    transaction = valid_transaction()
    transaction["customer_id"] = ""

    errors = validate_transaction(transaction)

    assert "customer_id must not be empty" in errors


def test_duplicate_transactions():
    transaction_1 = valid_transaction()
    transaction_2 = valid_transaction()

    valid_records, invalid_records = validate_transactions(
        [transaction_1, transaction_2]
    )

    assert len(valid_records) == 1
    assert len(invalid_records) == 1

    assert (
        "duplicate transaction_id"
        in invalid_records[0]["errors"]
    )


def test_multiple_invalid_transactions():
    valid = valid_transaction()

    invalid = valid_transaction()
    invalid["amount"] = -500

    valid_records, invalid_records = validate_transactions(
        [valid, invalid]
    )

    assert len(valid_records) == 1
    assert len(invalid_records) == 1
