from datetime import timedelta
from typing import Any

from .config import (
    HIGH_VALUE_THRESHOLD,
    MAX_TRANSACTIONS_IN_WINDOW,
    RAPID_TRANSACTION_WINDOW_MINUTES,
)


def check_high_value(transaction: dict[str, Any]) -> bool:
    """Flag transactions above the configured high-value threshold."""

    return transaction["amount"] >= HIGH_VALUE_THRESHOLD


def check_rapid_transactions(
    transaction: dict[str, Any],
    all_transactions: list[dict[str, Any]],
) -> bool:
    """
    Detect multiple transactions for the same customer
    within a short time window.
    """

    customer_id = transaction["customer_id"]
    transaction_time = transaction["transaction_timestamp"]

    window_start = transaction_time - timedelta(
        minutes=RAPID_TRANSACTION_WINDOW_MINUTES
    )

    matching_transactions = [
        record
        for record in all_transactions
        if (
            record["customer_id"] == customer_id
            and window_start
            <= record["transaction_timestamp"]
            <= transaction_time
        )
    ]

    return len(matching_transactions) >= MAX_TRANSACTIONS_IN_WINDOW


def check_multiple_failures(
    transaction: dict[str, Any],
    all_transactions: list[dict[str, Any]],
) -> bool:
    """Detect repeated failed transactions for a customer."""

    customer_id = transaction["customer_id"]
    transaction_time = transaction["transaction_timestamp"]

    window_start = transaction_time - timedelta(minutes=5)

    failed_transactions = [
        record
        for record in all_transactions
        if (
            record["customer_id"] == customer_id
            and record["status"] == "FAILED"
            and window_start
            <= record["transaction_timestamp"]
            <= transaction_time
        )
    ]

    return len(failed_transactions) >= 2


def calculate_risk_score(
    transaction: dict[str, Any],
    all_transactions: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Apply fraud detection rules and calculate a risk score.

    Rules:
    - High-value transaction: +40
    - Rapid transactions: +30
    - Multiple failed transactions: +30
    """

    score = 0
    reasons: list[str] = []

    if check_high_value(transaction):
        score += 40
        reasons.append("HIGH_VALUE_TRANSACTION")

    if check_rapid_transactions(
        transaction,
        all_transactions,
    ):
        score += 30
        reasons.append("RAPID_TRANSACTIONS")

    if check_multiple_failures(
        transaction,
        all_transactions,
    ):
        score += 30
        reasons.append("MULTIPLE_FAILED_TRANSACTIONS")

    if score >= 70:
        risk_level = "HIGH"
    elif score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        **transaction,
        "risk_score": score,
        "risk_level": risk_level,
        "fraud_reasons": reasons,
        "is_suspicious": score >= 70,
    }


def apply_fraud_rules(
    transactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Apply fraud rules to every transaction."""

    return [
        calculate_risk_score(
            transaction,
            transactions,
        )
        for transaction in transactions
    ]
