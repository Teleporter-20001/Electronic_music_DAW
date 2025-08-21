from app.backend.Models.Song import Song
import sounddevice as sd
import soundfile as sf
import time
import os
import numpy as np

class MusicPlayer:
    
    def __init__(self):
        pass

    def play_song(self, song: Song):
        print(f"Playing song: {song.title}")

        mixed_waveform = song.generate_mixed_waveform()
        if len(mixed_waveform) == 0:
            print("No tracks to play.")
            return

        self.play_single_waveform(mixed_waveform, song.sample_rate)
                
                
    def save_song_waveform(self, song: Song, filename: str):
        """将歌曲的波形保存为音频文件"""
        mixed_waveform = song.generate_mixed_waveform()
        if len(mixed_waveform) == 0:
            print("No tracks to save.")
            return
        
        try:
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
            sf.write(filename, mixed_waveform, samplerate=song.sample_rate)
            print(f"Waveform saved to {filename}")
        except Exception as e:
            print(f"Error saving waveform: {e}")
            
            
    def play_single_waveform(self, wave: np.ndarray, sample_rate: int):

        try:
            sd.play(wave, samplerate=sample_rate)
            while sd.get_stream().active:
                time.sleep(0.1)
        except KeyboardInterrupt:
            sd.stop()
            print("Playback stopped by user.")
        except Exception as e:
            print(f"Error occurred during playback: {e}")
            sd.stop()
            raise
        finally:
            if sd.get_stream().active:
                sd.stop()
                print("Playback finished.")