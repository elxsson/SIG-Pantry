import json
import os
from datetime import datetime

DATA_DIR = "data"
LOG_FILE = os.path.join(DATA_DIR, "movements_log.txt")

def ensure_data_dir():
    """Garante que o diretório data existe"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_data(filename, default=None):
    """Carrega dados de um arquivo JSON"""
    if default is None:
        default = []
    
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    except (json.JSONDecodeError, IOError):
        return default

