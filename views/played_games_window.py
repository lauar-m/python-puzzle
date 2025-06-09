import flet as ft
from utils.components import criar_card, COR_SECUNDARIA

def tela_jogos(content: ft.Column):
    historico = ft.Column([
        ft.ListTile(
            leading=ft.Icon(ft.Icons.EXTENSION, color=COR_SECUNDARIA),
            title=ft.Text("Nível Difícil"),
            subtitle=ft.Text("Tempo: 04:32 - 15/06/2023"),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.Icons.EXTENSION, color=COR_SECUNDARIA),
            title=ft.Text("Nível Médio"),
            subtitle=ft.Text("Tempo: 03:18 - 10/06/2023"),
        )
    ])
    content.controls.append(criar_card("📊 Seu Histórico", historico))
