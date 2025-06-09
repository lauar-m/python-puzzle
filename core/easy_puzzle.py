from core.puzzle import Puzzle

class EasyPuzzle(Puzzle):
    @property
    def grid_size(self) -> int:
        return 3
