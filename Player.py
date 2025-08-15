import Page
import threading
import sounddevice as sd
import soundfile as sf
import time
import os

class MusicPlayer:
    def __init__(self, speed: int, beat_num_per_bar: int = 4, beat_unit: int = 4):
        self.speed = speed
        self.beat_num_per_bar = beat_num_per_bar
        self.beat_unit = beat_unit
        
    
    def play_page(self, page: Page. Song):
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
                
                
    def save_page_waveform(self, page: Page. Song, filename: str):
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
