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
    if default is None:
        default = []
    
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    except (json.JSONDecodeError, IOError):
        return default


def save_data(filename, data):
    ensure_data_dir()
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except IOError:
        return False


def get_next_id(items):
    if not items:
        return 1
    return max(item.get('id', 0) for item in items) + 1


