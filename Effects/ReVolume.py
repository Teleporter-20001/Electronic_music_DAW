from Effects.Basefx import Basefx

class ReVolume(Basefx):
    def __init__(self, factor: float):
        super().__init__()
        self.factor = factor
        self.function = lambda x: x * self.factor