from PIL import Image
from PIL import ImageColor
import sys
import os

import transformHandles


def hex2rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0,2,4))


def rgb2hex(col):
    return '#{:02x}{:02x}{:02x}'.format(col[0], col[1], col[2])


def main():
    #print("Argv length : " + str(len(sys.argv)))
    img = Image.open("grid_samples/im1.png")
    hex_col = "E30613"
    col = [227, 6, 19]
    
    transformHandles.get_markers_by_color(img, col, 50, tolerance=40)




if __name__ == '__main__':
    main()