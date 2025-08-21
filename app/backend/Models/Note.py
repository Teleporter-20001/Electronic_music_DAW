from app.backend.Models.BeatTime import BeatTime

def quantize_duration(duration: float) -> float:
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


class Note:
    
    valid_durations = [0.0625 * i for i in range(1, 32+1)]  # 从十六分音符到双全音符
    
    def __init__(
            self,
            pitch: float,
            duration: float,
            strength: int = 100,
            starttime: BeatTime = BeatTime(1, 0),
            quantize: bool = True
    ):
        """
        Args:
            pitch: 音高
            duration: 音符时值（占一小节的多长）
            strength: 力度
            starttime: 音符的起始位置
            quantize: 是否要对音符时值进行量化
        """
        self.pitch = pitch
        self.duration = quantize_duration(duration) if quantize else duration
        self.strength = strength
        self.starttime = starttime

    def get_start_time(self, speed: int, beat_num_per_bar: int) -> float:
        """
        计算音符结束时的绝对时刻值。
        Args:
            speed: speed of the song. **以每beat_unit分音符为一拍来衡量。**
            beat_num_per_bar: how many beats are in a single bar
        Returns:
            out: 音符的开始时间（秒）
        """
        single_bar_duration = beat_num_per_bar * 60 / speed
        return (self.starttime.barNum - 1) * single_bar_duration + self.starttime.timeInsideBar

    def get_end_time(self, speed: int, beat_num_per_bar: int, beat_unit: int) -> float:
        whole_length = 60 / speed * 4 / beat_unit * 4
        return self.get_start_time(speed, beat_num_per_bar) + self.duration * whole_length