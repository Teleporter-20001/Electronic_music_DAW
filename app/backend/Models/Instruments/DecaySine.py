from app.backend.Models.Instruments.BaseInst import BaseInst
import numpy as np
from app.common.Settings import Settings

class DecaySine(BaseInst):
    def __init__(self, decay_factor: float = 1e-3):
        super().__init__()
        self.decay_factor = decay_factor
        self.generator = self.__generate

    def __generate(self, x, **kwargs):
        # freq = max(kwargs.get('freq', 440), 1e-9)  # 默认频率为440Hz
        # time = x / (2 * np.pi * freq)
        time = kwargs.get('time', np.linspace(0, 1./Settings.default_beat_unit, len(x)))
        return np.sin(x) * np.exp(-self.decay_factor * time)