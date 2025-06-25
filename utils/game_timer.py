import time


class GameTimer:
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        self.start_time = time.time()
        self.end_time = None
    
    def stop(self):
        self.end_time = time.time()

    def get_elapsed_seconds(self) -> int:
        if self.start_time is None:
            return 0
        return int((self.end_time or time.time()) - self.start_time)

    def get_elapsed_str(self) -> str:
        total = self.get_elapsed_seconds()
        minutes = total // 60
        seconds = total % 60
        return f"{minutes:02}:{seconds:02}"
