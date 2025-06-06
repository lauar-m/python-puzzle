import flet as ft
import random
import time
import threading
from typing import Callable
from utils.api_client import UnsplashClient
from models.game_session import GameSession

class GameWindow:
    def __init__(self, page: ft.Page, difficulty: str, on_exit: Callable):
        self.page = page
        self.difficulty = difficulty
        self.on_exit = on_exit
        self.session = GameSession()
        self.unsplash = UnsplashClient()
        
        # Configurações do jogo
        self.grid_sizes = {"easy": 3, "medium": 5, "hard": 8}
        self.grid_size = self.grid_sizes[difficulty]
        self.piece_size = 80 if difficulty == "hard" else 100
        
        # Estado do jogo
        self.puzzle_pieces = []
        self.dragged_piece = None
        self.correct_positions = [False] * (self.grid_size ** 2)
        
        # Inicializa componentes
        self._init_ui()
        self._start_game()

    def _init_ui(self):
        """Inicializa os componentes da interface"""
        # Controles UI
        self.timer_text = ft.Text("00:00", size=20, weight=ft.FontWeight.BOLD)
        self.moves_text = ft.Text("Movimentos: 0", size=16)
        
        # Botões
        self.exit_button = ft.IconButton(
            icon=ft.icons.EXIT_TO_APP,
            on_click=lambda e: self.on_exit(),
            tooltip="Voltar ao menu"
        )
        
        self.check_button = ft.ElevatedButton(
            "Verificar Solução",
            on_click=self._check_solution,
            icon=ft.icons.CHECK
        )

    def _start_game(self):
        """Inicia uma nova partida"""
        # Carrega imagem do Unsplash
        self.image_url = self.unsplash.get_random_image("nature")
        
        # Cria peças do puzzle
        self._create_puzzle_pieces()
        
        # Inicia cronômetro
        self._start_timer()
        
        # Atualiza UI
        self._update_ui()

    def _create_puzzle_pieces(self):
        """Cria as peças do quebra-cabeça"""
        self.puzzle_pieces.clear()
        piece_ids = list(range(self.grid_size ** 2))
        random.shuffle(piece_ids)
        
        for idx in piece_ids:
            self.puzzle_pieces.append(
                ft.Draggable(
                    group="puzzle",
                    content=ft.Container(
                        width=self.piece_size,
                        height=self.piece_size,
                        border=ft.border.all(1),
                        content=ft.Image(
                            src=f"{self.image_url}?crop={self._get_crop_coords(idx)}",
                            fit=ft.ImageFit.COVER
                        ),
                        on_click=self._on_piece_click
                    ),
                    data=idx,  # ID original da peça
                    content_when_dragging=ft.Container(
                        width=self.piece_size-10,
                        height=self.piece_size-10,
                        opacity=0.8,
                        border=ft.border.all(2, ft.colors.AMBER)
                    )
                )
            )

    def _get_crop_coords(self, piece_id: int) -> str:
        """Calcula as coordenadas de recorte para cada peça"""
        col = piece_id % self.grid_size
        row = piece_id // self.grid_size
        left = col * (100/self.grid_size)
        top = row * (100/self.grid_size)
        right = left + (100/self.grid_size)
        bottom = top + (100/self.grid_size)
        return f"entropy&rect={left}%,{top}%,{right}%,{bottom}%"

    def _create_targets(self):
        """Cria os alvos onde as peças podem ser soltas"""
        targets = []
        for pos in range(self.grid_size ** 2):
            targets.append(
                ft.DragTarget(
                    group="puzzle",
                    content=ft.Container(
                        width=self.piece_size,
                        height=self.piece_size,
                        bgcolor=ft.colors.GREY_200,
                        border=ft.border.all(1),
                    ),
                    data=pos,  # Posição no tabuleiro
                    on_will_accept=self._highlight_target,
                    on_accept=self._on_drop,
                    on_leave=self._reset_target
                )
            )
        return targets

    def _on_piece_click(self, e):
        """Registra movimento quando peça é clicada"""
        self.session.moves += 1
        self.moves_text.value = f"Movimentos: {self.session.moves}"
        self.page.update()

    def _highlight_target(self, e):
        """Destaca o alvo durante o arrasto"""
        e.control.content.bgcolor = (
            ft.colors.AMBER_100 if e.data == "true" 
            else ft.colors.GREY_200
        )
        e.control.update()

    def _on_drop(self, e):
        """Lógica quando peça é solta no alvo"""
        source_piece = e.src.data
        target_pos = e.control.data
        
        # Atualiza estado
        self.correct_positions[target_pos] = (source_piece == target_pos)
        self.session.moves += 1
        
        # Atualiza UI
        e.control.content.content = e.src.content
        e.control.content.bgcolor = (
            ft.colors.GREEN_100 if source_piece == target_pos
            else ft.colors.RED_100
        )
        
        self.moves_text.value = f"Movimentos: {self.session.moves}"
        self.page.update()
        
        # Verifica vitória
        if all(self.correct_positions):
            self._on_win()

    def _reset_target(self, e):
        """Remove destaque do alvo"""
        e.control.content.bgcolor = ft.colors.GREY_200
        e.control.update()

    def _start_timer(self):
        """Inicia o cronômetro da partida"""
        def update_timer():
            while not all(self.correct_positions):
                elapsed = int(time.time() - self.session.start_time)
                self.timer_text.value = f"{elapsed//60:02d}:{elapsed%60:02d}"
                self.page.update()
                time.sleep(1)
        
        threading.Thread(target=update_timer, daemon=True).start()

    def _on_win(self):
        """Ações ao completar o puzzle"""
        elapsed = int(time.time() - self.session.start_time)
        self.page.snack_bar = ft.SnackBar(
            ft.Text(
                f"Parabéns! Tempo: {elapsed//60:02d}:{elapsed%60:02d}",
                color=ft.colors.WHITE
            ),
            bgcolor=ft.colors.GREEN
        )
        self.page.snack_bar.open = True
        self.check_button.disabled = True
        self.page.update()

    def _check_solution(self, e):
        """Verifica manualmente a solução"""
        if all(self.correct_positions):
            self._on_win()
        else:
            incorrect = self.correct_positions.count(False)
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"{incorrect} peças incorretas!"),
                bgcolor=ft.colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _update_ui(self):
        """Atualiza toda a interface do jogo"""
        # Layout do tabuleiro
        puzzle_grid = ft.GridView(
            runs_count=self.grid_size,
            spacing=2,
            run_spacing=2,
            child_aspect_ratio=1,
            width=self.grid_size * (self.piece_size + 2),
            height=self.grid_size * (self.piece_size + 2)
        )
        
        # Adiciona alvos ao grid
        for target in self._create_targets():
            puzzle_grid.controls.append(target)

        # Layout principal
        self.view = ft.Column(
            controls=[
                ft.Row([
                    ft.Text(f"Dificuldade: {self.difficulty.capitalize()}", 
                          weight=ft.FontWeight.BOLD),
                    self.timer_text,
                    self.moves_text,
                    self.exit_button
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.Row([
                    # Imagem original de referência
                    ft.Container(
                        width=300,
                        content=ft.Column([
                            ft.Text("Modelo:", size=16),
                            ft.Image(
                                src=self.image_url,
                                width=300,
                                height=300,
                                fit=ft.ImageFit.COVER,
                                border_radius=10
                            )
                        ], spacing=5)
                    ),
                    
                    # Tabuleiro do puzzle
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Montagem:", size=16),
                            puzzle_grid
                        ], spacing=5)
                    )
                ], spacing=20),
                
                ft.Row([self.check_button], alignment=ft.MainAxisAlignment.CENTER)
            ],
            spacing=20,
            expand=True
        )

    def build(self) -> ft.Column:
        """Retorna o widget raiz da janela"""
        return self.view