import flet as ft
from utils.components import create_button, create_card, TEXT_COLOR, SECONDARY_COLOR

def DifficultyWindow(page: ft.Page, content: ft.Column, reload):
    content.controls.clear()
    
    difficulty_buttons = ft.Column(
        spacing=15,
        width=300,
        controls=[
            create_button(
                "FÁCIL",
                ft.Icons.STAR_OUTLINE,
                color=SECONDARY_COLOR,
                largura=300,
                action=lambda e: reload("game", difficulty="Fácil"),
            ),
            create_button(
                "MÉDIO",
                ft.Icons.STAR_HALF_OUTLINED,
                color=SECONDARY_COLOR,
                largura=300,
                action=lambda e: reload("game", difficulty="Médio"),
            ),
            create_button(
                "DIFÍCIL",
                ft.Icons.STAR,
                color=SECONDARY_COLOR,
                largura=300,
                action=lambda e: reload("game", difficulty="Difícil"),
            ),
            ft.Divider(height=20)
        ]
    )
    
    content.controls.extend([
        ft.Text(
            "🧠 DIFICULDADE", 
            size=24, 
            weight=ft.FontWeight.BOLD, 
            color=TEXT_COLOR
        ),
        create_card(
            "Selecione a dificuldade do desafio.",
            ft.Column(
                [
                    ft.Divider(height=10),
                    difficulty_buttons,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
    ])
    
    page.update()