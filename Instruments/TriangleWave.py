from scipy import signal
from Instruments.BaseInst import BaseInst

class TriangleWave(BaseInst):
    
    def __init__(self, width: float = 1):
        self.width = width
        self.generator = lambda x, **kwargs: signal.sawtooth(x, width=self.width)