import os
import requests
from PIL import Image
from io import BytesIO


class ImageFetcher:
    ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")
    UNSPLASH_API_URL = os.environ.get("UNSPLASH_API_URL")

    @classmethod
    def fetch_random_image(cls, query=None):
        headers = {
            "Authorization": f"Client-ID {cls.ACCESS_KEY}"
        }
        params = {
            "query": query or "nature",
        }

        try:
            response = requests.get(cls.UNSPLASH_API_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if "urls" in data and "regular" in data["urls"]:
                return data["urls"]["regular"]
            else:
                print("Resposta inesperada da API:", data)
                return None
        except requests.RequestException as e:
            raise Exception(f"Erro ao buscar imagem: {e}")

    @classmethod
    def split_image_from_url(cls, image_url: str, grid_size: int) -> list[BytesIO]:
        response = requests.get(image_url)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content))
        widht, height = img.size

        # Recortar imagem para tamanho mínimo dividível pelo grid
        min_dim = min(widht, height)
        img = img.crop((0, 0, min_dim, min_dim))  # quadrado
        piece_size = min_dim // grid_size

        pieces = []

        for row in range(grid_size):
            for col in range(grid_size):
                left = col * piece_size
                upper = row * piece_size
                right = left + piece_size
                lower = upper + piece_size

                piece = img.crop((left, upper, right, lower))
                byte_io = BytesIO()
                piece.save(byte_io, format="PNG")
                byte_io.seek(0)
                pieces.append(byte_io)

        return pieces
