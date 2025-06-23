from io import BytesIO


class Piece:
    def __init__(
        self,
        number: int,
        original_top: int,
        original_left: int,
        image_bytes: BytesIO,
    ):
        self.number = number
        self._original_top = original_top
        self._original_left = original_left
        self._start_top = 0
        self._start_left = 0
        self._image_bytes = image_bytes

    @property
    def original_top(self):
        return self._original_top

    @original_top.setter
    def original_top(self, value):
        self._original_top = value

    @property
    def original_left(self):
        return self._original_left

    @original_left.setter
    def original_left(self, value):
        self._original_left = value

    @property
    def start_top(self):
        return self._start_top

    @start_top.setter
    def start_top(self, value):
        self._start_top = value

    @property
    def start_left(self):
        return self._start_left

    @start_left.setter
    def start_left(self, value):
        self._start_left = value
