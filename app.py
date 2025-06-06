import flet as ft
from core.board import Board

def main(page: ft.Page):
    board = Board(page)
    page.add(ft.Stack(controls=board.controls, width=1500, height=600))

ft.app(target=main, view=ft.WEB_BROWSER, port=8000)
