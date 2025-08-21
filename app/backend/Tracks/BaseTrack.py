from app.backend.Effects.Basefx import Basefx
import numpy as np

class BaseTrack:
    
    def __init__(self, name: str):
        self.name = name
        self.effects: list[Basefx] = []
        
    def rename(self, newname: str):
        self.name = newname

    def add_effect(self, effect: Basefx):
        self.effects.append(effect)

    def remove_effect(self, effect: Basefx):
        if effect in self.effects:
            self.effects.remove(effect)
            
    def generate_waveform(self, sample_rate: int, speed: int, beat_unit: int):
        return np.array([])  # 基类默认返回空波形，子类应重写此方法
