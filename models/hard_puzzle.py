from core.puzzle import Puzzle


class HardPuzzle(Puzzle):
    @property
    def grid_size(self) -> int:
        return 7
