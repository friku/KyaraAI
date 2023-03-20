import os
import pdb
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.fire_and_forget import fire_and_forget
from utils.wavePlayerWithVolume import WavPlayerWithVolume


class FIFOPlayer:
    def __init__(self) -> None:
        self.queue = []
        self.is_open = True
    
    def setObject(self, obj: object) -> None:
        self.queue.append(obj)
    
    def close(self) -> None:
        self.is_open = False
        
    def get_file_queue_length(self) -> int:
        return len(self.queue)
        
    
    @fire_and_forget
    def playWithFIFO(self):
        while True:
            if len(self.queue) > 0:
                obj = self.queue.pop(0)
                obj.play()
            else:
                time.sleep(1)
            if self.is_open == False:
                break
                


def main():
    try:
        fifoPlayer = FIFOPlayer()
        fifoPlayer.playWithFIFO()
        

        for i in range(1,5):
            fifoPlayer.setObject(WavPlayerWithVolume(f'sampleData/test{i}.wav'))
            time.sleep(1)
        
        while True:
            print("main loop")
            time.sleep(1)
            
    except KeyboardInterrupt:
        fifoPlayer.close()
        

if __name__ == '__main__':
    main()
    
    
    
