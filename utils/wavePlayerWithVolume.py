import pyaudio
import wave
import struct
import math
import time
from fire_and_forget import fire_and_forget

class WavPlayerWithVolume:
    def __init__(self, filename):
        self.wav_file = wave.open(filename, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wav_file.getsampwidth()),
                                  channels=self.wav_file.getnchannels(),
                                  rate=self.wav_file.getframerate(),
                                  output=True)
        self.decibel = 0.0
        self.open = False

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    def play(self):
        while True:
            data = self.wav_file.readframes(1024)
            if not data:
                self.open = False
                break
            else:
                self.open = True

            self.stream.write(data)

            rms = 0.0
            count = len(data) / 2
            for i in range(int(count)):
                sample = struct.unpack('<h', data[i*2:i*2+2])[0]
                rms += sample**2
            rms = math.sqrt(rms / count)

            self.decibel = 20 * math.log10(rms)


    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.wav_file.close()

with WavPlayerWithVolume('test.wav') as player:
        player.play()
        while True:
            print(player.decibel)
            if player.open == False:
                break

