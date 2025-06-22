import flet as ft
from models.easy_puzzle import EasyPuzzle
from models.medium_puzzle import MediumPuzzle
from models.hard_puzzle import HardPuzzle
from dotenv import load_dotenv


def main(page: ft.Page):
    load_dotenv()
    page.window_width = 800
    page.window_height = 600
    page.window_maximized = True
    page.title = "Puzzle Game"

    def page_resize(e):
        # Recriar o puzzle quando a janela for redimensionada
        page.controls.clear()
        puzzle = EasyPuzzle(page)
        page.add(
            ft.Stack(controls=puzzle._controls, width=page.width, height=page.height)
        )
        puzzle.shuffle_pieces()
        page.update()

    page.on_resize = page_resize
    puzzle = EasyPuzzle(page)
    page.add(ft.Stack(controls=puzzle._controls, width=page.width, height=page.height))
    puzzle.shuffle_pieces()


ft.app(target=main, view=ft.WEB_BROWSER, port=8000)
