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


def add_category():
    print("\n=== Adicionar Nova Categoria ===")
    
    name = input("Nome da categoria: ").strip()
    
    if not name:
        print("❌ Nome da categoria não pode estar vazio!")
        return
    
    categories = load_categories_data()
    
    # Verifica se já existe:
    if any(cat['name'].lower() == name.lower() and cat.get('active', True) for cat in categories):
        print(f"❌ Categoria '{name}' já existe!")
        return
    
    new_category = {
        'id': get_next_id(categories),
        'name': name,
        'active': True,
        'created_at': datetime.now().isoformat()
    }
    
    categories.append(new_category)
    save_data(CATEGORIES_FILE, categories)
    
    log_operation(f"NOVA CATEGORIA CRIADA:\n{json.dumps(new_category, indent=2, ensure_ascii=False)}")
    
    print(f"✅ Categoria '{name}' criada com sucesso!")


def edit_category():
    categories = load_categories_data()
    active_categories = [cat for cat in categories if cat.get('active', True)]
    
    if not active_categories:
        print("❌ Nenhuma categoria encontrada!")
        return
    
    print("\n=== Editar Categoria ===")
    
    # seleciona categoria
    cat_choices = [f"{cat['id']} - {cat['name']}" for cat in active_categories]
    
    questions = [
        inquirer.List('category', message="Selecione a categoria para editar", choices=cat_choices)
    ]
    
    answer = inquirer.prompt(questions)
    if not answer:
        return
    
    cat_id = int(answer['category'].split(' - ')[0])
    category_to_edit = next((cat for cat in categories if cat['id'] == cat_id), None)
    
    if not category_to_edit:
        print("❌ Categoria não encontrada!")
        return
    
    print(f"Nome atual: {category_to_edit['name']}")
    new_name = input("Novo nome (Enter para manter o atual): ").strip()
    
    if new_name and new_name != category_to_edit['name']:
        # verifica se ja existe
        if any(cat['name'].lower() == new_name.lower() and cat.get('active', True) and cat['id'] != cat_id for cat in categories):
            print(f"❌ Categoria '{new_name}' já existe!")
            return
        
        category_to_edit['name'] = new_name
        category_to_edit['updated_at'] = datetime.now().isoformat()
        
        save_data(CATEGORIES_FILE, categories)
        log_operation(f"CATEGORIA EDITADA:\n{json.dumps(category_to_edit, indent=2, ensure_ascii=False)}")
        
        print(f"✅ Categoria atualizada para '{new_name}'!")
    else:
        print("ℹ️ Nenhuma alteração feita.")

