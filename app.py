import flet as ft
from core.puzzle import EasyPuzzle, MediumPuzzle, HardPuzzle

def main(page: ft.Page):
    board = HardPuzzle(page)
    page.add(ft.Stack(controls=board.controls, width=1500, height=600))

ft.app(target=main, view=ft.WEB_BROWSER, port=8000)
