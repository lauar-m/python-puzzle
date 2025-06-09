import flet as ft
from utils.components import create_button, create_card, TEXT_COLOR, SECONDARY_COLOR

def MainWindow(content: ft.Column):
    ranking = ft.Column(
        spacing=10,
        width=400
    )

    dados_ranking = [("MALU", "03:14", "DIF"), ("BIANCA", "03:52", "DIF"), ("TEO", "04:12", "MED")] # botar aqui as dodos do banco de dados

    for i, (nome, tempo, dificuldade) in enumerate(dados_ranking):
        ranking.controls.append(
            ft.ListTile(
                leading=ft.Text(f"{i+1}º", size=16, weight=ft.FontWeight.BOLD),
                title=ft.Text(nome, weight=ft.FontWeight.W_500),
                trailing=ft.Text(f"{tempo}", color=TEXT_COLOR),
                subtitle=ft.Text(f"Dificuldade: {dificuldade}", size=12, color=TEXT_COLOR,
                                 weight=ft.FontWeight.W_400)
            )
        )

    content.controls.extend([
        ft.Text("🏆 RANKING", size=24, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
        create_card("Melhores Tempos", ft.Column([
            ranking,
            ft.Divider(height=20),
            ft.Row(
                controls=[create_button("JOGAR", ft.Icons.PLAY_ARROW, color=SECONDARY_COLOR, largura=200)],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ]))
    ])
