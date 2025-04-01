import json
from pathlib import Path
from typing import List, Dict, Any

# Default file location if none is provided
DATA_FILE = Path("data/transactions.json")

def load_transactions(file_path: Path = None) -> List[Dict[str, Any]]:
    """Load transactions from a JSON file (defaults to data/transactions.json)."""
    if file_path is None:
        file_path = DATA_FILE

    if file_path.exists():
        with open(file_path, "r") as f:
            return json.load(f)
    return []

def save_transactions(transactions: List[Dict[str, Any]], file_path: Path = None) -> None:
    """Save transactions to a JSON file (defaults to data/transactions.json)."""
    if file_path is None:
        file_path = DATA_FILE

    with open(file_path, "w") as f:
        json.dump(transactions, f, indent=2)
