import cv2
import numpy as np

#フレームごとに画像を正弦波にしたがって上下させる。
class FlactuateImage():
    def __init__(self):     
        self.resize_amplitude = 30
        self.resize_frequency = 1/(30*4)
        self.resize_flame = 0
        
    
    def continuousResize(self, orig_img):
        # 100px大きく画像をリサイズする
        img = cv2.resize(orig_img, (orig_img.shape[1] + 600, orig_img.shape[0] + 600))
        
        # 0~100の間の正弦波を計算する
        crop_px = self.resize_amplitude * (np.sin(2 * np.pi * self.resize_frequency * self.resize_flame) + 1)/2
        self.resize_flame += 1
        
        img = img[int(crop_px):int(img.shape[0]), int(crop_px/2):int(img.shape[1] - crop_px/2)]
        
        img = cv2.resize(img, (orig_img.shape[1], orig_img.shape[0]))
        return img
    
    def getImg(self, orig_img, window_size=680, window_color=(0, 255, 0)):
        # 緑色の画像を作成する
        img = 255 * np.ones((window_size, window_size, 3), dtype=np.uint8)
        img[:, :] = window_color


        # 画像の中心座標を計算する
        center_x = int(img.shape[1] / 2)
        center_y = int(img.shape[0] / 2)


        # 画像を中心に表示するための座標を計算する
        top_y = int(center_y - orig_img.shape[0] / 2)
        bottom_y = top_y + orig_img.shape[0] 
        left_x = int(center_x - orig_img.shape[1] / 2)
        right_x = left_x + orig_img.shape[1]
        
        
        # 画像を中心に表示する
        img[-int(orig_img.shape[0]+1):-1, left_x:right_x] = orig_img
        
        # 連続的に画像をリサイズする
        img = self.continuousResize(img)
        
        return img


def main():
    flactuateImage = FlactuateImage()

    opened_img = cv2.imread("opened.png")
    while True:
        img = flactuateImage.getImg(opened_img)
        cv2.imshow("Green window", img)
        cv2.waitKey(30)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()