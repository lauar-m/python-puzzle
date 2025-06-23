from abc import ABC, abstractmethod
import random


class Puzzle(ABC):
    CELL_SIZE = 70
    CELL_SPACING = 2
    PIECES_PER_ROW = 8

    def __init__(self):
        self.slots = []
        self.pieces = []
        self.pieces_positions = {}
        self.board_top = 0
        self.board_left = 0
        self.pieces_area = {}

    @property
    @abstractmethod
    def grid_size(self) -> int:
        """Retorna o tamanho do grid (NxN)"""
        pass

    def calculate_layout(self, page_width, page_height):
        board_width = self.grid_size * (self.CELL_SIZE + self.CELL_SPACING)
        board_height = self.grid_size * (self.CELL_SIZE + self.CELL_SPACING)

        total_pieces = self.grid_size * self.grid_size
        pieces_per_column = self.PIECES_PER_ROW
        columns_needed = -(-total_pieces // pieces_per_column)  # Ceiling division

        pieces_width = columns_needed * (self.CELL_SIZE + self.CELL_SPACING)
        space_between = 40
        total_width = board_width + space_between + pieces_width

        base_left = (page_width - total_width) / 2
        self.board_left = base_left
        self.board_top = (page_height - board_height) / 3

        self.pieces_area = {
            "top": self.board_top,
            "left": self.board_left + board_width + space_between,
        }

    def register_slot(self, slot):
        self.slots.append(slot)

    def register_piece(self, piece):
        self.pieces.append(piece)

    def set_piece_position(self, slot, piece):
        self.pieces_positions[slot] = piece

    def clear_piece_position(self, piece):
        for slot in self.slots:
            if self.pieces_positions.get(slot) == piece:
                del self.pieces_positions[slot]
                break

    def check_solution(self) -> bool:
        for i, slot in enumerate(self.slots):
            piece = self.pieces_positions.get(slot)
            if piece is None or piece.model.number != i + 1:
                return False
        return True

    def shuffle_pieces(self):
        random.shuffle(self.pieces)
        total = len(self.pieces)
        for i, piece in enumerate(self.pieces):
            row = i // self.PIECES_PER_ROW
            col = i % self.PIECES_PER_ROW

            new_top = self.pieces_area["top"] + (
                row * (self.CELL_SIZE + self.CELL_SPACING)
            )
            new_left = self.pieces_area["left"] + (
                col * (self.CELL_SIZE + self.CELL_SPACING)
            )

            piece.model.original_top = new_top
            piece.model.original_left = new_left

            piece.return_to_original_position()
