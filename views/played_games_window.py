import flet as ft
from utils.components import SECONDARY_COLOR, TEXT_COLOR


def PlayedGamesWindow(content: ft.Column):
    played_games_data = [ # pegar do banco
        {
            "image": "https://picsum.photos/id/237/300/180",
            "difficulty": "Difícil",
            "time": "04:32",
            "date": "15/06/2023",
        },
        {
            "image": "https://picsum.photos/id/238/300/180",
            "difficulty": "Médio",
            "time": "03:18",
            "date": "10/06/2023",
        },
        {
            "image": "https://picsum.photos/id/239/300/180",
            "difficulty": "Fácil",
            "time": "02:05",
            "date": "08/06/2023",
        },
        {
            "image": "https://picsum.photos/id/240/300/180",
            "difficulty": "Difícil",
            "time": "05:12",
            "date": "02/06/2023",
        },
        {
            "image": "https://picsum.photos/id/241/300/180",
            "difficulty": "Médio",
            "time": "03:55",
            "date": "01/06/2023",
        },
        {
            "image": "https://picsum.photos/id/242/300/180",
            "difficulty": "Fácil",
            "time": "01:45",
            "date": "28/05/2023",
        },
        {
            "image": "https://picsum.photos/id/243/300/180",
            "difficulty": "Difícil",
            "time": "06:20",
            "date": "25/05/2023",
        },
        {
            "image": "https://picsum.photos/id/244/300/180",
            "difficulty": "Médio",
            "time": "04:10",
            "date": "20/05/2023",
        },
        {
            "image": "https://picsum.photos/id/245/300/180",
            "difficulty": "Fácil",
            "time": "02:30",
            "date": "18/05/2023",
        },
    ]

    row = ft.ResponsiveRow(
        spacing=20, run_spacing=20, alignment=ft.MainAxisAlignment.START
    )

    for played_game in played_games_data:
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
                        src=played_game["image"],
                        width=180,
                        height=180,
                        fit=ft.ImageFit.COVER,
                        border_radius=8,
                    ),
                    ft.Text(
                        f"Dificuldade: {played_game['difficulty']}",
                        color=TEXT_COLOR,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        f"Tempo: {played_game['time']}",
                        color=TEXT_COLOR,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        f"Data: {played_game['date']}",
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
                    "📊 Seu Histórico",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_COLOR,
                ),
                row,
            ],
        )
    )
