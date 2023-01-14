import base64
import cv2
import numpy as np
from PIL import Image
from io import BytesIO


def find_coordinates(backImage, slideImage):
    bg_edge = cv2.Canny(np.asarray(backImage), 100, 200)
    tp_edge = cv2.Canny(np.asarray(slideImage), 100, 200)

    # Change the image format
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # Looking for the best match
    return max_loc[0]


if __name__ == '__main__':
    slidingImage = Image.open('s.png')
    backImage = Image.open('b.png')
    print(find_coordinates(backImage, slidingImage))
