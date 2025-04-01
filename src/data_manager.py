import json
from pathlib import Path
from typing import List, Dict, Any

DATA_FILE = Path("data/transactions.json")

def load_transactions() -> List[Dict[str, Any]]:
    """Load transactions from a JSON file."""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Save transactions to a JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(transactions, f, indent=2)
