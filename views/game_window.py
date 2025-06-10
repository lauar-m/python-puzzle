import flet as ft
from core.easy_puzzle import EasyPuzzle
from core.medium_puzzle import MediumPuzzle
from core.hard_puzzle import HardPuzzle

def GameWindow(content: ft.Column, difficulty: str):
    content.controls.clear()

    # Cria o puzzle conforme a dificuldade escolhida
    if difficulty == "Fácil":
        puzzle = EasyPuzzle()
    elif difficulty == "Médio":
        puzzle = MediumPuzzle()
    else:
        puzzle = HardPuzzle()

    # Cria a área de jogo com Stack
    game_area = ft.Stack(
        controls=puzzle.controls,
        width=800,
        height=600
    )

    content.controls.append(
        ft.Column(
            controls=[
                ft.Text(f"🧩 Jogo - {difficulty}", size=24, weight=ft.FontWeight.BOLD),
                game_area
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # Embaralhar peças ao iniciar
    puzzle.shuffle_pieces()
