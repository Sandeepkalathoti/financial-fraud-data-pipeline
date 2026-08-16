from datetime import datetime, timezone

from fraud_pipeline.fraud_rules import (
    apply_fraud_rules,
    calculate_risk_score,
    check_high_value,
    check_multiple_failures,
    check_rapid_transactions,
)


def create_transaction(
    transaction_id,
    customer_id,
    timestamp,
    amount=500.0,
    status="SUCCESS",
):
    return {
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "merchant_id": "MERCH001",
        "transaction_timestamp": datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        ),
        "amount": amount,
        "currency": "INR",
        "transaction_type": "PURCHASE",
        "payment_method": "CARD",
        "city": "Hyderabad",
        "status": status,
    }


def test_high_value_transaction():
    transaction = create_transaction(
        "TXN001",
        "CUST001",
        "2026-08-16T10:00:00Z",
        amount=15000,
    )

    assert check_high_value(transaction) is True


def test_normal_value_transaction():
    transaction = create_transaction(
        "TXN002",
        "CUST001",
        "2026-08-16T10:00:00Z",
        amount=500,
    )

    assert check_high_value(transaction) is False


def test_rapid_transactions():
    transactions = [
        create_transaction(
            "TXN001",
            "CUST001",
            "2026-08-16T10:00:00Z",
        ),
        create_transaction(
            "TXN002",
            "CUST001",
            "2026-08-16T10:01:00Z",
        ),
        create_transaction(
            "TXN003",
            "CUST001",
            "2026-08-16T10:02:00Z",
        ),
    ]

    assert check_rapid_transactions(
        transactions[-1],
        transactions,
    ) is True


def test_multiple_failed_transactions():
    transactions = [
        create_transaction(
            "TXN001",
            "CUST001",
            "2026-08-16T10:00:00Z",
            status="FAILED",
        ),
        create_transaction(
            "TXN002",
            "CUST001",
            "2026-08-16T10:01:00Z",
            status="FAILED",
        ),
        create_transaction(
            "TXN003",
            "CUST001",
            "2026-08-16T10:02:00Z",
            status="SUCCESS",
        ),
    ]

    assert check_multiple_failures(
        transactions[-1],
        transactions,
    ) is True


def test_high_risk_transaction():
    transactions = [
        create_transaction(
            "TXN001",
            "CUST001",
            "2026-08-16T10:00:00Z",
            amount=15000,
        ),
        create_transaction(
            "TXN002",
            "CUST001",
            "2026-08-16T10:01:00Z",
            amount=16000,
        ),
        create_transaction(
            "TXN003",
            "CUST001",
            "2026-08-16T10:02:00Z",
            amount=17000,
        ),
    ]

    result = calculate_risk_score(
        transactions[-1],
        transactions,
    )

    assert result["risk_score"] >= 70
    assert result["risk_level"] == "HIGH"
    assert result["is_suspicious"] is True


def test_apply_fraud_rules():
    transactions = [
        create_transaction(
            "TXN001",
            "CUST001",
            "2026-08-16T10:00:00Z",
            amount=500,
        ),
        create_transaction(
            "TXN002",
            "CUST002",
            "2026-08-16T10:05:00Z",
            amount=20000,
        ),
    ]

    results = apply_fraud_rules(transactions)

    assert len(results) == 2

    assert results[0]["risk_level"] == "LOW"

    assert results[1]["risk_level"] == "MEDIUM"
    assert results[1]["is_suspicious"] is False
