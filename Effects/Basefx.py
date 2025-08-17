from typing import Callable

class Basefx:
    def __init__(self) -> None:
        self.function: Callable = lambda x: x

    def func(self, x):
        return self.function(x)
