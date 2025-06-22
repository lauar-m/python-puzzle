import flet as ft
from models.piece import Piece
from abc import ABC, abstractmethod
import math
from io import BytesIO
from utils.image_fetcher import ImageFetcher
import random


class Puzzle(ABC):
    CELL_SIZE = 70
    CELL_SPACING = 2
    PIECES_PER_ROW = 8

    def __init__(self, page: ft.Page):
        self.__page = page
        self._slots = []
        self._pieces: list[Piece] = []
        self._controls = []
        self._pieces_positions = {}

        image_url = ImageFetcher.fetch_random_image()
        image_pieces = ImageFetcher.split_image_from_url(image_url, self.grid_size)

        self._calculate_layout()

        self._create_board()
        self._create_pieces(image_pieces=image_pieces)

        self._controls = self._slots + [piece.gesture_detector for piece in self._pieces]

    @property
    @abstractmethod
    def grid_size(self) -> int:
        """Retorna o tamanho do grid (NxN)"""
        pass

    def _calculate_layout(self):
        # Calcula dimensões do tabuleiro
        board_width = self.grid_size * (self.CELL_SIZE + self.CELL_SPACING)
        board_height = self.grid_size * (self.CELL_SIZE + self.CELL_SPACING)

        # Dimensões da área das peças
        total_pieces = self.grid_size * self.grid_size
        pieces_per_column = self.PIECES_PER_ROW  # Máximo de peças por coluna
        columns_needed = math.ceil(total_pieces / pieces_per_column)
        pieces_width = columns_needed * (self.CELL_SIZE + self.CELL_SPACING)

        # Espaço entre tabuleiro e peças
        space_between = 40

        # Largura total do conjunto
        total_width = board_width + space_between + pieces_width

        # Centralizar o conjunto todo na tela
        base_left = (self.__page.width - total_width) / 2
        self.board_left = base_left
        self.board_top = (self.__page.height - board_height) / 3

        # Posicionar peças à direita do tabuleiro
        self._pieces_area = {
            "top": self.board_top,
            "left": self.board_left + board_width + space_between,
        }

    def _create_board(self):
        number = 1
        size = self.grid_size
        for i in range(size):
            for j in range(size):
                slot = ft.Container(
                    content=ft.Text(value=str(number), size=24, color=ft.Colors.BLACK),
                    width=self.CELL_SIZE,
                    height=self.CELL_SIZE,
                    left=self.board_left + (j * (self.CELL_SIZE + self.CELL_SPACING)),
                    top=self.board_top + (i * (self.CELL_SIZE + self.CELL_SPACING)),
                    border=ft.border.all(1),
                    alignment=ft.alignment.center,
                )
                self._slots.append(slot)
                number += 1

    def _create_pieces(self, image_pieces: list[BytesIO]):
        total_pieces = self.grid_size * self.grid_size
        pieces_per_row = self.PIECES_PER_ROW

        for i in range(total_pieces):
            row = i // pieces_per_row
            col = i % pieces_per_row

            piece = Piece(
                self.__page,
                number=i + 1,
                original_top=self._pieces_area["top"]
                + (row * (self.CELL_SIZE + self.CELL_SPACING)),
                original_left=self._pieces_area["left"]
                + (col * (self.CELL_SIZE + self.CELL_SPACING)),
                image_bytes=image_pieces[i],
            )
            piece.setup_drag_handlers(self)
            self._pieces.append(piece)

    def move_on_top(self, control):
        self._controls.remove(control)
        self._controls.append(control)
        self.__page.update()

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
        for slot in self._slots:
            if (
                abs(e.control.top - slot.top) < 20
                and abs(e.control.left - slot.left) < 20
            ):
                # Verifica se  o slot já está ocupado por outra peça
                if (
                    slot in self._pieces_positions
                    and self._pieces_positions[slot] != piece
                ):
                    # Slot ocupado, retornar a peça à posição original
                    break

                piece.place_at(slot.top, slot.left)
                self._pieces_positions[slot] = piece
                found_slot = True
                return

        if not found_slot:
            piece.return_to_original_position()
            # Limpa a posição anterior se existir
            for slot in self._slots:
                if self._pieces_positions.get(slot) == piece:
                    del self._pieces_positions[slot]

    def check_solution(self) -> bool:
        all_correct = True
        for i, slot in enumerate(self._slots):
            piece = self._pieces_positions.get(slot)
            if piece is None or piece.number != i + 1:
                all_correct = False
                break

        return all_correct

    def shuffle_pieces(self):
        pieces_per_row = self.PIECES_PER_ROW

        random.shuffle(self._pieces)

        for i, piece in enumerate(self._pieces):
            row = i // pieces_per_row
            col = i % pieces_per_row

            new_top = self._pieces_area["top"] + (
                row * (self.CELL_SIZE + self.CELL_SPACING)
            )
            new_left = self._pieces_area["left"] + (
                col * (self.CELL_SIZE + self.CELL_SPACING)
            )

            piece.original_top = new_top
            piece.original_left = new_left

            piece.return_to_original_position()
