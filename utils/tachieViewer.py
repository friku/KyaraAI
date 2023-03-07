import sys
from pathlib import Path
import random
import time
import cv2
if __name__ == '__main__':
    from fire_and_forget import fire_and_forget
else:
    from utils.fire_and_forget import fire_and_forget

class TachieViewer:
    def __init__(self, imagesDirPath: Path):
        self.getImages(imagesDirPath)
        self.image = self.closed_mouth_open_eye_image
        self.is_mouth_open = False
        self.is_eye_open = False

        
    
    def getImages(self, imagesDirPath: Path):
        self.open_mouth_open_eye_image = cv2.imread(str(imagesDirPath / 'om_oe.png'))
        self.closed_mouth_open_eye_image = cv2.imread(str(imagesDirPath / 'cm_oe.png'))
        self.open_mouth_closed_eye_image = cv2.imread(str(imagesDirPath / 'om_ce.png'))
        self.closed_mouth_closed_eye_image = cv2.imread(str(imagesDirPath / 'cm_ce.png'))

        
    def setRandomBlinkFlag(self):
        # 乱数(1~100)で90以上なら目を閉じる
        randomNum = random.randint(1, 1000)
        if randomNum >= 990:
            self.is_eye_open = False
        else:
            self.is_eye_open = True
        
    def setMouthOpenFlag(self, DB: float, threshold: float = 50):
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

        
    @fire_and_forget
    def play(self):
        while True:
            key = cv2.waitKey(30)
            self.setRandomBlinkFlag()
            self.selectImage()
            
            # Draw character
            cv2.imshow('image', self.image)
            
            if key == 27 or key == ord('q') :
                cv2.destroyAllWindows()
                break


def main():
    imagesDirPath = Path('characterConfig/test/images')
    tachieViewer = TachieViewer(imagesDirPath)
    tachieViewer.play()

    while True:
        db = random.randint(1, 60)
        tachieViewer.setMouthOpenFlag(db, 50)
        print(tachieViewer.is_mouth_open, tachieViewer.is_eye_open)


if __name__ == '__main__':
    main()