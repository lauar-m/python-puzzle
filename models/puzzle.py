from abc import ABC, abstractmethod
from models.piece import Piece
import random
import flet as ft


class Puzzle(ABC):
    CELL_SIZE = 70
    CELL_SPACING = 0
    PIECES_PER_ROW = 5

    def __init__(self):
        self._slots = []
        self._pieces = []
        self._pieces_positions = {}
        self._board_top = 0
        self._board_left = 0
        self._pieces_area = {}

    @property
    @abstractmethod
    def grid_size(self) -> int:
        """Retorna o tamanho do grid (NxN)"""
        pass

    def _calculate_layout(self, page_width: float, page_height: float):
        board_width = self.grid_size * (self.CELL_SIZE + self.CELL_SPACING)
        board_height = self.grid_size * (self.CELL_SIZE + self.CELL_SPACING)

        total_pieces = self.grid_size * self.grid_size
        pieces_per_column = self.PIECES_PER_ROW
        columns_needed = -(-total_pieces // pieces_per_column)  # Ceiling division

        pieces_width = columns_needed * (self.CELL_SIZE + self.CELL_SPACING)
        space_between = 40
        total_width = board_width + space_between + pieces_width

        base_left = (page_width - total_width) / 2
        self._board_left = base_left
        self._board_top = (page_height - board_height) / 3

        self._pieces_area = {
            "top": self._board_top,
            "left": self._board_left + board_width + space_between,
        }

    def _register_slot(self, slot: ft.Container):
        self._slots.append(slot)

    def _register_piece(self, piece: Piece):
        self._pieces.append(piece)

    def _set_piece_position(self, slot: ft.Container, piece: Piece):
        self._pieces_positions[slot] = piece

    def _clear_piece_position(self, piece: Piece):
        for slot in self._slots:
            if self._pieces_positions.get(slot) == piece:
                del self._pieces_positions[slot]
                break

    def _check_solution(self) -> bool:
        for i, slot in enumerate(self._slots):
            piece = self._pieces_positions.get(slot)
            if piece is None or piece.model.number != i + 1:
                return False
        return True

    def _shuffle_pieces(self):
        random.shuffle(self._pieces)
        for i, piece in enumerate(self._pieces):
            row = i // self.PIECES_PER_ROW
            col = i % self.PIECES_PER_ROW

            new_top = self._pieces_area["top"] + (
                row * (self.CELL_SIZE + self.CELL_SPACING)
            )
            new_left = self._pieces_area["left"] + (
                col * (self.CELL_SIZE + self.CELL_SPACING)
            )

            piece.model.original_top = new_top
            piece.model.original_left = new_left

            piece.return_to_original_position()
