import flet as ft
from utils.components import create_button, create_card, TEXT_COLOR, SECONDARY_COLOR



def MainWindow(content: ft.Column, reload):
    ranking = ft.Column(spacing=10, width=400)

    ranking_data = [ # pegar do banco
        ("MALU", "03:14", "MED"),
        ("MALU", "03:52", "MED"),
        ("MALU", "04:12", "DIF"),
    ]

    for i, (name, time, difficulty) in enumerate(ranking_data):
        ranking.controls.append(
            ft.ListTile(
                leading=ft.Text(f"{i+1}º", size=16, weight=ft.FontWeight.BOLD),
                title=ft.Text(name, weight=ft.FontWeight.W_500),
                trailing=ft.Text(f"{time}", color=TEXT_COLOR),
                subtitle=ft.Text(
                    f"Dificuldade: {difficulty}",
                    size=12,
                    color=TEXT_COLOR,
                    weight=ft.FontWeight.W_400,
                ),
            )
        )

    content.controls.extend(
        [
            ft.Text("🏆 RANKING", size=24, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
            create_card(
                "Melhores Tempos",
                ft.Column(
                    [
                        ranking,
                        ft.Divider(height=20),
                        ft.Row(
                            controls=[
                                create_button(
                                    "JOGAR",
                                    ft.Icons.PLAY_ARROW,
                                    color=SECONDARY_COLOR,
                                    largura=200,
                                    action=lambda e: reload("game", difficulty="Fácil"),
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ]
                ),
            ),
        ]
    )
