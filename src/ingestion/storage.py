import os
import shutil
from typing import BinaryIO
from src.infrastructure.models import generate_uuid

class StorageService:
    def __init__(self, base_dir: str = "./tmp_storage"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        
    def save_file(self, file_obj: BinaryIO, filename: str) -> str:
        """Saves a file to local storage (acts as S3 mock) and returns path"""
        unique_filename = f"{generate_uuid()}_{filename}"
        path = os.path.join(self.base_dir, unique_filename)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file_obj, buffer)
        return path
        
    def read_file(self, path: str) -> str:
        """Reads a local file as string"""
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
