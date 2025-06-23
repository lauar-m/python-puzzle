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

    puzzle_stack = ft.Stack(
        controls=puzzle_view.controls,
        expand=True,
    )
    
    container = ft.Container(
        content=puzzle_stack,
        expand=True,
        padding=20,
    )
    
    content.controls.append(container)
    page.update()

    puzzle_view.shuffle_pieces()
    
    def on_resize(e):
        puzzle_model._calculate_layout(page.width, page.height)
        puzzle_view.shuffle_pieces()
        page.update()
    
    page.on_resize = on_resize