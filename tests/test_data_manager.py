import pytest
import os
from pathlib import Path
from app.data_manager import load_transactions, save_transactions

def test_load_transactions_empty(tmp_path):
    data_file = tmp_path / "transactions.json"
    # Now we can pass data_file
    assert load_transactions(data_file) == []

def test_save_load_transactions(tmp_path):
    data_file = tmp_path / "transactions.json"
    sample_data = [{"Ticker": "AAPL", "Shares": 10, "Price Paid": 150.0}]
    # Save to the temp file
    save_transactions(sample_data, data_file)
    # Load from the same temp file
    reloaded = load_transactions(data_file)
    assert reloaded == sample_data
