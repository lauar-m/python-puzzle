import flet as ft

# Cores
BACKGROUND_COLOR = "#DAD7CD"
CARD_COLOR = "#FFFFFF"
PRIMARY_COLOR = "#A3B18A"
SECONDARY_COLOR = "#588157"
TEXT_COLOR = "#344E41"
THIRD_COLOR = "#3A5A40"
QUIT_COLOR = "#E76F51"


def create_button(text, icon=None, action=None, largura=180, color=PRIMARY_COLOR):
    return ft.Container(
        width=largura,
        height=45,
        border_radius=30,
        content=ft.ElevatedButton(
            content=ft.Row(
                [ft.Icon(icon), ft.Text(text)] if icon else [ft.Text(text)],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            ),
            style=ft.ButtonStyle(
                bgcolor=color,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=30),
                padding=15,
                elevation=1,
            ),
            on_click=action,
        ),
    )


def create_card(titulo, corpo):
    return ft.Container(
        width=400,
        padding=20,
        border_radius=12,
        bgcolor=CARD_COLOR,
        border=ft.border.all(1, PRIMARY_COLOR),
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(titulo, size=20, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                corpo,
            ],
        ),
    )
