import copy
from typing import Callable
import numpy as np
from scipy import signal

class Note:
    
    valid_durations = [0.0625 * i for i in range(1, 32+1)]  # 从十六分音符到双全音符
    
    def __init__(self, pitch: float, duration: float, quantize: bool = True):
        self.pitch = pitch
        self.duration = self.quantize_duration(duration) if quantize else duration

    def __repr__(self):
        return f"Note(pitch={self.pitch}, duration={self.duration})"

    def quantize_duration(self, duration: float) -> float:
        """
        将音符时值量化到最近的合法分度。
        合法分度范围: 0.0625 (十六分音符) 到 2 (双全音符)。
        输入值假设以全音符 = 1 为基准。
        """
        min_val = 0.0625  # 十六分音符
        max_val = 2.0     # 双全音符
        
        # 限制范围
        duration = max(min_val, min(duration, max_val))
                
        # 找到最近的分度
        closest = min(Note.valid_durations, key=lambda x: abs(x - duration))
        return closest

    
    
class BaseInstrument:
    def __init__(self, name: str):
        self.name = name
        self.mainKey = 'base'   # 用于标识乐器的种类，与名字区分是为了方便命名，而且重建的时候依赖这个来确定乐器类型
        self.generator: Callable = lambda x: x - x  # 用于生成波形的函数，基类默认值为全0
        self.notes: list[Note] = []

    def add_note(self, note):
        if isinstance(note, Note):
            self.notes.append(note)
        else:
            raise TypeError("Only Note instances can be added.")

    def play(self):
        for note in self.notes:
            print(f"Playing {note} on {self.name}")

    def __repr__(self):
        return f"InstrumentBase(name={self.name}, notes={self.notes})"
    
    
class SineInstrument(BaseInstrument):
    def __init__(self, name="Sine Wave Instrument"):
        super().__init__(name)
        self.mainKey = 'sine'
        self.generator = np.sin  # 这里只使用相位
        
        
class SquareInstrument(BaseInstrument):
    def __init__(self, name="Square Wave Instrument"):
        super().__init__(name)
        self.mainKey = 'square'
        self.generator = signal.square


class TriangleInstrument(BaseInstrument):
    def __init__(self, name="Triangle Wave Instrument"):
        super().__init__(name)
        self.mainKey = 'triangle'
        self.generator = signal.sawtooth


class NoiseInstrument(BaseInstrument):
    def __init__(self, name="Noise Instrument"):
        super().__init__(name)
        self.mainKey = 'noise'
        self.generator = lambda x: np.random.normal(0, 1, size=x.shape)  # 生成白噪声
        
        
class SineSquareInstrument(BaseInstrument):
    def __init__(self, name="Sine and Square Instrument"):
        super().__init__(name)
        self.mainKey = 'sine_square'
        self.generator = lambda x: np.clip(0.9 * np.sin(x) + 0.1 * signal.square(x), -1, 1)  # 混合正弦波和方波
        
        
class GtjInstrument(BaseInstrument):
    def __init__(self, name="Tj Instrument"):
        super().__init__(name)
        self.mainKey = 'gtj'
        self.generator = lambda x: abs(np.sin(x)) - np.pi/2  # 绝对值正弦波


class DecaySineInstrument(BaseInstrument):
    def __init__(self, name="Decay Sine Instrument"):
        super().__init__(name)
        self.mainKey = 'decay_sine'
        self.generator = lambda x: np.sin(x) * np.exp(-1.6 * x)  # 衰减正弦波


def trans(instrument: BaseInstrument, newname: str, newclass: type) -> BaseInstrument:
    """
    将一个 InstrumentBase 的实例拷贝为另一个类型的实例。
    """
    if not issubclass(newclass, BaseInstrument):
        raise TypeError("newclass must be a subclass of InstrumentBase")

    new_instrument = newclass(name=newname)
    new_instrument.notes = copy.deepcopy(instrument.notes)  # 复制音符
    return new_instrument


if __name__ == "__main__":
    
    ins1 = SineInstrument()
    ins1.add_note(Note(440.0, 0.3))
    ins1.add_note(Note(493.88, 0.3))
    ins1.add_note(Note(523.25, 0.4, quantize=False))
    ins2 = trans(ins1, "Transposed Square", SquareInstrument)
    print(f"ins1 == ins2: {ins1 == ins2}")  # should be false