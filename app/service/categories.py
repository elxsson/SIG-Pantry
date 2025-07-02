import json
import os
from datetime import datetime
from tabulate import tabulate
import inquirer
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


def load_categories_data():
    initialize_categories()
    return load_data(CATEGORIES_FILE, [])


def list_categories():
    """lista todas as categorias ativas"""
    categories = load_categories_data()
    active_categories = [cat for cat in categories if cat.get('active', True)]
    
    if not active_categories:
        print("❌ Nenhuma categoria encontrada!")
        return
    
    print(f"\n=== Lista de Categorias ({len(active_categories)} categorias) ===")
    
    table_data = []
    for cat in active_categories:
        # Contar itens na categoria
        items = load_data(os.path.join(DATA_DIR, "items.json"), [])

        # solução do stackoverflow:
        active_items = [item for item in items if item.get('active', True) and item.get('categoria_id') == cat['id']]
        
        table_data.append([
            cat['id'],
            cat['name'],
            len(active_items),
            cat.get('created_at', 'N/A')[:10] if cat.get('created_at') else 'N/A'
        ])
    
    headers = ['ID', 'Nome', 'Qtd Itens', 'Criada em']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))

