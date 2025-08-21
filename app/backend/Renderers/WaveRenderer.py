import warnings

import numpy as np
from functools import singledispatch

from app.backend.Models.Note import Note
from app.backend.Models.Tracks.InstrumentTrack import InstrumentTrack
from app.common.Exceptions import WaveGenerateError


@singledispatch
def generate_waveform(
        track,
        sample_rate: int,
        speed: int,
        beat_num_per_bar: int,
        beat_unit: int,
        channels: int = 1,
        pan: float = 0
) -> np.ndarray:
    raise WaveGenerateError(f'invalid item type: {type(track)}')


@generate_waveform.register(InstrumentTrack)
def generate_waveform(
        track: InstrumentTrack,
        sample_rate: int,
        speed: int,
        beat_num_per_bar: int,
        beat_unit: int,
        channels: int = 1,
        pan: float = 0
) -> np.ndarray:

    # length of quarter note and full note
    quarter_duration = (60 / speed) * (4 / beat_unit)
    whole_duration = quarter_duration * 4

    max_end_time = max(note.get_end_time(speed=speed, beat_num_per_bar=beat_num_per_bar, beat_unit=beat_unit) for note in track.notes)

    # check memory so that it will not be killed by system
    expected_samples = int(max_end_time * sample_rate)
    expected_memory_mb = expected_samples * channels * 8 / (1024 * 1024)
    memory_limit_mb = 4000
    if expected_memory_mb > memory_limit_mb:
        raise WaveGenerateError(f'expected {expected_memory_mb} MB, which is too large')

    waveform = np.zeros(shape=(int(sample_rate * max_end_time), channels), dtype=np.float64)

    left_gain = np.sqrt((1 - pan) / 2)
    right_gain = np.sqrt((1 + pan) / 2)

    for note in track.notes:
        duration = whole_duration * note.duration
        start_time = note.get_start_time(speed=speed, beat_num_per_bar=beat_num_per_bar)
        end_time = start_time + duration
        start_idx = int(start_time * sample_rate)   # TODO: 这里使用的idx是绝对时刻的，不是相对的，所以跑得通，以后写分段渲染的时候要注意这里
        end_idx = int(end_time * sample_rate)

        # single waveform gen
        t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
        phase = 2 * np.pi * note.pitch * t
        singlewave: np.ndarray = track.inst.generate(phase, time=t)
        # singlewave = singlewave.reshape(singlewave.shape[0], channels)

        # fade in/out
        fade_factor = 1.0 / 200
        fade_len = int(sample_rate * (duration * fade_factor))
        fade_len = min(fade_len, waveform.shape[0] // 2)
        fade_in = np.linspace(0, 1, fade_len, endpoint=False)
        # fade_in = fade_in[:, np.newaxis]
        fade_out = np.linspace(1, 0, fade_len, endpoint=False)
        # fade_out = fade_out[:, np.newaxis]
        singlewave[:fade_len] *= fade_in
        singlewave[-fade_len:] *= fade_out

        end_idx = min(end_idx, waveform.shape[0])
        if not start_idx <= end_idx:
            raise WaveGenerateError(f'start index {start_idx} > end index {end_idx}')
        wave_to_add = singlewave[:end_idx - start_idx]
        if channels == 1:
            # waveform[start_idx:end_idx, :] += singlewave[:end_idx - start_idx, np.newaxis]
            waveform[start_idx:end_idx, 0] += wave_to_add
        elif channels == 2:
            # stereo_singlewave = np.zeros((singlewave.shape[0], channels), dtype=np.float64)
            # stereo_singlewave[:, 0] = singlewave * left_gain
            # stereo_singlewave[:, 1] = singlewave * right_gain
            # waveform[start_idx:end_idx, :] += stereo_singlewave[:end_idx - start_idx]
            stereo_singlewave = np.zeros((wave_to_add.shape[0], channels), dtype=np.float64)
            stereo_singlewave[:, 0] = wave_to_add * left_gain
            stereo_singlewave[:, 1] = wave_to_add * right_gain
            waveform[start_idx:end_idx] += stereo_singlewave
        else:
            raise WaveGenerateError(f'invalid channels: {channels}. channels must be 1 or 2.')

    for effect in track.effects:
        waveform = effect.func(waveform)


    return waveform


class WaveRenderer:

    def __init__(self):
        warnings.warn('not finished yet', DeprecationWarning)
        pass

    @staticmethod
    def generate_waveform(
        # self,
        track,
        sample_rate: int,
        speed: int,
        beat_num_per_bar: int,
        beat_unit: int,
        channels: int = 1,
        pan: float = 0.
    ):
        return generate_waveform(
            track=track,
            sample_rate=sample_rate,
            speed=speed,
            beat_num_per_bar=beat_num_per_bar,
            beat_unit=beat_unit,
            channels=channels,
            pan=pan
        )
