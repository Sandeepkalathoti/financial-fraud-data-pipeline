import json
from pathlib import Path
from typing import Any

from .config import DATA_FILE


def load_transactions(
    file_path: str = DATA_FILE,
) -> list[dict[str, Any]]:
    """
    Load financial transaction records from a JSONL file.

    Each line in the file represents one transaction.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Transaction file not found: {path}"
        )

    transactions: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                transaction = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc

            if not isinstance(transaction, dict):
                raise ValueError(
                    f"Expected JSON object on line {line_number}"
                )

            transactions.append(transaction)

    return transactions


if __name__ == "__main__":
    transactions = load_transactions()

    print(
        f"Loaded {len(transactions)} transactions"
    )
