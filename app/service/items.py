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

	
def check_expiry_alerts(items):
    today = datetime.now().date()
    soon_expiry = []
    expired = []
    
    for item in items:
        if not item.get('active', True):
            continue
            
        try:
            validade = datetime.strptime(item['validade'], '%Y-%m-%d').date()
            days_until_expiry = (validade - today).days
            
            if days_until_expiry < 0:
                expired.append((item, abs(days_until_expiry)))
            elif days_until_expiry <= 7:
                soon_expiry.append((item, days_until_expiry))
        except (ValueError, KeyError):
            continue
    
    if expired or soon_expiry:
        print("\n🚨 ALERTAS DE VALIDADE 🚨")
        print("=" * 50)
        
        # os dois 'if's abaixo sao uma soluçao do stackoverflow
        if expired:
            print("\n❌ PRODUTOS VENCIDOS:")
            expired_data = []
            for item, days_expired in expired:
                expired_data.append([
                    item['nome'], 
                    item['validade'], 
                    f"{days_expired} dias atrás"
                ])
            print(tabulate(expired_data, headers=['Produto', 'Validade', 'Vencido há'], tablefmt='grid'))
        
        if soon_expiry:
            print("\n⚠️  PRODUTOS PRÓXIMOS DO VENCIMENTO:")
            soon_data = []
            for item, days_left in soon_expiry:
                soon_data.append([
                    item['nome'], 
                    item['validade'], 
                    f"{days_left} dias" if days_left > 0 else "Hoje"
                ])
            print(tabulate(soon_data, headers=['Produto', 'Validade', 'Vence em'], tablefmt='grid'))
        
        print("=" * 50)


def add_item():
    ensure_data_dir()
    
    categories = load_categories()
    if not categories:
        print("❌ Nenhuma categoria ativa encontrada! Crie uma categoria primeiro.")
        return
    
    print("\n=== Adicionar Novo Item ===")
    
    # mostra categorias disponíveis
    cat_choices = [f"{cat['id']} - {cat['name']}" for cat in categories]
    
    questions = [
        inquirer.Text('nome', message="Nome do item"),
        inquirer.List('categoria', message="Categoria", choices=cat_choices),
        inquirer.Text('quantidade', message="Quantidade", validate=lambda _, x: x.isdigit()),
        inquirer.Text('unidade_medida', message="Unidade de medida (ex: unidade, kg, litro)"),
        inquirer.Text('validade', message="Data de validade (YYYY-MM-DD)"),
        inquirer.Text('estoque_minimo', message="Estoque mínimo", validate=lambda _, x: x.isdigit()),
    ]
    
    answers = inquirer.prompt(questions)
    if not answers:
        return
    
    # valida a data
    try:
        datetime.strptime(answers['validade'], '%Y-%m-%d')
    except ValueError:
        print("❌ Data inválida! Use o formato YYYY-MM-DD")
        return
    
    categoria_id = int(answers['categoria'].split(' - ')[0])
    
    items = load_data(ITEMS_FILE, [])
    
    new_item = {
        'id': get_next_id(items),
        'nome': answers['nome'],
        'categoria_id': categoria_id,
        'quantidade': int(answers['quantidade']),
        'unidade_medida': answers['unidade_medida'],
        'validade': answers['validade'],
        'estoque_minimo': int(answers['estoque_minimo']),
        'active': True,
        'created_at': datetime.now().isoformat()
    }
    
    items.append(new_item)
    save_data(ITEMS_FILE, items)
    
    log_operation(f"NOVO ITEM ADICIONADO:\n{json.dumps(new_item, indent=2, ensure_ascii=False)}")
    
    print(f"✅ Item '{new_item['nome']}' adicionado com sucesso!")


def remove_item():
    items = load_data(ITEMS_FILE, [])
    active_items = [item for item in items if item.get('active', True)]
    
    if not active_items:
        print("❌ Nenhum item encontrado!")
        return
    
    print("\n=== Remover Item ===")
    
    item_choices = [f"{item['id']} - {item['nome']}" for item in active_items]
    
    questions = [
        inquirer.List('item', message="Selecione o item para remover", choices=item_choices),
        inquirer.Confirm('confirm', message="Tem certeza que deseja remover este item?")
    ]
    
    answers = inquirer.prompt(questions)
    if not answers or not answers['confirm']:
        return
    
    item_id = int(answers['item'].split(' - ')[0])
    
    # encontra e marca como inativo
    for item in items:
        if item['id'] == item_id:
            item['active'] = False
            item['deleted_at'] = datetime.now().isoformat()
            
            save_data(ITEMS_FILE, items)
            log_operation(f"ITEM REMOVIDO:\n{json.dumps(item, indent=2, ensure_ascii=False)}")
            
            print(f"✅ Item '{item['nome']}' removido com sucesso!")
            return
    
    print("❌ Item não encontrado!")
