import os
import importlib

from app.backend.Note import Note


# ------------- import instruments dynamically -------------
path: str = 'Instruments'
base_name: str = 'BaseInst'
instrument_list_scan_result: list[str] = os.listdir(os.path.join(os.path.dirname(__file__), '%s' % path))
instrument_list_scan_result = [os.path.splitext(i)[0] for i in instrument_list_scan_result if i.endswith('.py') and i != '__init__.py']
instrument_list_scan_result.remove('%s' % base_name)  # BaseInst is not an instrument for use, it's a base class
availableInstruments: list[str] = []
for inst in instrument_list_scan_result:
    try:
        module = importlib.import_module(f'%s.{inst}' % path)
        globals()[inst] = getattr(module, inst)
        availableInstruments.append(inst)
    except ImportError:
        print(f'{inst} not found.')
    except AttributeError:
        print(f'{inst} not found.')
    except Exception as e:
        print(f'{inst} not found.')
        raise
# ----------------------------------------------------------
# from Instruments.DecaySine import DecaySine
# from Instruments.SquareWave import SquareWave

# ------------ import effects units dynamically ------------
effect_list_scan_result: list[str] = os.listdir(os.path.join(os.path.dirname(__file__), 'Effects'))
effect_list_scan_result = [os.path.splitext(i)[0] for i in effect_list_scan_result if i.endswith('.py') and i != '__init__.py']
effect_list_scan_result.remove('Basefx')  # Basefx is not an effect for use, it's a base class
availableEffects: list[str] = []
for effect in effect_list_scan_result:
    try:
        module = importlib.import_module(f'Effects.{effect}')
        globals()[effect] = getattr(module, effect)
        availableEffects.append(effect)
    except ImportError:
        print(f'{effect} not found.')
    except AttributeError:
        print(f'{effect} not found.')
    except Exception as e:
        print(f'{effect} not found.')
        raise
# ----------------------------------------------------------
# from Effects.CompressorHard import CompressorHard
# from Effects.ReVolume import ReVolume

from Tracks.InstrumentTrack import InstrumentTrack
from Song import Song
from MusicPlayer import MusicPlayer
import Utils

def main():

    melody = InstrumentTrack(
        'melody', 
        DecaySine(0.6) # type: ignore
        # TriangleWave(0.5)
    )
    melody.add_note(Note(Utils.note_to_frequency('F#4'), 1 / 4))
    for _ in range(4):
        melody.add_note(Note(Utils.note_to_frequency('C#5'), 1 / 4))
        melody.add_note(Note(Utils.note_to_frequency('Bb4'), 1 / 8))
        melody.add_note(Note(Utils.note_to_frequency('G#4'), 1 / 4))
        melody.add_note(Note(Utils.note_to_frequency('F#4'), 1 / 4))    # bar 1 -> 2
        melody.add_note(Note(Utils.note_to_frequency('F#4'), 1 / 8))
        melody.add_note(Note(Utils.note_to_frequency('C#5'), 1 / 4))
        melody.add_note(Note(Utils.note_to_frequency('Bb4'), 1 / 2))   # bar 2 end
        melody.add_note(Note(Utils.note_to_frequency('F#4'), 1 / 4))
        melody.add_note(Note(Utils.note_to_frequency('C#5'), 1 / 4))
        melody.add_note(Note(Utils.note_to_frequency('Bb4'), 1 / 8))
        melody.add_note(Note(Utils.note_to_frequency('G#4'), 1 / 4))
        melody.add_note(Note(Utils.note_to_frequency('F4'), 1 / 4))     # bar 3 -> 4
        melody.add_note(Note(Utils.note_to_frequency('F4'), 1 / 8))
        melody.add_note(Note(Utils.note_to_frequency('C#5'), 1 / 4))
        melody.add_note(Note(Utils.note_to_frequency('Bb4'), 1 / 8))
        melody.add_note(Note(Utils.note_to_frequency('G#4'), 1 / 4))
        melody.add_note(Note(Utils.note_to_frequency('F#4'), 3 / 8))  # bar 4 end
        
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
    testsong.add_instTrack(melody)
    testsong.add_instTrack(background_low)
    testsong.add_instTrack(background_high)
    
    player = MusicPlayer()
    player.playSong(testsong)
    
if __name__ == "__main__":
    main()
