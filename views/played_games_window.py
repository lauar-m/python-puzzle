import base64
import flet as ft
from utils.components import SECONDARY_COLOR, TEXT_COLOR
from data.services import PuzzleHistoryService
from data.schemas import User, Difficulty


def PlayedGamesWindow(content: ft.Column, user: User):
    played_games_data, error = PuzzleHistoryService.get_puzzle_histories_for_user(user.id)

    if played_games_data is None:
        content.controls.append(
            ft.Text("Erro ao carregar o histórico de jogos.", color="red")
        )
        return

    row = ft.ResponsiveRow(
        spacing=20, run_spacing=20, alignment=ft.MainAxisAlignment.START
    )

    for played_game in played_games_data:
        difficulty = "Fácil"
        if played_game.difficulty == Difficulty.medium:
            difficulty = "Médio"
        elif played_game.difficulty == Difficulty.hard:
            difficulty = "Difícil"

        total_seconds = played_game.solving_time
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        formatted_time = f"{minutes:02}:{seconds:02}"

        formatted_date = played_game.played_date.strftime("%d/%m/%Y %H:%M")

        image_data = base64.b64encode(played_game.image).decode("utf-8")
        image_src = f"data:image/png;base64,{image_data}"

        card = ft.Container(
            col={"md": 3, "sm": 12},
            padding=ft.padding.only(top=30, bottom=30, left=5, right=5),
            bgcolor="white",
            border_radius=12,
            border=ft.border.all(1, SECONDARY_COLOR),
            shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.BLACK12),
            content=ft.Column(
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(
                        src=image_src,
                        width=180,
                        height=180,
                        fit=ft.ImageFit.COVER,
                        border_radius=8,
                    ),
                    ft.Text(
                        f"Dificuldade: {difficulty}",
                        color=TEXT_COLOR,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        f"Tempo: {formatted_time}",
                        color=TEXT_COLOR,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        f"Data: {formatted_date}",
                        color=TEXT_COLOR,
                        size=12,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )
        row.controls.append(card)

    content.controls.append(
        ft.Column(
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "📊 HISTÓRICO",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_COLOR,
                ),
                row,
            ],
        )
    )
