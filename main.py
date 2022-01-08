from PIL import Image
from PIL import ImageColor
import sys
import os
import math

from PyQt5 import QtWidgets

import transformHandles
import cropHandles
import qtHandles


def hex2rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0,2,4))


def rgb2hex(col):
    return '#{:02x}{:02x}{:02x}'.format(col[0], col[1], col[2])


def main():
    #print("Argv length : " + str(len(sys.argv)))
    img = Image.open("grid_samples/im1.png") # default image, slighlty tilted
    img2 = Image.open("grid_samples/im2.png") # 0.5° tilted
    img3 = Image.open("grid_samples/im3.png") # 12,8° tilted
    img4 = Image.open("grid_samples/im4.png") # 12,8° tilted, thick marks
    img5 = Image.open("grid_samples/im5.png") # 3° tilted

    hex_col = "E30613"
    col = [227, 6, 19]
    """
        top_mark, bottom_mark = transformHandles.getMarkersByColor(img5, col, 250, tolerance=40)


    new_img = transformHandles.adjustTransforms(img5, top_mark, bottom_mark)
    new_top_mark, new_bottom_mark = transformHandles.getMarkersByColor(new_img, col, 50, tolerance=40)
        
    new_img.show()
    new_img.save("grid_samples/res1.png")

    img6 = Image.open("grid_samples/res1.png") # check for alpha

    new_img6 = cropHandles.crop_transparency(img6)
    new_img6.save("grid_samples/res2.png")
    #new_img6.show()

    top_mark5, bottom_mark5 = transformHandles.getMarkersByColor(img5, col, 250, tolerance=40)
    img5 = transformHandles.adjustTransforms(img5, top_mark5, bottom_mark5)
    new_img5 = cropHandles.cropTransparency(img5)
    #new_img5.show()
    cropHandles.cropNSave(new_img5, (50, 50))


    img7 = Image.open("grid_samples/im7.png")
    img7_w = Image.open("grid_samples/im7_w.png")
    top_mark7_w, bottom_mark7_w = transformHandles.getMarkersByColor(img7_w, col, 250, tolerance=40)
    img7_w = transformHandles.adjustTransforms(img7_w, top_mark7_w, bottom_mark7_w)
    img7_w.save("grid_samples/res3.png")
    new_img7_w = cropHandles.cropByColor(img7_w, col, tolerance=40)
    new_img7_w.save("grid_samples/res4.png")
    cropHandles.cropNSave(new_img7_w, (49, 49), offset=(1,1), full_cell=False)

    img8_w = Image.open("grid_samples/im8_w.png")
    top_mark8_w, bottom_mark8_w = transformHandles.getMarkersByColor(img8_w, col, 250, tolerance=40)
    img8_w = transformHandles.adjustTransforms(img8_w, top_mark8_w, bottom_mark8_w)
    img8_w.save("grid_samples/res3.png")
    new_img8_w = cropHandles.cropByColor(img8_w, col, tolerance=40)
    new_img8_w.save("grid_samples/res4.png")
    cropHandles.cropNSave(new_img8_w, (48, 48), offset=(3,2), full_cell=False, nom="test")"""

    
    # create pyqt5 app 
    App = QtWidgets.QApplication(sys.argv)

    # create the instance of our Window 
    window = qtHandles.GridWindow() 
    
    # start the app 
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()