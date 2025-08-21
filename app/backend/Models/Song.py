import warnings

import numpy as np

from app.backend.Models.Tracks.InstrumentTrack import InstrumentTrack
from app.common.Settings import Settings


class Song:
    def __init__(
        self, 
        title: str = 'Untitled', 
        content: str = '', 
        speed: int = Settings.default_speed,
        beat_num_per_bar: int = Settings.default_beat_num_per_bar,
        beat_unit: int = Settings.default_beat_unit,
        sample_rate: int = Settings.default_sample_rate,
        tracks=None
    ):
        self.title = title
        self.content = content
        self.speed = speed
        self.beat_num_per_bar = beat_num_per_bar
        self.beat_unit = beat_unit
        self.sample_rate = sample_rate
        self.instrumentTracks: list[InstrumentTrack] = tracks if tracks is not None else []
        self.returnTracks = None    # todo
        self.mainTrack = None   # todo

    def add_inst_track(self, track: InstrumentTrack):
        if isinstance(track, InstrumentTrack):
            self.instrumentTracks.append(track)
        else:
            raise TypeError("Expected an instance of Track")


    def remove_inst_track(self, trackname: str):
        if any(t.name == trackname for t in self.instrumentTracks):
            self.instrumentTracks = [t for t in self.instrumentTracks if t.name != trackname]


    def generate_mixed_waveform(self):
        warnings.warn('Processor method should not be called in data structure', DeprecationWarning)
        """生成所有音轨混合后的波形"""
        if not self.instrumentTracks:
            return np.array([])

        # 生成所有音轨的波形
        waveforms = []
        for track in self.instrumentTracks:
            waveform = track.generate_waveform(
                sample_rate=self.sample_rate,
                speed=self.speed,
                beat_unit=self.beat_unit
            )
            waveforms.append(waveform)
            
        # 补齐所有波形到相同长度
        max_length = max(waveform.shape[0] for waveform in waveforms)
        waveforms = [np.pad(waveform, (0, max_length - waveform.shape[0]), mode='constant') for waveform in waveforms]

        # 混合所有波形
        mixed_waveform: np.ndarray = np.sum(waveforms, axis=0) / len(waveforms)  # 平均混合
        return mixed_waveform.astype(np.float32)