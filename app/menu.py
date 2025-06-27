import inquirer
from app import service

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
