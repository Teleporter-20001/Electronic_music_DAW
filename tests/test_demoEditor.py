import os
import importlib
import time

import numpy as np

from app.backend.Models.BeatTime import BeatTime
from app.backend.Models.Instruments.SineWave import SineWave
from app.backend.Models.Note import Note


# ------------- import instruments dynamically -------------
# path: str = '../app/backend/Models/Instruments'
# base_name: str = 'BaseInst'
# instrument_list_scan_result: list[str] = os.listdir(os.path.join(os.path.dirname(__file__), '%s' % path))
# instrument_list_scan_result = [os.path.splitext(i)[0] for i in instrument_list_scan_result if i.endswith('.py') and i != '__init__.py']
# instrument_list_scan_result.remove('%s' % base_name)  # BaseInst is not an instrument for use, it's a base class
# availableInstruments: list[str] = []
# for inst in instrument_list_scan_result:
#     try:
#         module = importlib.import_module(f'%s.{inst}' % path)
#         globals()[inst] = getattr(module, inst)
#         availableInstruments.append(inst)
#     except ImportError:
#         print(f'{inst} not found.')
#     except AttributeError:
#         print(f'{inst} not found.')
#     except Exception as e:
#         print(f'{inst} not found.')
#         raise
# ----------------------------------------------------------
from app.backend.Models.Instruments.DecaySine import DecaySine
from app.backend.Models.Instruments.SquareWave import SquareWave

# ------------ import effects units dynamically ------------
# effect_list_scan_result: list[str] = os.listdir(os.path.join(os.path.dirname(__file__), 'Effects'))
# effect_list_scan_result = [os.path.splitext(i)[0] for i in effect_list_scan_result if i.endswith('.py') and i != '__init__.py']
# effect_list_scan_result.remove('Basefx')  # Basefx is not an effect for use, it's a base class
# availableEffects: list[str] = []
# for effect in effect_list_scan_result:
#     try:
#         module = importlib.import_module(f'Effects.{effect}')
#         globals()[effect] = getattr(module, effect)
#         availableEffects.append(effect)
#     except ImportError:
#         print(f'{effect} not found.')
#     except AttributeError:
#         print(f'{effect} not found.')
#     except Exception as e:
#         print(f'{effect} not found.')
#         raise
# ----------------------------------------------------------
from app.backend.Models.Effects.CompressorHard import CompressorHard
from app.backend.Models.Effects.ReVolume import ReVolume

from app.backend.Models.Tracks.InstrumentTrack import InstrumentTrack
from app.backend.Models.Song import Song
from app.backend.Models.Utils import note_to_frequency
from app.backend.Runtime.MusicPlayer import MusicPlayer
from app.backend.Models import Utils
from app.backend.Renderers.WaveRenderer import WaveRenderer
# from tests.test_WaveRenderer import sample_rate, speed, beat_unit


def test_su_reverse():
    sample_rate = 44100
    speed = 120
    beat_num_per_bar = 4
    beat_unit = 4
    channel = 1
    pan = 0.0
    whole_length = 60 / speed * 4 / beat_unit * 4

    melody = InstrumentTrack(
        'melody', 
        DecaySine(0.6) # type: ignore
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
    ]
    durations: np.ndarray = np.array(durations)

    for i in range(4):
        for note_name, dur in zip(pattern_notes, durations):
            temp_starttime = np.sum(durations[:i]) * whole_length
            melody.add_note(Note(Utils.note_to_frequency(note_name), dur, starttime=BeatTime(1, temp_starttime)))

    background_low = InstrumentTrack(
        'background-low', 
        DecaySine(0.8) # type: ignore
    )
    for _ in range(4):
        for note in ['B1', 'C#2', 'Eb2', 'Bb1']:
            background_low.add_note(Note(Utils.note_to_frequency(note), 3 / 8))
            background_low.add_note(Note(Utils.note_to_frequency(note), 3 / 8))
            background_low.add_note(Note(Utils.note_to_frequency(note), 1 / 4))
    background_low.add_note(Note(Utils.note_to_frequency('B1'), 1 / 4))
    
    background_high = InstrumentTrack(
        'background-high', 
        DecaySine(0.8) # type: ignore
    )
    for _ in range(4):
        for note in ['B2', 'C#3', 'Eb3', 'Bb2']:
            background_high.add_note(Note(Utils.note_to_frequency(note), 3 / 8))
            background_high.add_note(Note(Utils.note_to_frequency(note), 3 / 8))
            background_high.add_note(Note(Utils.note_to_frequency(note), 1 / 4))
    background_high.add_note(Note(Utils.note_to_frequency('B2'), 1 / 4))
    
    testsong = Song(
        'Reverse', 
        'demo song', 
        130
    )
    testsong.add_inst_track(melody)
    testsong.add_inst_track(background_low)
    testsong.add_inst_track(background_high)
    
    player = MusicPlayer()
    player.play_song(testsong)
    # player.play_single_waveform(
    #     melody.generate_waveform(sample_rate=44100, speed=130, beat_unit=4),
    #     sample_rate=44100
    # )


def test_old_audio_engine():
    sample_rate = 44100
    speed = 120
    beat_num_per_bar = 4
    beat_unit = 4
    channel = 1
    pan = 0.0
    whole_length = 60 / speed * 4 / beat_unit * 4

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
    song = Song()
    song.add_inst_track(track)
    player = MusicPlayer()
    time1 = time.time()
    player.play_song(song)
    time2 = time.time()
    print(f'{time2 - time1} seconds elapsed.')
