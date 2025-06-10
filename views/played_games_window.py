import flet as ft
from utils.components import SECONDARY_COLOR, TEXT_COLOR


def PlayedGamesWindow(content: ft.Column):
    jogos = [
        {
            "imagem": "https://picsum.photos/id/237/300/180",
            "dificuldade": "Difícil",
            "tempo": "04:32",
            "data": "15/06/2023",
        },
        {
            "imagem": "https://picsum.photos/id/238/300/180",
            "dificuldade": "Médio",
            "tempo": "03:18",
            "data": "10/06/2023",
        },
        {
            "imagem": "https://picsum.photos/id/239/300/180",
            "dificuldade": "Fácil",
            "tempo": "02:05",
            "data": "08/06/2023",
        },
        {
            "imagem": "https://picsum.photos/id/240/300/180",
            "dificuldade": "Difícil",
            "tempo": "05:12",
            "data": "02/06/2023",
        },
        {
            "imagem": "https://picsum.photos/id/241/300/180",
            "dificuldade": "Médio",
            "tempo": "03:55",
            "data": "01/06/2023",
        },
        {
            "imagem": "https://picsum.photos/id/242/300/180",
            "dificuldade": "Fácil",
            "tempo": "01:45",
            "data": "28/05/2023",
        },
        {
            "imagem": "https://picsum.photos/id/243/300/180",
            "dificuldade": "Difícil",
            "tempo": "06:20",
            "data": "25/05/2023",
        },
        {
            "imagem": "https://picsum.photos/id/244/300/180",
            "dificuldade": "Médio",
            "tempo": "04:10",
            "data": "20/05/2023",
        },
        {
            "imagem": "https://picsum.photos/id/245/300/180",
            "dificuldade": "Fácil",
            "tempo": "02:30",
            "data": "18/05/2023",
        },
    ]

    row = ft.ResponsiveRow(
        spacing=20, run_spacing=20, alignment=ft.MainAxisAlignment.START
    )

    for jogo in jogos:
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
                        src=jogo["imagem"],
                        width=180,
                        height=180,
                        fit=ft.ImageFit.COVER,
                        border_radius=8,
                    ),
                    ft.Text(
                        f"Dificuldade: {jogo['dificuldade']}",
                        color=TEXT_COLOR,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        f"Tempo: {jogo['tempo']}",
                        color=TEXT_COLOR,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        f"Data: {jogo['data']}",
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
