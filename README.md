# SIG-Pantry

### Sistema de Controle de Despensa Doméstica

Este projeto tem como objetivo fornecer uma solução simples e funcional para o controle de itens em uma despensa doméstica. Desenvolvido em Python com abordagem estruturada.

### Funcionalidades

- Adicionar itens à despensa  
- Remover itens (uso ou descarte)  
- Atualizar quantidades dos itens  
- Listar todos os itens cadastrados  
- Buscar itens por nome  
- Alertas de validade ou estoque baixo  
- Login de usuários


### 📁 Estrutura do Projeto

    sig_pantry/
    ├── app/
    │   ├── menu.py
    │   └── service/
    │       ├── __init__.py
    │       ├── categories.py
    │       ├── items.py
    │       ├── movements.py
    ├── .gitignore
    ├── main.py
    └── README.md

### Requisitos

- Python 3.7 ou superior  
- Instalar as dependências listadas em `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Executando

Na raiz do projeto, rode:

```bash
python main.py
```
Isso abrirá o menu interativo, onde você poderá navegar pelas opções disponíveis para gerenciar sua despensa.
