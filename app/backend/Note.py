class Note:
    
    valid_durations = [0.0625 * i for i in range(1, 32+1)]  # 从十六分音符到双全音符
    
    def __init__(self, pitch: float, duration: float, quantize: bool = True):
        self.pitch = pitch
        self.duration = self.quantize_duration(duration) if quantize else duration

    def __repr__(self):
        return f"Note(pitch={self.pitch}, duration={self.duration})"

    def quantize_duration(self, duration: float) -> float:
        """
        将音符时值量化到最近的合法分度。
        合法分度范围: 0.0625 (十六分音符) 到 2 (双全音符)。
        输入值假设以全音符 = 1 为基准。
        """
        min_val = 0.0625  # 十六分音符
        max_val = 2.0     # 双全音符
        
        # 限制范围
        duration = max(min_val, min(duration, max_val))
                
        # 找到最近的分度
        closest = min(Note.valid_durations, key=lambda x: abs(x - duration))
        return closest
