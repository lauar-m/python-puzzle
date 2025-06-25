import flet as ft
from models.easy_puzzle import EasyPuzzle
from models.medium_puzzle import MediumPuzzle
from models.hard_puzzle import HardPuzzle
from views.puzzle_view import PuzzleView
from utils.components import create_button, SECONDARY_COLOR
from utils.game_timer import GameTimer
from data.services import PuzzleHistoryService
from data.schemas import User, Difficulty


def GameWindow(page: ft.Page, content: ft.Column, difficulty: str, user: User, reload):
    content.controls.clear()

    # Cria o puzzle conforme a dificuldade escolhida
    difficulty_enum = Difficulty.easy.value
    if difficulty == "Fácil":
        puzzle_model = EasyPuzzle()
        puzzle_height = page.height - 200
    elif difficulty == "Médio":
        puzzle_model = MediumPuzzle()
        difficulty_enum = Difficulty.medium.value
        puzzle_height = page.height - 200
    elif difficulty == "Difícil":
        puzzle_model = HardPuzzle()
        difficulty_enum = Difficulty.hard.value
        puzzle_height = 900
    else:
        puzzle_model = EasyPuzzle()
        puzzle_height = page.height - 200

    puzzle_view = PuzzleView(page, puzzle_model)
    
    # Função para verificar se o puzzle foi resolvido
    def check_puzzle(e):
        if puzzle_view.check_solution():
            timer.stop()
            elapsed_time = timer.get_elapsed_seconds()
            elapsed_time_str = timer.get_elapsed_str()
            PuzzleHistoryService.add_puzzle_history(
                user_id=user.id,
                solving_time=elapsed_time,
                image=puzzle_view.image_bin,
                difficulty=difficulty_enum
            )
            show_dialog("Parabéns! 🎉", f"Você completou o puzzle com sucesso! Seu tempo foi de {elapsed_time_str}", success=True)
            # modal com imagem do puzzle resolvido, tempo e botão para voltar ao menu
        else:
            show_dialog("Atenção", "Algumas peças ainda não estão no lugar correto. Continue tentando!", success=False)

    # Função para mostrar diálogo
    def show_dialog(title, message, success):
        dlg.title = ft.Text(title)
        dlg.content = ft.Text(message)
        if success:
            # Botão que volta para a home
            dlg.actions = [
                ft.TextButton("Voltar ao Menu", on_click=lambda e: close_and_go_home(e)),
            ]
        else:
            # Botão que apenas fecha o diálogo
            dlg.actions = [
                ft.TextButton("OK", on_click=lambda e: close_dialog())
            ]

        dlg.open = True
        page.update()

    def close_and_go_home(e):
        dlg.open = False
        page.update()
        reload("home")

    def close_dialog():
        dlg.open = False
        page.update()

    dlg = ft.AlertDialog(
        title=ft.Text(""),
        content=ft.Text(""),
    )
    page.dialog = dlg
    page.overlay.append(dlg)
    
    # Botão para verificar se o puzzle foi resolvido
    check_puzzle_button = create_button(
        "Verificar jogo",
        ft.Icons.CHECK,
        color=SECONDARY_COLOR,
        largura=200,
        action=check_puzzle,
    )

    container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Stack(  # tabuleiro e peças
                        controls=puzzle_view.controls,
                        width=page.width - 80,
                        height=puzzle_height
                    ),
                    expand=True,
                ),
                ft.Container(  # botão abaixo do jogo, centralizado
                    content=check_puzzle_button,
                    alignment=ft.alignment.center,
                    padding=20,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START,
            expand=True,
            spacing=10,
        ),
        expand=True,
        padding=20,
    )
    
    content.controls.append(container)
    timer = GameTimer()
    timer.start()
    page.update()

    puzzle_view.shuffle_pieces()
    
    def on_resize(e):
        puzzle_model._calculate_layout(page.width, page.height)
        puzzle_view.shuffle_pieces()
        page.update()
    
    page.on_resize = on_resize