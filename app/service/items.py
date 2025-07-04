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

