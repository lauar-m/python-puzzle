import flet as ft
from models.easy_puzzle import EasyPuzzle
from models.medium_puzzle import MediumPuzzle
from models.hard_puzzle import HardPuzzle
from views.puzzle_view import PuzzleView


def GameWindow(page: ft.Page, content: ft.Column, difficulty: str):
    content.controls.clear()

    # Cria o puzzle conforme a dificuldade escolhida
    if difficulty == "Fácil":
        puzzle_model = EasyPuzzle()
    elif difficulty == "Médio":
        puzzle_model = MediumPuzzle()
    elif difficulty == "Difícil":
        puzzle_model = HardPuzzle()
    else:
        puzzle_model = EasyPuzzle()
    
    puzzle_view = PuzzleView(page, puzzle_model)

    stack = ft.Stack(
        controls=puzzle_view.controls,
        width=page.width,
        height=page.height,
        expand=True
    )
    content.controls.append(stack)

    page.update()

    puzzle_view.shuffle_pieces()