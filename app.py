import flet as ft
from models.easy_puzzle import EasyPuzzle
from models.medium_puzzle import MediumPuzzle
from models.hard_puzzle import HardPuzzle
from dotenv import load_dotenv
from views.puzzle_view import PuzzleView


def main(page: ft.Page):
    load_dotenv()
    page.window_width = 800
    page.window_height = 600
    page.window_maximized = True
    page.title = "Puzzle Game"

    puzzle_model = EasyPuzzle()
    puzzle_view = PuzzleView(page, puzzle_model)

    def page_resize(e):
        # Recriar o puzzle quando a janela for redimensionada
        page.controls.clear()
        puzzle_model = EasyPuzzle()
        puzzle_view = PuzzleView(page, puzzle_model)

        page.add(
            ft.Stack(controls=puzzle_view.controls, width=page.width, height=page.height)
        )
        puzzle_view.shuffle_pieces()
        page.update()

    page.on_resize = page_resize
    page.add(ft.Stack(controls=puzzle_view.controls, width=page.width, height=page.height))
    puzzle_view.shuffle_pieces()


ft.app(target=main, view=ft.WEB_BROWSER, port=8000)
