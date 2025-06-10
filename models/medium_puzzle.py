from core.puzzle import Puzzle


class MediumPuzzle(Puzzle):
    @property
    def grid_size(self) -> int:
        return 5
