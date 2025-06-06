import flet as ft
from utils.components import criar_botao, criar_card, COR_TEXTO, COR_SECUNDARIA

def tela_home(conteudo: ft.Column):
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
                trailing=ft.Text(f"{tempo}", color=COR_TEXTO),
                subtitle=ft.Text(f"Dificuldade: {dificuldade}", size=12, color=COR_TEXTO,
                                 weight=ft.FontWeight.W_400)
            )
        )

    conteudo.controls.extend([
        ft.Text("🏆 RANKING", size=24, weight=ft.FontWeight.BOLD, color=COR_TEXTO),
        criar_card("Melhores Tempos", ft.Column([
            ranking,
            ft.Divider(height=20),
            ft.Row(
                controls=[criar_botao("JOGAR", ft.Icons.PLAY_ARROW, cor=COR_SECUNDARIA, largura=200)],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ]))
    ])
