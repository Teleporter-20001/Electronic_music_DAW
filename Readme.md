# 电子音乐制作器

这是一个使用python来实现电子音乐的生成与播放的Project。

## 快速开始

运行`main.py`中的`main`或者`test`函数，你将听到一段事先创建好的旋律。

## 编写说明

`Instrument.py`中定义了各种乐器，包括正弦波、方波、三角波等等。

如果你想要自己实现乐器，也可以仿照这些内置乐器，编写你自己的乐器类（记得继承基类）。**写完了记得去`player.py`里面补充一下`mainkey`到类型的字典。**当你尝试从一个“midi文件”中加载歌曲时，会用到它。

若想要保存旋律，请调用`MusicPlayer.savesong`函数将其保存为smid文件（类似midi文件），或者用`MusicPlayer.save_page_waveform`函数来保存一个wav文件。

为了创建一段旋律，你可以像在`main.py`里面的`main`函数一样，自己创建乐器、音符和音轨，再用音轨生成歌曲。如果你有smid文件，也可以用`MusicPlayer.load_song`函数加载它。

然后，就可以调用MusicPlayer.play_page函数来播放歌曲啦。