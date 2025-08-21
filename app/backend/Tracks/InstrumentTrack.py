from app.backend.Note import Note
from app.backend.Instruments.BaseInst import BaseInst
from app.backend.Tracks.BaseTrack import BaseTrack
import numpy as np

class InstrumentTrack(BaseTrack):

    def __init__(self, name: str, inst: BaseInst) -> None:
        '''
        Note: tracks should not have the same name.
        '''
        super().__init__(name)
        self.inst: BaseInst = inst
        self.notes: list[Note] = []

    def add_note(self, note: Note) -> None:
        self.notes.append(note)
        
    def remove_note(self, note: Note) -> None:
        if note in self.notes:
            self.notes.remove(note)

    def generate_waveform(self, sample_rate: int, speed: int, beat_unit: int):

        # 四分音符的时长
        quarter_duration = (60 / speed) * (4 / beat_unit)
        # 全音符的时长
        whole_duration = quarter_duration * 4

        waveform = self.inst.generate(np.array([]))

        for note in self.notes:
            duration = whole_duration * note.duration
            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            phase = 2 * np.pi * note.pitch * t
            singlewave: np.ndarray = self.inst.generate(phase, time=t)
            
            # fade in/out
            fade_factor = 1.0 / 200
            fade_in = np.linspace(0, 1, int(sample_rate * (duration * fade_factor)), endpoint=False)
            fade_out = np.linspace(1, 0, int(sample_rate * (duration * fade_factor)), endpoint=False)
            if len(fade_in * 2 > singlewave.size):
                fade_in = fade_in[:singlewave.size // 2]
                fade_out = fade_out[:singlewave.size // 2]
            singlewave[:len(fade_in)] *= fade_in
            singlewave[-len(fade_out):] *= fade_out

            waveform = np.concatenate((waveform, singlewave))
            
        for effect in self.effects:
            waveform = effect.func(waveform)

        return waveform