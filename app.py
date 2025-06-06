import flet as ft

class Piece:
    def __init__(self, page: ft.Page, number: int, original_top: int, original_left: int):
        self.page = page
        self.number = number
        self.start_top = 0
        self.start_left = 0
        self.original_top = original_top
        self.original_left = original_left

        self.container = ft.Container(
            content=ft.Text(value=str(number), size=24, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN,
            width=70,
            height=70,
            alignment=ft.alignment.center
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

class Board:
    def __init__(self, page: ft.Page):
        self.page = page
        self.slots = []
        self.pieces: list[Piece] = []
        self.controls = []
        self.pieces_positions = {}

        self._create_board()
        self._create_pieces()

        self.check_button = ft.ElevatedButton(
            text="Verificar",
            on_click=self.check_solution
        )

        self.message = ft.Text(
            value="",
            color=ft.Colors.GREEN,
            size=20,
            visible=False
        )

        self.controls = (
            self.slots +
            [piece.gesture_detector for piece in self.pieces] +
            [
                ft.Container(content=self.check_button, top=400, left=400),
                ft.Container(content=self.message, top=450, left=400)
            ]
        )

    def _create_board(self):
        number = 1
        for i in range(3):
            for j in range(3):
                slot = ft.Container(
                    content=ft.Text(value=str(number), size=24, color=ft.Colors.BLACK),
                    width=70,
                    height=70,
                    left=j*72,
                    top=i*72,
                    border=ft.border.all(1),
                    alignment=ft.alignment.center
                )
                self.slots.append(slot)
                number += 1

    def _create_pieces(self):
        for i in range(9):
            piece = Piece(
                self.page,
                number=i+1,
                original_top=i*55,
                original_left=400
            )
            piece.setup_drag_handlers(self)
            self.pieces.append(piece)

    def move_on_top(self, control):
        self.controls.remove(control)
        self.controls.append(control)
        self.page.update()

    def start_drag(self, e: ft.DragStartEvent, piece: Piece):
        self.move_on_top(e.control)
        piece.start_top = e.control.top
        piece.start_left = e.control.left

    def drag(self, e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    def drop(self, e: ft.DragEndEvent, piece: Piece):
        found_slot = False
        for slot in self.slots:
            if (
                    abs(e.control.top - slot.top) < 20
                    and abs(e.control.left - slot.left) < 20
            ):
                piece.place_at(slot.top, slot.left)
                self.pieces_positions[slot] = piece
                found_slot = True
                return

        if not found_slot:
            piece.return_to_original_position()
            for slot in self.slots:
                if self.pieces_positions.get(slot) == piece:
                    del self.pieces_positions[slot]

    def check_solution(self, e):
        all_correct = True
        for i, slot in enumerate(self.slots):
            piece = self.pieces_positions.get(slot)
            if piece is None or piece.number != i + 1:
                all_correct = False
                break

        self.message.visible = True
        if all_correct:
            self.message.value = "Parabéns! Você completou o quebra cabeça!"
        else:
            self.message.value = "Continue tentando!"
        self.page.update()


def main(page: ft.Page):
    board = Board(page)
    page.add(ft.Stack(controls=board.controls, width=1500, height=600))

ft.app(target=main, view=ft.WEB_BROWSER, port=8000)
