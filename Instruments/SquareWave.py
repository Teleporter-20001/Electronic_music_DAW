from scipy import signal
from Instruments.BaseInst import BaseInst

class SquareWave(BaseInst):
    
    def __init__(self, occupancy: float = 0.5):
        self.occupancy = occupancy
        self.generator = lambda x, **kwargs: signal.square(x, duty=self.occupancy)