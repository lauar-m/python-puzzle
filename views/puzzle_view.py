import flet as ft
import math
from io import BytesIO
from abc import ABC
from models.puzzle import Puzzle
from models.piece import Piece
from views.piece_view import PieceView
from utils.image_fetcher import ImageFetcher


class PuzzleView(ABC):
    def __init__(self, page: ft.Page, model: Puzzle):
        self.page = page
        self.model = model

        self.slots = []
        self.pieces: list[PieceView] = []
        self.controls = []

        image_url = ImageFetcher.fetch_random_image()
        image_pieces = ImageFetcher.split_image_from_url(
            image_url, self.model.grid_size
        )

        self.model._calculate_layout(page.width, page.height)

        self._create_board()
        self._create_pieces(image_pieces)

        self.controls = self.slots + [piece.gesture_detector for piece in self.pieces]

    def _create_board(self):
        number = 1
        size = self.model.grid_size
        for i in range(size):
            for j in range(size):
                slot = ft.Container(
                    content=ft.Text(
                        value=str(number), size=24, color=ft.Colors.BLACK
                    ),
                    width=self.model.CELL_SIZE,
                    height=self.model.CELL_SIZE,
                    left=self.model._board_left
                    + (j * (self.model.CELL_SIZE + self.model.CELL_SPACING)),
                    top=self.model._board_top
                    + (i * (self.model.CELL_SIZE + self.model.CELL_SPACING)),
                    border=ft.border.all(1),
                    alignment=ft.alignment.center,
                )
                self.slots.append(slot)
                self.model._register_slot(slot)
                number += 1

    def _create_pieces(self, image_pieces: list[BytesIO]):
        total_pieces = self.model.grid_size * self.model.grid_size
        pieces_per_row = self.model.PIECES_PER_ROW

        for i in range(total_pieces):
            row = i // pieces_per_row
            col = i % pieces_per_row

            piece_model = Piece(
                number=i + 1,
                original_top=self.model._pieces_area["top"]
                + (row * (self.model.CELL_SIZE + self.model.CELL_SPACING)),
                original_left=self.model._pieces_area["left"]
                + (col * (self.model.CELL_SIZE + self.model.CELL_SPACING)),
                image_bytes=image_pieces[i],
            )

            piece_view = PieceView(self.page, piece_model)
            piece_view.setup_drag_handlers(self)

            self.pieces.append(piece_view)
            self.model._register_piece(piece_view)

    def move_on_top(self, control):
        self.controls.remove(control)
        self.controls.append(control)
        self.page.update()

    def start_drag(self, e: ft.DragStartEvent, piece: PieceView):
        self.move_on_top(e.control)
        piece.model.start_top = e.control.top
        piece.model.start_left = e.control.left

    def drag(self, e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    def drop(self, e: ft.DragEndEvent, piece: PieceView):
        found_slot = False
        for slot in self.slots:
            if (
                abs(e.control.top - slot.top) < 20
                and abs(e.control.left - slot.left) < 20
            ):
                # Verifica se o slot já está ocupado
                if (
                    slot in self.model._pieces_positions
                    and self.model._pieces_positions[slot] != piece
                ):
                    break

                piece.place_at(slot.top, slot.left)
                self.model._set_piece_position(slot, piece)
                found_slot = True
                return

        if not found_slot:
            piece.return_to_original_position()
            self.model._clear_piece_position(piece)

    def check_solution(self) -> bool:
        return self.model._check_solution()

    def shuffle_pieces(self):
        self.model._shuffle_pieces()
