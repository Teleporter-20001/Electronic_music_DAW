from Instruments.BaseInst import BaseInst
import numpy as np
from typing import Callable

class SineWave(BaseInst):
    def __init__(self):
        super().__init__()
        self.generator: Callable = lambda x, **kwargs: np.sin(x)