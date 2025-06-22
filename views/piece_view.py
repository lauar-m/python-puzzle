import flet as ft
import base64
from io import BytesIO
from models.piece_model import PieceModel


class PieceView:
    def __init__(self, page: ft.Page, model: PieceModel):
        self.page = page
        self.model = model

        image_src = self.__convert_image_to_base64(model.image_bytes)

        self.__container = ft.Container(
            content=ft.Stack(
                [
                    ft.Image(src=image_src, width=70, height=70, fit=ft.ImageFit.COVER),
                    ft.Container(
                        content=ft.Text(
                            value=str(model.number),
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
            left=model.original_left,
            top=model.original_top,
            content=self.__container,
        )

    def __convert_image_to_base64(self, image_bytes: BytesIO):
        base64_str = base64.b64encode(image_bytes.read()).decode("utf-8")
        return f"data:image/png;base64,{base64_str}"

    def setup_drag_handlers(self, board):
        def __start_drag_handler(e):
            board.start_drag(e, self)

        def __drag_handler(e):
            board.drag(e)

        def __drop_handler(e):
            board.drop(e, self)

        self.gesture_detector.on_pan_start = __start_drag_handler
        self.gesture_detector.on_pan_update = __drag_handler
        self.gesture_detector.on_pan_end = __drop_handler

    def place_at(self, top: int, left: int):
        self.gesture_detector.top = top
        self.gesture_detector.left = left
        self.gesture_detector.update()

    def return_to_original_position(self):
        self.place_at(self.model.original_top, self.model.original_left)
        self.page.update()
