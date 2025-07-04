import json
import os
from datetime import datetime, timedelta
from tabulate import tabulate
import inquirer
from app.service.categories import load_categories_data
from app.service.utils import load_data, save_data, log_operation, get_next_id, ensure_data_dir

DATA_DIR = "data"
ITEMS_FILE = os.path.join(DATA_DIR, "items.json")

def load_categories():
    categories = load_categories_data()
    #retorna somente as categorias ativas
    return [cat for cat in categories if cat.get('active', True)]
