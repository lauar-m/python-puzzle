import flet as ft
from models.easy_puzzle import EasyPuzzle
from models.medium_puzzle import MediumPuzzle
from models.hard_puzzle import HardPuzzle
from views.puzzle_view import PuzzleView
from utils.components import create_button, SECONDARY_COLOR
from utils.game_timer import GameTimer
from data.services import PuzzleHistoryService
from data.schemas import User, Difficulty


def GameWindow(page: ft.Page, content: ft.Column, difficulty: str, user: User):
    content.controls.clear()

    # Cria o puzzle conforme a dificuldade escolhida
    difficulty_enum = Difficulty.easy.value
    if difficulty == "Fácil":
        puzzle_model = EasyPuzzle()
    elif difficulty == "Médio":
        puzzle_model = MediumPuzzle()
        difficulty_enum = Difficulty.medium.value
    elif difficulty == "Difícil":
        puzzle_model = HardPuzzle()
        difficulty_enum = Difficulty.hard.value
    else:
        puzzle_model = EasyPuzzle()

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
            show_dialog("Parabéns! 🎉", f"Você completou o puzzle com sucesso! Seu tempo foi de {elapsed_time_str}")
        else:
            show_dialog("Atenção", "Algumas peças ainda não estão no lugar correto. Continue tentando!")

    # Função para mostrar diálogo
    def show_dialog(title, message):
        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            on_dismiss=lambda e: print("Dialog dismissed!")
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

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
                        height=page.height,
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