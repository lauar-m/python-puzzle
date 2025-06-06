import flet as ft
from views.main_window import tela_home
from views.played_games_window import tela_jogos
from utils.components import criar_botao


def main(page: ft.Page):
    page.title = "Quebra-Cabeça"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#DAD7CD"
    page.padding = 0
    page.fonts = {
        "Poppins": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap"
    }
    page.theme = ft.Theme(font_family="Poppins")

    conteudo = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=25
    )

    def atualizar_tela(tela):
        conteudo.controls.clear()
        if tela == "home":
            tela_home(conteudo)
        elif tela == "jogos":
            tela_jogos(conteudo)
        page.update()

    # Sidebar com botões centralizados
    sidebar = ft.Container(
        width=220,
        padding=ft.padding.only(top=40),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#3A5A40", "#344E41"]
        ),
        content=ft.Column(
            spacing=25,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.EXTENSION, size=40, color="white"),
                        ft.Text("Quebra-Cabeça", size=20, color="white", weight=ft.FontWeight.BOLD)
                    ]
                ),
                ft.Divider(color=ft.Colors.WHITE24),
                # Container para centralizar os botões
                ft.Container(
                    width=180,  # Largura fixa para os botões
                    content=ft.Column(
                        spacing=10,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            criar_botao("Home", ft.Icons.HOME, lambda e: atualizar_tela("home")),
                            criar_botao("Jogos", ft.Icons.GAMES, lambda e: atualizar_tela("jogos")),
                        ]
                    )
                ),
                ft.Divider(color=ft.Colors.WHITE24),
                ft.Container(
                    padding=15,
                    border_radius=8,
                    bgcolor=ft.Colors.WHITE10,
                    content=ft.Column(
                        spacing=8,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Jogador", color="white", size=12),
                            ft.Text("Malu", color="white", size=16, weight=ft.FontWeight.BOLD)
                        ]
                    )
                ),
                ft.Container(
                    width=180,
                    content=criar_botao("Sair", ft.Icons.EXIT_TO_APP, lambda e: page.window_close(), cor="#E76F51")
                )
            ]
        )
    )

    layout = ft.Row(
        expand=True,
        spacing=0,
        controls=[
            sidebar,
            ft.VerticalDivider(width=1),
            ft.Container(
                expand=True,
                padding=40,
                content=conteudo,
                bgcolor="#DAD7CD"
            )
        ]
    )

    page.add(layout)
    atualizar_tela("home")

ft.app(target=main, view=ft.WEB_BROWSER, port=8550, host="localhost")