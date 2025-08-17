from typing import Callable
from Effects.Basefx import Basefx
import numpy as np

class CompressorHard(Basefx):
    def __init__(self, threshold: float = -5., ratio: float = 2., makeup_gain: float = 0.) -> None:
        super().__init__()
        self.threshold: float = threshold
        self.ratio: float = ratio
        self.makeup_gain: float = makeup_gain
        self.function: Callable = self._compress

    def _compress(self, x: np.ndarray) -> np.ndarray:
        """
        简单硬压缩实现：
        - 超过阈值的部分按照 ratio 压缩
        - 小于阈值部分保持不变
        """
        y = np.copy(x)
        over = np.abs(y) > self.threshold
        y[over] = np.sign(y[over]) * (self.threshold + (np.abs(y[over]) - self.threshold) / self.ratio)
        return y * self.makeup_gain
