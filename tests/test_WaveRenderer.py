import pytest
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import sys
sys.path.append('..')

from app.backend.Models.BeatTime import BeatTime
from app.backend.Renderers.WaveRenderer import WaveRenderer
from app.backend.Models.Instruments.DecaySine import DecaySine
from app.backend.Models.Instruments.SineWave import SineWave
from app.backend.Models.Tracks.InstrumentTrack import InstrumentTrack
from app.backend.Models.Note import Note
from app.backend.Models.Utils import note_to_frequency
from app.backend.Runtime.MusicPlayer import MusicPlayer
from app.backend.Models import Utils


sample_rate = 44100
speed = 120
beat_num_per_bar = 4
beat_unit = 4
channel = 1
pan = 0.0

whole_length = 60 / speed * 4 / beat_unit * 4


def generate_input_output():

    inst = SineWave()
    track = InstrumentTrack('myname', inst)
    track.add_note(Note(
        note_to_frequency('C4'),
        1,
        100,
        BeatTime(1, 0.)
    ))
    track.add_note(Note(
        note_to_frequency('D4'),
        1,
        100,
        BeatTime(2, 0.)
    ))
    return WaveRenderer.generate_waveform(track, sample_rate, speed, beat_num_per_bar, beat_unit)


wave = generate_input_output()

def _test_plot():
    matplotlib.use('TkAgg')
    plt.figure(figsize=(18, 6))
    timeseq = np.linspace(0, whole_length, wave.shape[0])
    plt.plot(timeseq, wave)
    plt.xlabel('time')
    plt.ylabel('amplitude')
    plt.title('WaveRenderer test result')
    plt.show()


def test_play():
    player = MusicPlayer()
    player.play_single_waveform(wave, sample_rate)


def test_su_reverse():
    sample_rate = 44100
    speed = 130
    beat_num_per_bar = 4
    beat_unit = 4
    channel = 1
    pan = 0.0
    whole_duration = 60 / speed * beat_unit

    melody = InstrumentTrack(
        'melody',
        DecaySine(0.6)  # type: ignore
        # TriangleWave(0.5)
    )
    melody.add_note(Note(Utils.note_to_frequency('F#4'), 1 / 4, starttime=BeatTime(1, 0)))
    pattern_notes = [
        'C#5', 'Bb4', 'G#4', 'F#4', 'F#4', 'C#5', 'Bb4',
        'F#4', 'C#5', 'Bb4', 'G#4', 'F4', 'F4', 'C#5', 'Bb4', 'G#4', 'F#4'
    ]
    durations: list[float] = [
        1 / 4, 1 / 8, 1 / 4, 1 / 4, 1 / 8, 1 / 4, 1 / 2,
        1 / 4, 1 / 4, 1 / 8, 1 / 4, 1 / 4, 1 / 8, 1 / 4, 1 / 8, 1 / 4, 3 / 8
    ]   # sum: 4 bar
    durations: np.ndarray = np.array(durations)
    offset_for_melody = melody.notes[0].get_end_time(speed, beat_num_per_bar, beat_unit)

    # 计算一次循环的总时值（以全音符为单位）
    # total_duration_per_loop = np.sum(durations)
    accumulated_time = offset_for_melody
    for i in range(4):
        for note_name, dur in zip(pattern_notes, durations):
            melody.add_note(Note(Utils.note_to_frequency(note_name), dur, starttime=BeatTime(1, accumulated_time)))
            accumulated_time += dur * whole_duration

    background_low = InstrumentTrack(
        'background-low',
        DecaySine(0.8)  # type: ignore
    )
    # 修改background_low的音符添加方式
    low_notes = ['B1', 'C#2', 'Eb2', 'Bb1']
    low_durations = [3 / 8, 3 / 8, 1 / 4]
    accumulated_time = 0.0
    for _ in range(4):
        for note in low_notes:
            for dur in low_durations:
                background_low.add_note(
                    Note(Utils.note_to_frequency(note), dur, 100, BeatTime(1, accumulated_time)))
                accumulated_time += dur * whole_duration
    background_low.add_note(Note(Utils.note_to_frequency('B1'), 1 / 4, 100, BeatTime(1, accumulated_time)))

    background_high = InstrumentTrack(
        'background-high',
        DecaySine(0.8)  # type: ignore
    )
    high_notes = ['B2', 'C#3', 'Eb3', 'Bb2']
    high_durations = [3 / 8, 3 / 8, 1 / 4]

    # 修改background_high的音符添加方式
    accumulated_time = 0.0
    for _ in range(4):
        for note in high_notes:
            for dur in high_durations:
                background_high.add_note(
                    Note(Utils.note_to_frequency(note), dur, 100, BeatTime(1, accumulated_time)))
                accumulated_time += dur * whole_duration
    background_high.add_note(Note(Utils.note_to_frequency('B2'), 1 / 4, 100, BeatTime(1, accumulated_time)))

    wave1 = WaveRenderer.generate_waveform(melody, sample_rate, speed, beat_num_per_bar, beat_unit)
    wave2 = WaveRenderer.generate_waveform(background_low, sample_rate, speed, beat_num_per_bar, beat_unit)
    wave3 = WaveRenderer.generate_waveform(background_high, sample_rate, speed, beat_num_per_bar, beat_unit)
    waves = [wave1, wave2, wave3]
    max_length = max(waveform.shape[0] for waveform in waves)
    processed_waves = [np.pad(waveform, (0, max_length - waveform.shape[0]), mode='constant') for waveform in waves]
    mainwave: np.ndarray = np.sum(processed_waves, axis=0) / len(processed_waves)
    player = MusicPlayer()
    # player.play_single_waveform(wave1, sample_rate)
    player.play_single_waveform(mainwave, sample_rate)
