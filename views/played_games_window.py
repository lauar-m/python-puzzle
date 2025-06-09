import flet as ft
from utils.components import create_card, SECONDARY_COLOR

def PlayedGamesWindow(content: ft.Column):
    historico = ft.Column([
        ft.ListTile(
            leading=ft.Icon(ft.Icons.EXTENSION, color=SECONDARY_COLOR),
            title=ft.Text("Nível Difícil"),
            subtitle=ft.Text("Tempo: 04:32 - 15/06/2023"),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.Icons.EXTENSION, color=SECONDARY_COLOR),
            title=ft.Text("Nível Médio"),
            subtitle=ft.Text("Tempo: 03:18 - 10/06/2023"),
        )
    ])
    content.controls.append(create_card("📊 Seu Histórico", historico))
