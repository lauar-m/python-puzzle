import flet as ft

# Cores
COR_FUNDO = "#DAD7CD"
COR_CARD = "#FFFFFF"
COR_PRIMARIA = "#A3B18A"
COR_SECUNDARIA = "#588157"
COR_TEXTO = "#344E41"
COR_DESTAQUE = "#E76F51"

def create_button(texto, icone=None, acao=None, largura=180, cor=COR_PRIMARIA):
    return ft.Container(
        width=largura,
        height=45,
        border_radius=30,
        content=ft.ElevatedButton(
            content=ft.Row(
                [ft.Icon(icone), ft.Text(texto)] if icone else [ft.Text(texto)],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8
            ),
            style=ft.ButtonStyle(
                bgcolor=cor,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=30),
                padding=15,
                elevation=1,
            ),
            on_click=acao
        )
    )

def criar_card(titulo, corpo):
    return ft.Container(
        width=400,
        padding=20,
        border_radius=12,
        bgcolor=COR_CARD,
        border=ft.border.all(1, COR_PRIMARIA),
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(titulo, size=20, weight=ft.FontWeight.BOLD, color=COR_TEXTO),
                corpo
            ]
        )
    )
