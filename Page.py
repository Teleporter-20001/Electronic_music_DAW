import Instrument
import numpy as np
from scipy import signal
from typing import Callable
import soundfile as sf
import threading
import time


class Track:

    def __init__(self, instrument: Instrument.InstrumentBase) -> None:
        self.instrument = instrument
        
    def generate_waveform(self, speed: int, beat_num_per_bar: int, beat_unit: int):
        sample_rate = 44100

        # 四分音符的时长
        quarter_duration = (60 / speed) * (4 / beat_unit)
        # 全音符的时长
        whole_duration = quarter_duration * 4

        waveform = np.array([], dtype=np.float32)

        for note in self.instrument.notes:
            # 直接用全音符时长 * 比例
            duration = whole_duration * note.duration
            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            wave: np.ndarray = self.instrument.generator(2 * np.pi * note.pitch * t)
            waveform = np.concatenate((waveform, wave))
        
        return waveform
    

class Song:
    def __init__(self, title: str, content: str, tracks=None):
        self.title = title
        self.content = content
        self.tracks: list[Track] = tracks if tracks is not None else []

    def add_track(self, track: Track):
        if isinstance(track, Track):
            self.tracks.append(track)
        else:
            raise TypeError("Expected an instance of Track")


    def remove_track(self, trackname: str):
        if any(trackname == track.instrument.name for track in self.tracks):
            self.tracks = [track for track in self.tracks if track.instrument.name != trackname]
        else:
            raise ValueError("Track not found in the song")
                    
            
    def generate_mixed_waveform(self, speed: int, beat_num_per_bar: int, beat_unit: int):
        """生成所有音轨混合后的波形"""
        if not self.tracks:
            return np.array([])
        
        # 生成所有音轨的波形
        waveforms = []
        max_length = 0
        
        for track in self.tracks:
            waveform = track.generate_waveform(speed, beat_num_per_bar, beat_unit)
            waveforms.append(waveform)
            max_length = max(max_length, len(waveform))
        
        # 将所有波形填充到相同长度
        for i in range(len(waveforms)):
            if len(waveforms[i]) < max_length:
                padding = np.zeros(max_length - len(waveforms[i]))
                waveforms[i] = np.concatenate((waveforms[i], padding))
        
        # 混合所有波形
        mixed_waveform = np.sum(waveforms, axis=0) / len(waveforms)  # 平均混合
        # 简单滤波：去除高频噪声
        # b, a = signal.butter(6, 0.15, btype='low')
        # mixed_waveform = signal.filtfilt(b, a, mixed_waveform)
        return mixed_waveform.astype(np.float32)