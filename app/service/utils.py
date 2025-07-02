import json
import os
from datetime import datetime

DATA_DIR = "data"
LOG_FILE = os.path.join(DATA_DIR, "movements_log.txt")

def ensure_data_dir():
    """Garante que o diretório data existe"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
