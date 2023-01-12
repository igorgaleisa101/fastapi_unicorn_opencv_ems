import base64
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

def findCoord(backImage, slideImage):

    # backImage = backImage.resize((backImage.width // 2, backImage.height // 2))
    # slideImage = slideImage.resize((slideImage.width // 2, slideImage.height // 2))
    # Identify the edge of the image
    bg_edge = cv2.Canny(np.asarray(backImage), 100, 200)
    tp_edge = cv2.Canny(np.asarray(slideImage), 100, 200)

    # Change the image format
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # Looking for the best match

    x = max_loc[0]

    # # Draw a box
    # th, tw = tp_pic.shape[:2]
    # tl = max_loc # The coordinates of the upper left corner
    # br = (tl[0]+tw,tl[1]+th) # The coordinates of the lower right corner
    # cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2) # Draw a rectangle
    # cv2.imwrite('out.jpg', bg_img) # Keep it locally

    return x

if __name__ == '__main__':
    slidingImage = Image.open('s.png')
    backImage = Image.open('b.png')
    print(findCoord(backImage, slidingImage))