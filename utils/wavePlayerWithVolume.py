import pyaudio
import wave
import struct
import math
import time
# from fire_and_forget import fire_and_forget

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.tachieViewer import TachieViewer
from pathlib import Path


class WavPlayerWithVolume:
    '''
    wavファイルを再生するクラス
    再生中にリアルタイムで音量を取得することができる。
    setDecibelFuncが指定されている場合、一定フレームごとにsetDecibelFuncを呼び出す。
    '''
    def __init__(self, wavFilePath, setDecibelFunc=None):
        self.wavFilePath = wavFilePath
        self.setDecibelFunc = setDecibelFunc
        self.decibel = 0.0
        self.open = False

    
    def streamInit(self):
        self.wav_file = wave.open(str(self.wavFilePath.absolute()), 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wav_file.getsampwidth()),
                                  channels=self.wav_file.getnchannels(),
                                  rate=self.wav_file.getframerate(),
                                  output=True)

        
    def setDecibel(self):
        if self.setDecibelFunc != None:
            self.setDecibelFunc(self.decibel)

    def play(self):
        while True:
            try:
                self.streamInit()
                break
            except:
                time.sleep(0.2)
        
        while True:
            data = self.wav_file.readframes(1024)
            if not data:
                self.open = False
                self.decibel = 0.0
                self.close()
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
            
            self.setDecibel()


    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.wav_file.close()



def setDecibel(decibel):
    print(decibel)


def main():
    imagesDirPath = Path('characterConfig/test/images')
    tachieViewer = TachieViewer(imagesDirPath)
    tachieViewer.play()
    
    player = WavPlayerWithVolume('test.wav',tachieViewer.setMouthOpenFlag)
    player.play()

    while True:
        print(player.decibel)
        if player.open == False:
            break


if __name__ == '__main__':
    main()
