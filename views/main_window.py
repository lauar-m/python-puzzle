import flet as ft
from utils.components import create_button, create_card, TEXT_COLOR, SECONDARY_COLOR
from data.services import PuzzleHistoryService
from data.schemas import Difficulty, PuzzleHistory


def MainWindow(content: ft.Column, reload):
    def render_ranking( ranking_data: list[PuzzleHistory]):
        items = []
        for i, record in enumerate(ranking_data):
            minutes = record.solving_time // 60
            seconds = record.solving_time % 60
            formatted_time = f"{minutes:02}:{seconds:02}"

            items.append(
                ft.ListTile(
                    leading=ft.Text(f"{i + 1}º", size=16, weight=ft.FontWeight.BOLD),
                    title=ft.Text(record.user.username, weight=ft.FontWeight.W_500),
                    trailing=ft.Text(f"{formatted_time}", color=TEXT_COLOR),
                )
            )

        return ft.Column([ft.Text(size=18, weight=ft.FontWeight.W_600)] + items)

    ranking_easy, _ = PuzzleHistoryService.get_best_times(Difficulty.easy)
    ranking_medium, _ = PuzzleHistoryService.get_best_times(Difficulty.medium)
    ranking_hard, _ = PuzzleHistoryService.get_best_times(Difficulty.hard)

    content.controls.extend(
        [
            ft.Text("🏆 RANKING", size=24, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
            ft.Row(
                controls=[
                    create_card("Fácil", render_ranking(ranking_easy)),
                    create_card("Médio", render_ranking(ranking_medium)),
                    create_card("Difícil", render_ranking(ranking_hard)),
                ],

                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                spacing=20,
            ),
            ft.Divider(height=20),
            ft.Row(
                controls=[
                    create_button(
                        "JOGAR",
                        ft.Icons.PLAY_ARROW,
                        color=SECONDARY_COLOR,
                        largura=200,
                        action=lambda e: reload("difficulty"),
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ]
    )
