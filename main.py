import flet as ft
from views.main_window import MainWindow
from views.played_games_window import PlayedGamesWindow
from views.login_window import LoginWindow
from views.game_window import GameWindow
from views.difficulty_window import DifficultyWindow

from utils.components import (
    create_button,
    TEXT_COLOR,
    THIRD_COLOR,
    QUIT_COLOR,
    BACKGROUND_COLOR,
)
from data.schemas import User


def main(page: ft.Page):
    page.title = "Quebra-Cabeça"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = BACKGROUND_COLOR
    page.padding = 0
    page.fonts = {
        "Poppins": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap"
    }
    page.theme = ft.Theme(font_family="Poppins")

    current_window = {"name": "login"}
    logged_user = {"name": "Visitante"}

    content = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=25,
    )

    def reload_window(window_name: str, user: User = None, difficulty: str = "Fácil"):
        content.controls.clear()
        if user:
            logged_user["name"] = user.username

        current_window["name"] = window_name

        if window_name == "home":
            MainWindow(content, reload_window)
        elif window_name == "played_games":
            PlayedGamesWindow(content)
        elif window_name == "login":
            LoginWindow(content, on_success=lambda user: reload_window("home", user))
        elif window_name == "game":
            GameWindow(page, content, difficulty=difficulty, reload=reload_window)
        elif window_name == "difficulty":
            DifficultyWindow(page, content, reload=reload_window)

        page.controls.clear()
        page.add(build_layout())
        page.update()

    def build_sidebar():
        return ft.Container(
            width=220,
            padding=ft.padding.only(top=40),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[THIRD_COLOR, TEXT_COLOR],
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                # Distribui topo e fundo
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=True,
                controls=[
                    ft.Column(
                        spacing=25,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(ft.Icons.EXTENSION, size=40, color="white"),
                                    ft.Text(
                                        "Quebra-Cabeça",
                                        size=20,
                                        color="white",
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                            ),
                            ft.Divider(color=ft.Colors.WHITE24),
                            ft.Container(
                                width=180,
                                content=ft.Column(
                                    spacing=10,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        create_button(
                                            "Home",
                                            ft.Icons.HOME,
                                            lambda e: reload_window("home"),
                                        ),
                                        create_button(
                                            "Jogos",
                                            ft.Icons.GAMES,
                                            lambda e: reload_window("played_games"),
                                        ),
                                        create_button(
                                            "Jogar",
                                            ft.Icons.PLAY_ARROW,
                                            lambda e: reload_window("difficulty"),
                                        ),
                                    ],
                                ),
                            ),
                            ft.Divider(color=ft.Colors.WHITE24),
                        ],
                    ),
                    ft.Column(
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                padding=15,
                                border_radius=8,
                                bgcolor=ft.Colors.WHITE10,
                                content=ft.Column(
                                    spacing=8,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("Jogador: ", color="white", size=12),
                                        ft.Text(
                                            logged_user["name"],
                                            color="white",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                            expand=True,
                                        ),
                                    ],
                                ),
                            ),
                            ft.Container(
                                width=180,
                                margin=ft.margin.only(bottom=20),
                                content=create_button(
                                    "Sair",
                                    ft.Icons.EXIT_TO_APP,
                                    lambda e: reload_window("login"),
                                    color=QUIT_COLOR,
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        )

    def build_layout():
        return ft.Row(
            expand=True,
            spacing=0,
            controls=[
                *(
                    [build_sidebar(), ft.VerticalDivider(width=1)]
                    if current_window["name"] != "login"
                    else []
                ),
                ft.Container(
                    expand=True, padding=40, content=content, bgcolor=BACKGROUND_COLOR
                ),
            ],
        )

    page.add(build_layout())
    reload_window("login")


ft.app(target=main, view=ft.WEB_BROWSER, port=8550, host="localhost")
