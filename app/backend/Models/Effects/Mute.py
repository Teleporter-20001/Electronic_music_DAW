from app.backend.Models.Effects.Basefx import Basefx
import numpy as np

class Mute(Basefx):
    def __init__(self) -> None:
        super().__init__()
        self.function = self._mute

    def _mute(self, x: np.ndarray) -> np.ndarray:
        return np.zeros_like(x)
