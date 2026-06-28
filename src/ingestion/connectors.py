from abc import ABC, abstractmethod
from typing import List, Dict, Any
import csv
from io import StringIO

class BaseConnector(ABC):
    @abstractmethod
    def extract(self, storage_path: str) -> List[Dict[str, Any]]:
        """Extracts raw data from the storage blob into a list of dictionaries"""
        pass

class CSVConnector(BaseConnector):
    def __init__(self, mapping: Dict[str, str]):
        # mapping example: {"Date": "transaction_date", "Description": "merchant", "Amount": "amount"}
        self.mapping = mapping
        
    def extract(self, storage_path: str) -> List[Dict[str, Any]]:
        records = []
        with open(storage_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                normalized_row = {}
                for csv_col, sys_col in self.mapping.items():
                    normalized_row[sys_col] = row.get(csv_col)
                records.append(normalized_row)
        return records
