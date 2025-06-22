from models.puzzle_model import PuzzleModel


class EasyPuzzle(PuzzleModel):
    @property
    def grid_size(self) -> int:
        return 3
