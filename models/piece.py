import flet as ft
import base64
from io import BytesIO


class Piece:
    def __init__(
        self,
        page: ft.Page,
        number: int,
        original_top: int,
        original_left: int,
        image_bytes: BytesIO,
    ):
        self.page = page
        self.number = number
        self.start_top = 0
        self.start_left = 0
        self.original_top = original_top
        self.original_left = original_left

        base64_str = base64.b64encode(image_bytes.read()).decode("utf-8")
        image_src = f"data:image/png;base64,{base64_str}"

        self.container = ft.Container(
            content=ft.Stack(
                [
                    ft.Image(src=image_src, width=70, height=70, fit=ft.ImageFit.COVER),
                    ft.Container(
                        content=ft.Text(
                            value=str(number),
                            size=20,
                            color=ft.Colors.WHITE,
                            weight=ft.FontWeight.BOLD,
                        ),
                        alignment=ft.alignment.center,
                        width=70,
                        height=70,
                    ),
                ]
            ),
            width=70,
            height=70,
        )

        self.gesture_detector = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            drag_interval=5,
            left=original_left,
            top=original_top,
            content=self.container,
        )

    def setup_drag_handlers(self, board):
        def start_drag_handler(e):
            board.start_drag(e, self)

        def drag_handler(e):
            board.drag(e)

        def drop_handler(e):
            board.drop(e, self)

        self.gesture_detector.on_pan_start = start_drag_handler
        self.gesture_detector.on_pan_update = drag_handler
        self.gesture_detector.on_pan_end = drop_handler

    def place_at(self, top: int, left: int):
        self.gesture_detector.top = top
        self.gesture_detector.left = left
        self.gesture_detector.update()

    def return_to_original_position(self):
        self.place_at(self.original_top, self.original_left)
        self.page.update()
