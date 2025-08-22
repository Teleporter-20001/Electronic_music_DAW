from functools import total_ordering

@total_ordering
class BeatTime:
    def __init__(self, bar_num: int, time_inside_bar: float):
        """
        在带有小节的音乐中标记时间位置。
        Args:
            bar_num: 第几小节（注意在音乐中小节一般从1开始计数）
            time_inside_bar: 小节开始后的第几秒
        """
        self.barNum = bar_num
        self.timeInsideBar = time_inside_bar

    def __lt__(self, other):
        if self.barNum == other.barNum:
            return self.timeInsideBar < other.timeInsideBar
        else:
            return self.barNum < other.barNum

    def __eq__(self, other):
        return self.barNum == other.barNum and self.timeInsideBar == other.timeInsideBar


