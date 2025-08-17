from Song import Song
import sounddevice as sd
import soundfile as sf
import time
import os

class MusicPlayer:
    
    def __init__(self):
        pass

    def playSong(self, song: Song):
        print(f"Playing song: {song.title}")

        mixed_waveform = song.generate_mixed_waveform()
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
                
                
    def save_song_waveform(self, song: Song, filename: str):
        """将歌曲的波形保存为音频文件"""
        mixed_waveform = song.generate_mixed_waveform()
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
            
            
