import inquirer
from app import service

def handle_menu(menu_function):
    """funcao que lida com os menus"""
    should_continue = True
    while should_continue:
        should_continue = menu_function()


def show_items_menu():
    questions = [
        inquirer.List(
            "option",
            message="Menu Itens - Selecione uma ação:",
            choices=[
                "Adicionar item",
                "Remover item",
                "Atualizar item",
                "Listar itens",
                "Buscar item por nome",
                "Voltar"
            ],
        )
    ]
    answer = inquirer.prompt(questions)
    if not answer:
        return False

    option = answer["option"]

    if option == "Adicionar item":
        service.add_item()
    elif option == "Remover item":
        service.remove_item()
    elif option == "Atualizar item":
        service.update_item()
    elif option == "Listar itens":
        service.list_items()
    elif option == "Buscar item por nome":
        service.search_item()
    elif option == "Voltar":
        return False

    return True


def show_categories_menu():
    questions = [
        inquirer.List(
            "option",
            message="Menu Categorias - Selecione uma ação:",
            choices=[
                "Gerenciar categorias",
                "Voltar"
            ],
        )
    ]
    answer = inquirer.prompt(questions)
    if not answer:
        return False

    option = answer["option"]

    if option == "Gerenciar categorias":
        service.manage_categories()
    elif option == "Voltar":
        return False

    return True


def show_main_menu():
    running = True

    while running:
        print("\n=== SIG-Pantry: Sistema de Controle de Despensa Doméstica ===\n")

        questions = [
            inquirer.List(
                "resource",
                message="Selecione um recurso:",
                choices=[
                    "Itens",
                    "Categorias",
                    "Movimentações",
                    "Sair"
                ]
            )
        ]

        answer = inquirer.prompt(questions)
        if not answer:
            print("Nenhuma opção selecionada. Encerrando o sistema.")
            break

        resource = answer["resource"]

        if resource == "Itens":
            # handle_menu(show_items_menu)
            pass
        elif resource == "Categorias":
            # handle_menu(show_categories_menu)
            pass
        elif resource == "Movimentações":
            # handle_menu(show_movements_menu)
            pass
        elif resource == "Sair":
            print("Encerrando o sistema...")
            running = False
