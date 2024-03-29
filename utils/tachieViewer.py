import os
import random
# if __name__ == '__main__':
#     from fire_and_forget import fire_and_forget
# else:
#     from utils.fire_and_forget import fire_and_forget
import sys
import time
from pathlib import Path

import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# 標準出力のエンコードをUTF-8に変更する
import io

from utils.fire_and_forget import fire_and_forget

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from utils.FlactuateImage import FlactuateImage


class TachieViewer:
    def __init__(self, imagesDirPath: Path, windowName: str = 'TachieViewer'):
        self.getImages(imagesDirPath)
        self.image = self.closed_mouth_open_eye_image
        self.is_mouth_open = False
        self.is_eye_open = False
        self.windowName = windowName
        self.flactuateImage = FlactuateImage()
        self.closeFlag = False

    
    def getImages(self, imagesDirPath: Path):
        self.open_mouth_open_eye_image = cv2.imdecode(np.fromfile(str(imagesDirPath / 'om_oe.png'), dtype=np.uint8), cv2.IMREAD_UNCHANGED)[:,:,:3]
        self.closed_mouth_open_eye_image = cv2.imdecode(np.fromfile(str(imagesDirPath / 'cm_oe.png'), dtype=np.uint8), cv2.IMREAD_UNCHANGED)[:,:,:3]
        self.open_mouth_closed_eye_image = cv2.imdecode(np.fromfile(str(imagesDirPath / 'om_ce.png'), dtype=np.uint8), cv2.IMREAD_UNCHANGED)[:,:,:3]
        self.closed_mouth_closed_eye_image = cv2.imdecode(np.fromfile(str(imagesDirPath / 'cm_ce.png'), dtype=np.uint8), cv2.IMREAD_UNCHANGED)[:,:,:3]

        
    def setRandomBlinkFlag(self):
        # 乱数(1~100)で90以上なら目を閉じる
        randomNum = random.randint(1, 1000)
        if randomNum >= 920:
            self.is_eye_open = False
        else:
            self.is_eye_open = True
        
    def setMouthOpenFlag(self, DB: float, threshold: float = 57):
        if DB >= threshold:
            self.is_mouth_open = True
        else:
            self.is_mouth_open = False

    def selectImage(self):
        if self.is_mouth_open and self.is_eye_open:
            self.image = self.open_mouth_open_eye_image
        elif self.is_mouth_open and not self.is_eye_open:
            self.image = self.open_mouth_closed_eye_image
        elif not self.is_mouth_open and self.is_eye_open:
            self.image = self.closed_mouth_open_eye_image
        elif not self.is_mouth_open and not self.is_eye_open:
            self.image = self.closed_mouth_closed_eye_image

    def close(self):
        self.closeFlag = True
        
    @fire_and_forget
    def play(self):
        while True:
            key = cv2.waitKey(30)
            self.setRandomBlinkFlag()
            self.selectImage()
            
            # 画像の座標を拡張し、フレームごとに座標をずらす。
            flactImage = self.flactuateImage.getImg(self.image)
            
            # Draw character
            cv2.imshow(self.windowName, flactImage)
            
            if key == 27 or key == ord('q') :
                cv2.destroyAllWindows()
                break
            
            if self.closeFlag == True:
                cv2.destroyAllWindows()
                break


def main():
    # imagesDirPath = Path('characterConfig/test/images')
    imagesDirPath = Path('characterConfig/りおん/images')
    tachieViewer = TachieViewer(imagesDirPath)
    tachieViewer.play()

    while True:
        db = random.randint(1, 60)
        tachieViewer.setMouthOpenFlag(db, 50)
        # print(tachieViewer.is_mouth_open, tachieViewer.is_eye_open)


if __name__ == '__main__':
    main()