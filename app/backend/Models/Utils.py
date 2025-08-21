def note_to_frequency(note: str) -> float:
    """
    将音名(如 'A4', 'C#3', 'Bb2') 转换为频率(Hz)。
    支持范围: A0 ~ C8
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
