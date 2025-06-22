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
        self.__page = page
        self.number = number
        self._start_top = 0
        self._start_left = 0
        self._original_top = original_top
        self._original_left = original_left

        base64_str = base64.b64encode(image_bytes.read()).decode("utf-8")
        image_src = f"data:image/png;base64,{base64_str}"

        self.__container = ft.Container(
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
            content=self.__container,
        )

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
        self.place_at(self._original_top, self._original_left)
        self.__page.update()

    @property
    def original_top(self):
        return self._original_top

    @original_top.setter
    def original_top(self, value):
        self._original_top = value

    @property
    def original_left(self):
        return self._original_left

    @original_left.setter
    def original_left(self, value):
        self._original_left = value

    @property
    def start_top(self):
        return self._start_top

    @start_top.setter
    def start_top(self, value):
        self._start_top = value

    @property
    def start_left(self):
        return self._start_left

    @start_left.setter
    def start_left(self, value):
        self._start_left = value
