import os
from datetime import datetime
from tabulate import tabulate
from app.service.utils import load_data, save_data, log_operation, get_next_id, ensure_data_dir

DATA_DIR = "data"
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")

def initialize_categories():
    """inicializa categorias padrão"""
    ensure_data_dir()
    
    if not os.path.exists(CATEGORIES_FILE):
        default_categories = [
            {"id": 1, "name": "Alimentos", "active": True},
            {"id": 2, "name": "Higiene Pessoal", "active": True},
            {"id": 3, "name": "Pet", "active": True},
            {"id": 4, "name": "Medicamentos", "active": True}
        ]
        save_data(CATEGORIES_FILE, default_categories)
