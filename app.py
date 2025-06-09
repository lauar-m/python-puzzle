import flet as ft
from core.easy_puzzle import EasyPuzzle
from core.medium_puzzle import MediumPuzzle
from core.hard_puzzle import HardPuzzle


def main(page: ft.Page):
    page.window_width = 800
    page.window_height = 600
    page.window_maximized = True
    page.title = "Puzzle Game"

    def page_resize(e):
        # Recriar o puzzle quando a janela for redimensionada
        page.controls.clear()
        puzzle = EasyPuzzle(page)
        page.add(ft.Stack(controls=puzzle.controls, width=page.width, height=page.height))
        puzzle.shuffle_pieces()
        page.update()

    page.on_resize = page_resize
    puzzle = EasyPuzzle(page)
    page.add(ft.Stack(controls=puzzle.controls, width=page.width, height=page.height))
    puzzle.shuffle_pieces()


ft.app(target=main, view=ft.WEB_BROWSER, port=8000)
