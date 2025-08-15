import Song
from Instrument import *
import sounddevice as sd
import soundfile as sf
import time
import os
import json
import zlib

class MusicPlayer:

    insTypeMap: dict[str, type] = {
        'sine': SineInstrument,
        'square': SquareInstrument,
        'triangle': TriangleInstrument,
        'noise': NoiseInstrument,
        'sine_square': SineSquareInstrument,
        'gtj': GtjInstrument,
        'decay_sine': DecaySineInstrument,
    }
    
    def __init__(self, speed: int, beat_num_per_bar: int = 4, beat_unit: int = 4):
        self.speed = speed
        self.beat_num_per_bar = beat_num_per_bar
        self.beat_unit = beat_unit
        
    
    def play_page(self, page: Song.Song):
        print(f"Playing page: {page.title}")    
    
        mixed_waveform = page.generate_mixed_waveform(self.speed, self.beat_num_per_bar, self.beat_unit)
        if len(mixed_waveform) == 0:
            print("No tracks to play.")
            return

        try:
            sd.play(mixed_waveform, samplerate=44100)
            while sd.get_stream().active:
                time.sleep(0.1)
        except KeyboardInterrupt:
            sd.stop()
            print("Playback stopped by user.")
        except Exception as e:
            print(f"Error occurred during playback: {e}")
            sd.stop()
        finally:
            if sd.get_stream().active:
                sd.stop()
                print("Playback finished.")
                
                
    def save_page_waveform(self, page: Song.Song, filename: str):
        """将页面的波形保存为音频文件"""
        mixed_waveform = page.generate_mixed_waveform(self.speed, self.beat_num_per_bar, self.beat_unit)
        if len(mixed_waveform) == 0:
            print("No tracks to save.")
            return
        
        try:
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
            sf.write(filename, mixed_waveform, samplerate=44100)
            print(f"Waveform saved to {filename}")
        except Exception as e:
            print(f"Error saving waveform: {e}")
            
            
    def save_song(self, song: Song.Song, filename: str):
        """
        Save current song as a specific-format(*.smid) file. 
        Args:
            filename (str): The target filename(without '.smid').
        """
        if song is None:
            print('no song.')
            return
        if not isinstance(song, Song.Song):
            raise TypeError("Expected an instance of Song")
        
        if not filename.endswith('.smid'):
            filename += ".smid"
        
        song_data = {
            "format": "SMID",
            "version": 1,
            "meta": {
                "title": song.title,
                "content": song.content,
            },
            "tempo": {
                "speed": self.speed,
                "beat_num_per_bar": self.beat_num_per_bar,
                "beat_unit": self.beat_unit,
            },
            "tracks": [
                {
                    "instrument": {
                        "name": track.instrument.name,
                        "mainKey": track.instrument.mainKey,
                    },
                    "notes": [
                        {"pitch": note.pitch, "duration": note.duration}
                        for note in track.instrument.notes
                    ],
                }
                for track in song.tracks
            ],
        }
            
        try:
            if not os.path.exists(os.path.dirname(filename)) \
                    and os.access(os.path.dirname(filename), os.W_OK) \
                    and not filename.startswith('.smid'):
                os.makedirs(os.path.dirname(filename))
            with open(filename, 'wb') as f:
                json_str = json.dumps(song_data, ensure_ascii=False)
                compressed_json_str = zlib.compress(json_str.encode("utf-8"))
                f.write(compressed_json_str)
            print(f"Song saved to {filename}")
        except Exception as e:
            print(f"Error saving song: {e}")
            

    def load_song(self, filename: str) -> Song.Song | None:
        """
        从 .smid（JSON）文件加载乐谱，构建并返回 Song.Song 实例。
        同时更新播放器的 tempo（speed/beat）。
        """
        if not filename.endswith(".smid"):
            filename += ".smid"

        if not os.path.isfile(filename):
            raise FileNotFoundError(f"Song file not found: {filename}")

        try:
            with open(filename, "rb") as f:
                origincontents = f.read()
                datastr = zlib.decompress(origincontents).decode("utf-8")
                data = json.loads(datastr)
        except Exception as e:
            print(f"Error reading song file: {e}")
            return None

        # 基本校验
        if not isinstance(data, dict) or data.get("format") != "SMID":
            print("Invalid song file format.")
            return None
        if data.get("version") not in (1,):
            print(f"Incompatible song version: {data.get('version')}")
            return None

        # 恢复元信息与节拍信息
        meta = data.get("meta", {}) or {}
        tempo = data.get("tempo", {}) or {}
        title = meta.get("title", "Untitled")
        content = meta.get("content", "")

        # 更新播放器的节拍参数
        self.speed = tempo.get("speed", self.speed)
        self.beat_num_per_bar = tempo.get("beat_num_per_bar", self.beat_num_per_bar)
        self.beat_unit = tempo.get("beat_unit", self.beat_unit)

        # 构建 Song.Song
        try:
            try:
                song = Song.Song(title, content)
            except TypeError:
                song = Song.Song(title=title, content=content)
        except Exception as e:
            print(f"Error constructing Song.Song: {e}")
            return None

        # 确保有容器存放轨道
        if not hasattr(song, "tracks") or not isinstance(getattr(song, "tracks"), list):
            # 如果没有 tracks 列表，但有 add_track 方法，后续使用 add_track
            use_add_track = hasattr(song, "add_track") and callable(getattr(song, "add_track"))
            if not use_add_track:
                # 回退：给 song 附加一个 tracks 列表
                setattr(song, "tracks", [])
        else:
            use_add_track = False

        # 逐轨道重建
        tracks_data = data.get("tracks", []) or []
        for t in tracks_data:
            inst_info = t.get("instrument", {}) or {}
            notes_info = t.get("notes", []) or []

            name = inst_info.get("name", "Instrument")
            main_key = inst_info.get("mainKey", 0)

            # 构建 Instrument
            try:
                try:
                    instype = MusicPlayer.insTypeMap.get(main_key, BaseInstrument)
                    instrument = instype(name=name)
                except TypeError:
                    print(f"WARNING: Using BaseInstrument for {name}, while mainkey={main_key}")
                    instrument = BaseInstrument(name)
            except AttributeError:
                # 若没有 Instrument 类型，尝试 BaseInstrument
                print(f"WARNING: Using BaseInstrument for {name}")
                try:
                    try:
                        instrument = BaseInstrument(name=name)
                    except TypeError:
                        instrument = BaseInstrument(name)
                except Exception as e:
                    print(f"Error constructing Instrument: {e}")
                    return None

            # 填充 Note
            if not hasattr(instrument, "notes") or not isinstance(getattr(instrument, "notes"), list):
                setattr(instrument, "notes", [])
            for n in notes_info:
                pitch = n.get("pitch")
                duration = n.get("duration")
                try:
                    try:
                        note_obj = Note(pitch=pitch, duration=duration)
                    except TypeError:
                        print(f"WARNING: Using default Note constructor for pitch={pitch}, duration={duration}")
                        note_obj = Note(pitch, duration)
                    instrument.notes.append(note_obj)
                except Exception as e:
                    print(f"Error constructing Note: {e}")
                    return None

            # 构建 Track 并加入 song
            try:
                try:
                    track = Song.Track(instrument=instrument)
                except TypeError:
                    track = Song.Track(instrument)
            except Exception as e:
                print(f"Error constructing Track: {e}")
                return None

            if use_add_track:
                song.add_track(track)
            else:
                song.tracks.append(track)

        print(f"Song loaded from {filename}")
        return song

