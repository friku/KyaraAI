import pygame
import sys
from pathlib import Path
import random
import time
if __name__ == '__main__':
    from fire_and_forget import fire_and_forget
else:
    from utils.fire_and_forget import fire_and_forget

class TachieViewer:
    def __init__(self, imagesDirPath: Path):
        self.pygameInit()
        self.getImages(imagesDirPath)
        self.image = self.closed_mouth_open_eye_image
        self.is_mouth_open = False
        self.is_eye_open = False
        
    
    def getImages(self, imagesDirPath: Path):
        self.open_mouth_open_eye_image = pygame.image.load(imagesDirPath / 'om_oe.png').convert_alpha()
        self.closed_mouth_open_eye_image = pygame.image.load(imagesDirPath / 'cm_oe.png').convert_alpha()
        self.open_mouth_closed_eye_image = pygame.image.load(imagesDirPath / 'om_ce.png').convert_alpha()
        self.closed_mouth_closed_eye_image = pygame.image.load(imagesDirPath / 'cm_ce.png').convert_alpha()
        
    def pygameInit(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 640))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Pygame Test')
        
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
        
        
    def draw(self, surface):
        surface.blit(self.image, (0, 0))
        
    @fire_and_forget
    def play(self):
        while True:
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         pygame.quit()
            #         sys.exit()

            self.setRandomBlinkFlag()
            # db = random.randint(1, 60)
            # self.setMouthOpenFlag(db, 50)
            self.selectImage()
            
            # Draw character
            self.draw(self.screen)
            
            # Update screen
            pygame.display.flip()
            self.clock.tick(30)

imagesDirPath = Path('./characterConfig/りおん/images')
tachieViewer = TachieViewer(imagesDirPath)
tachieViewer.play()

while True:
    db = random.randint(1, 60)
    tachieViewer.setMouthOpenFlag(db, 50)
    time.sleep(1)