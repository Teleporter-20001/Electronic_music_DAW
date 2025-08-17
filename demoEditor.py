from Note import Note
from Instruments.DecaySine import DecaySine
from Tracks.InstrumentTrack import InstrumentTrack
from Song import Song
from MusicPlayer import MusicPlayer
import Utils

def main():

    melody = InstrumentTrack(
        'melody', 
        DecaySine(0.6)
    )
    melody.add_note(Note(Utils.note_to_frequency('F#4'), 1/4))
    for _ in range(4):
        melody.add_note(Note(Utils.note_to_frequency('C#5'), 1/4))
        melody.add_note(Note(Utils.note_to_frequency('Bb4'), 1/8))
        melody.add_note(Note(Utils.note_to_frequency('G#4'), 1/4))
        melody.add_note(Note(Utils.note_to_frequency('F#4'), 1/4))    # bar 1 -> 2
        melody.add_note(Note(Utils.note_to_frequency('F#4'), 1/8))
        melody.add_note(Note(Utils.note_to_frequency('C#5'), 1/4))
        melody.add_note(Note(Utils.note_to_frequency('Bb4'), 1/2))   # bar 2 end
        melody.add_note(Note(Utils.note_to_frequency('F#4'), 1/4))
        melody.add_note(Note(Utils.note_to_frequency('C#5'), 1/4))
        melody.add_note(Note(Utils.note_to_frequency('Bb4'), 1/8))
        melody.add_note(Note(Utils.note_to_frequency('G#4'), 1/4))
        melody.add_note(Note(Utils.note_to_frequency('F4'), 1/4))     # bar 3 -> 4
        melody.add_note(Note(Utils.note_to_frequency('F4'), 1/8))
        melody.add_note(Note(Utils.note_to_frequency('C#5'), 1/4))
        melody.add_note(Note(Utils.note_to_frequency('Bb4'), 1/8))
        melody.add_note(Note(Utils.note_to_frequency('G#4'), 1/4))
        melody.add_note(Note(Utils.note_to_frequency('F#4'), 3/8))  # bar 4 end
        
    background_low = InstrumentTrack(
        'background-low', 
        DecaySine(0.8)
    )
    for _ in range(4):
        for note in ['B1', 'C#2', 'Eb2', 'Bb1']:
            background_low.add_note(Note(Utils.note_to_frequency(note), 3/8))
            background_low.add_note(Note(Utils.note_to_frequency(note), 3/8))
            background_low.add_note(Note(Utils.note_to_frequency(note), 1/4))
    background_low.add_note(Note(Utils.note_to_frequency('B1'), 1/4))
    
    background_high = InstrumentTrack(
        'background-high', 
        DecaySine(0.8)
    )
    for _ in range(4):
        for note in ['B2', 'C#3', 'Eb3', 'Bb2']:
            background_high.add_note(Note(Utils.note_to_frequency(note), 3/8))
            background_high.add_note(Note(Utils.note_to_frequency(note), 3/8))
            background_high.add_note(Note(Utils.note_to_frequency(note), 1/4))
    background_high.add_note(Note(Utils.note_to_frequency('B2'), 1/4))
    
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
