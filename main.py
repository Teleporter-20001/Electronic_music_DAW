from Instrument import *
from Page import  Song, Track
from Player import MusicPlayer

def note_to_frequency(note: str) -> float:
    """
    将音名(如 'A4', 'C#3', 'Bb2') 转换为频率(Hz)。
    支持范围: A1 ~ A8 -> A0 ~ C8
    """
    # 休止符
    if note == 'R':
        return 0.0
    
    # 半音序列（以C为起点）
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F',
                  'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # 处理可能的降号(Bb 转为 A#)
    note = note.strip().upper().replace('BB', 'A#').replace('EB', 'D#').replace('AB', 'G#').replace('DB', 'C#').replace('GB', 'F#')
    
    # 提取音名和八度
    if len(note) == 2:  # 例如 A4
        name = note[0]
        octave = int(note[1])
    elif len(note) == 3:  # 例如 C#4
        name = note[:2]
        octave = int(note[2])
    else:
        raise ValueError(f"无法解析音符: {note}")
    
    if name not in note_names:
        raise ValueError(f"未知音名: {name}")
    
    # 计算该音与A4的半音差
    note_index = note_names.index(name)
    a4_index = note_names.index('A') + 4 * 12
    target_index = note_index + octave * 12
    n = target_index - a4_index
    
    # 计算频率
    freq = 440.0 * (2 ** (n / 12))
    return round(freq, 3)  # 保留 3 位小数


def main():

    melody = SineInstrument()
    melody.add_note(Note(note_to_frequency('F#4'), 1/4))
    for _ in range(4):
        melody.add_note(Note(note_to_frequency('C#5'), 1/4))
        melody.add_note(Note(note_to_frequency('Bb4'), 1/8))
        melody.add_note(Note(note_to_frequency('G#4'), 1/4))
        melody.add_note(Note(note_to_frequency('F#4'), 1/4))    # bar 1 -> 2
        melody.add_note(Note(note_to_frequency('F#4'), 1/8))
        melody.add_note(Note(note_to_frequency('C#5'), 1/4))
        melody.add_note(Note(note_to_frequency('Bb4'), 1/2))   # bar 2 end
        melody.add_note(Note(note_to_frequency('F#4'), 1/4))
        melody.add_note(Note(note_to_frequency('C#5'), 1/4))
        melody.add_note(Note(note_to_frequency('Bb4'), 1/8))
        melody.add_note(Note(note_to_frequency('G#4'), 1/4))
        melody.add_note(Note(note_to_frequency('F4'), 1/4))     # bar 3 -> 4
        melody.add_note(Note(note_to_frequency('F4'), 1/8))
        melody.add_note(Note(note_to_frequency('C#5'), 1/4))
        melody.add_note(Note(note_to_frequency('Bb4'), 1/8))
        melody.add_note(Note(note_to_frequency('G#4'), 1/4))
        melody.add_note(Note(note_to_frequency('F#4'), 3/8, quantize=False))  # bar 4 end
        
    
    ground_low = SineInstrument()
    for _ in range(4):
        for note in ['B1', 'C#2', 'Eb2', 'Bb1']:
            ground_low.add_note(Note(note_to_frequency(note), 3/8, quantize=False))
            ground_low.add_note(Note(note_to_frequency(note), 3/8, quantize=False))
            ground_low.add_note(Note(note_to_frequency(note), 1/4, quantize=False))
    ground_low.add_note(Note(note_to_frequency('B1'), 1/4))
            
    ground_high = SineInstrument()
    for _ in range(4):
        for note in ['B2', 'C#3', 'Eb3', 'Bb2']:
            ground_high.add_note(Note(note_to_frequency(note), 3/8, quantize=False))
            ground_high.add_note(Note(note_to_frequency(note), 3/8, quantize=False))
            ground_high.add_note(Note(note_to_frequency(note), 1/4, quantize=False))
    ground_high.add_note(Note(note_to_frequency('B2'), 1/4))

    melodyTrack = Track(melody)
    groundLowTrack = Track(ground_low)
    groundHighTrack = Track(ground_high)
    
    testpage =  Song(title="Test Page", content="This is a test page.")
    testpage.add_track(melodyTrack)
    testpage.add_track(groundLowTrack)
    testpage.add_track(groundHighTrack)
    
    testplayer = MusicPlayer(speed=130, beat_num_per_bar=4, beat_unit=4)
    testplayer.save_page_waveform(testpage, "data/test_page.wav")
    testplayer.play_page(testpage)
        
    
def test():
    ins1 = SineInstrument()
    ins1.add_note(Note(note_to_frequency('A0'), 1))
    ins1.add_note(Note(note_to_frequency('R'), 1/2))
    ins1.add_note(Note(note_to_frequency('C8'), 1))
    testtrack = Track(ins1)
    testpage =  Song(title="Test Page", content="This is a test page.")
    testpage.add_track(testtrack)
    testplayer = MusicPlayer(speed=120, beat_num_per_bar=4, beat_unit=4)
    testplayer.play_page(testpage)  
    
if __name__ == "__main__":
    main()
    # test()  # Uncomment to run the test function
