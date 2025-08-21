import warnings

import numpy as np
import scipy.signal as signal
from functools import singledispatch

from app.backend.Models.Note import Note
from app.backend.Models.Tracks.InstrumentTrack import InstrumentTrack
from app.common.Exceptions import WaveGenerateError


class WaveRenderer:

    def __init__(self):
        warnings.warn('not finished yet', DeprecationWarning)
        pass


    @singledispatch
    def generate_waveform(self, item, sample_rate: int, speed: int, beat_unit: int):
        raise WaveGenerateError(f'invalid item type: {type(item)}')


    @generate_waveform.register(InstrumentTrack)
    def _generate_waveform(self, track: InstrumentTrack, sample_rate: int, speed: int, beat_unit: int):

        # length of quarter note and full note
        quarter_duration = (60 / speed) * (4 / beat_unit)
        whole_duration = quarter_duration * 4

        waveform = track.inst.generate(np.array([]))
        for note in track.notes:
            duration = whole_duration * note.duration
            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            phase = 2 * np.pi * note.pitch * t
