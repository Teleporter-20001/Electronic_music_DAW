from typing import Callable
import numpy as np

class BaseInst:
    def __init__(self):
        self.generator: Callable = lambda x, **kwargs: np.zeros_like(x)  # 用于生成波形的函数，基类默认值为全0

    def generate(self, x, **kwargs):
        """

        """
        return self.generator(x, **kwargs)
