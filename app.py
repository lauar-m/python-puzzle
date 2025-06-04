import flet as ft
import random
import requests
import base64
from io import BytesIO
from PIL import Image

class PuzzleGame:
    def __init__(self, page: ft.Page, rows: int, cols: int):
        """Classe base abstrata para o jogo de quebra-cabeças"""
        self._page = page
        self._rows = rows
        self._cols = cols
        self._size = 300  # Tamanho fixo do tabuleiro
        self._tile_size = self._size // max(rows, cols)
        self._empty_pos = (rows-1, cols-1)  # Posição vazia no canto inferior direito
        self._tiles = []
        self._image_url = ""
        self._image_controls = []
        
        # Configurações da página
        self._page.title = "Quebra-Cabeças Aéreo"
        self._page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self._page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self._page.window_width = 800
        self._page.window_height = 800
        
    def _load_random_image(self, unsplash_access_key):
        """Método abstrato para carregar imagem - deve ser implementado pelas classes filhas"""
        raise NotImplementedError("Este método deve ser implementado pelas classes filhas")
    
    def _create_board(self):
        """Cria o tabuleiro com as peças na posição correta"""
        self._tiles = [[(r, c) for c in range(self._cols)] for r in range(self._rows)]
        
    def _shuffle_board(self):
        """Embaralha o tabuleiro com movimentos válidos"""
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Direita, Baixo, Esquerda, Cima
        empty_r, empty_c = self._empty_pos
        
        for _ in range(1000):  # Número alto de movimentos para garantir boa mistura
            move_r, move_c = random.choice(moves)
            new_r, new_c = empty_r + move_r, empty_c + move_c
            
            if 0 <= new_r < self._rows and 0 <= new_c < self._cols:
                # Troca a peça vazia com a peça adjacente
                self._tiles[empty_r][empty_c] = self._tiles[new_r][new_c]
                self._tiles[new_r][new_c] = (self._rows-1, self._cols-1)  # Nova posição vazia
                empty_r, empty_c = new_r, new_c
        
        self._empty_pos = (empty_r, empty_c)
    
    def _get_tile_image(self, row, col):
        """Retorna a parte da imagem correspondente à peça (row, col)"""
        if (row, col) == (self._rows-1, self._cols-1):
            return None  # Peça vazia
        
        img = Image.open(BytesIO(requests.get(self._image_url).content))
        img = img.resize((self._size, self._size))
        
        # Calcula a região da imagem original
        tile_width = img.width // self._cols
        tile_height = img.height // self._rows
        left = col * tile_width
        upper = row * tile_height
        right = left + tile_width
        lower = upper + tile_height
        
        # Recorta a região
        tile_img = img.crop((left, upper, right, lower))
        return tile_img
    
    def _pil_to_base64(self, pil_image):
        """Converte imagem PIL para base64"""
        img_bytes = BytesIO()
        pil_image.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        return base64.b64encode(img_bytes.read()).decode("utf-8")
    
    def _handle_click(self, e):
        """Manipula o clique em uma peça"""
        tile_idx = int(e.control.data)
        clicked_row = tile_idx // self._cols
        clicked_col = tile_idx % self._cols
        empty_row, empty_col = self._empty_pos
        
        # Verifica se a peça clicada é adjacente à peça vazia
        if (abs(clicked_row - empty_row) == 1 and clicked_col == empty_col) or \
           (abs(clicked_col - empty_col) == 1 and clicked_row == empty_row):
            
            # Troca as peças
            self._tiles[empty_row][empty_col] = self._tiles[clicked_row][clicked_col]
            self._tiles[clicked_row][clicked_col] = (self._rows-1, self._cols-1)
            self._empty_pos = (clicked_row, clicked_col)
            
            # Atualiza a UI
            self._update_ui()
            
            # Verifica se o jogo foi concluído
            if self._check_win():
                self._page.snack_bar = ft.SnackBar(ft.Text("Parabéns! Você completou o quebra-cabeças!"))
                self._page.snack_bar.open = True
                self._page.update()
    
    def _check_win(self):
        """Verifica se o jogador completou o quebra-cabeças"""
        for r in range(self._rows):
            for c in range(self._cols):
                if self._tiles[r][c] != (r, c):
                    return False
        return True
    
    def _update_ui(self):
        """Atualiza a interface do usuário"""
        self._image_controls.clear()
        
        for r in range(self._rows):
            for c in range(self._cols):
                tile_pos = self._tiles[r][c]
                if tile_pos != (self._rows-1, self._cols-1):  # Não é a peça vazia
                    tile_img = self._get_tile_image(*tile_pos)
                    if tile_img:
                        img_control = ft.Image(
                            src_base64=self._pil_to_base64(tile_img),
                            width=self._tile_size,
                            height=self._tile_size,
                            fit=ft.ImageFit.CONTAIN,
                            data=r * self._cols + c,
                        )
                        img_control.on_click = self._handle_click
                        self._image_controls.append(img_control)
                else:
                    # Adiciona um container vazio no lugar da peça vazia
                    empty_control = ft.Container(
                        width=self._tile_size,
                        height=self._tile_size,
                        bgcolor=ft.Colors.GREY_300,
                        data=r * self._cols + c,
                        on_click=self._handle_click,
                    )
                    self._image_controls.append(empty_control)
        
        self._page.clean()
        self._build_ui()
    
    def _build_ui(self):
        """Constrói a interface do usuário"""
        # Grid para as peças do quebra-cabeças
        grid = ft.GridView(
            runs_count=self._cols,
            max_extent=self._tile_size,
            child_aspect_ratio=1,
            spacing=2,
            run_spacing=2,
        )
        
        for control in self._image_controls:
            grid.controls.append(control)
        
        # Botão para reiniciar
        restart_btn = ft.ElevatedButton(
            "Reiniciar Jogo",
            on_click=lambda e: self.start_game(),
            icon=ft.Icons.REFRESH,
        )
        
        # Layout principal
        self._page.add(
            ft.Column(
                [
                    ft.Text(f"Quebra-Cabeças Aéreo - {self.__class__.__name__}", size=20, weight=ft.FontWeight.BOLD),
                    grid,
                    restart_btn,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    
    def start_game(self):
        """Inicia o jogo - método template que usa os métodos abstratos"""
        self._load_random_image("qGaoXW48AxXTWM7BTcGwHQG_zqVpFQfyKtOAicAsM8o")  # Substitua pela sua chave de API do Unsplash
        self._create_board()
        self._shuffle_board()
        self._update_ui()


class EasyPuzzle(PuzzleGame):
    def __init__(self, page: ft.Page):
        super().__init__(page, 3, 3)
    
    def _load_random_image(self, unsplash_access_key):
        """Carrega uma imagem aleatória de avião do Unsplash para o nível fácil"""
        response = requests.get(
            "https://api.unsplash.com/photos/random",
            params={
                "query": "airplane",
                "orientation": "squarish",
                "client_id": unsplash_access_key
            }
        )
        response.raise_for_status()
        data = response.json()
        self._image_url = data["urls"]["regular"]


class MediumPuzzle(PuzzleGame):
    def __init__(self, page: ft.Page):
        super().__init__(page, 5, 5)
    
    def _load_random_image(self, unsplash_access_key):
        """Carrega uma imagem aleatória de avião do Unsplash para o nível médio"""
        response = requests.get(
            "https://api.unsplash.com/photos/random",
            params={
                "query": "airplane",
                "orientation": "squarish",
                "client_id": unsplash_access_key
            }
        )
        response.raise_for_status()
        data = response.json()
        self._image_url = data["urls"]["regular"]


class HardPuzzle(PuzzleGame):
    def __init__(self, page: ft.Page):
        super().__init__(page, 7, 7)
    
    def _load_random_image(self, unsplash_access_key):
        """Carrega uma imagem aleatória de avião do Unsplash para o nível difícil"""
        response = requests.get(
            "https://api.unsplash.com/photos/random",
            params={
                "query": "airplane",
                "orientation": "squarish",
                "client_id": unsplash_access_key
            }
        )
        response.raise_for_status()
        data = response.json()
        self._image_url = data["urls"]["regular"]


def main(page: ft.Page):
    def start_game(difficulty):
        """Inicia o jogo com a dificuldade selecionada"""
        page.clean()
        if difficulty == "easy":
            game = EasyPuzzle(page)
        elif difficulty == "medium":
            game = MediumPuzzle(page)
        else:
            game = HardPuzzle(page)
        game.start_game()
    
    # Tela de seleção de dificuldade
    page.add(
        ft.Column(
            [
                ft.Text("Selecione a Dificuldade", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Tema: Aviões", size=16, color=ft.Colors.BLUE),
                ft.ElevatedButton(
                    "Fácil (3x3)",
                    on_click=lambda e: start_game("easy"),
                    width=200,
                    height=50,
                ),
                ft.ElevatedButton(
                    "Médio (5x5)",
                    on_click=lambda e: start_game("medium"),
                    width=200,
                    height=50,
                ),
                ft.ElevatedButton(
                    "Difícil (7x7)",
                    on_click=lambda e: start_game("hard"),
                    width=200,
                    height=50,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)