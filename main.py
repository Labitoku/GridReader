from PIL import Image
from PIL import ImageColor
import sys
import os
import math

import transformHandles
import cropHandles


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
        top_mark, bottom_mark = transformHandles.get_markers_by_color(img5, col, 250, tolerance=40)


    new_img = transformHandles.adjust_transform(img5, top_mark, bottom_mark)
    new_top_mark, new_bottom_mark = transformHandles.get_markers_by_color(new_img, col, 50, tolerance=40)
        
    new_img.show()
    new_img.save("grid_samples/res1.png")"""

    img6 = Image.open("grid_samples/im6.png") # check for alpha

    new_img6 = cropHandles.crop_transparency(img6)
    new_img6.save("grid_samples/res2.png")
    new_img6.show()

    #cropHandles.crop_n_save(new_img, (50, 50))



    #angle = math.cos(45)
    #print(angle)



if __name__ == '__main__':
    main()