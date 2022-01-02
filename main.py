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
    
    img05 = Image.open("grid_samples/im1_0,5dg.png")
    hex_col = "E30613"
    col = [227, 6, 19]
    
    top_mark, bottom_mark = transformHandles.get_markers_by_color(img, col, 50, tolerance=40)


    new_img = transformHandles.adjust_transform(img, top_mark, bottom_mark)
    new_top_mark, new_bottom_mark = transformHandles.get_markers_by_color(new_img, col, 50, tolerance=40)

    while not transformHandles.get_markers_alignment(new_top_mark, new_bottom_mark):
        
        new_img = transformHandles.adjust_transform(img, top_mark, bottom_mark)
        new_top_mark, new_bottom_mark = transformHandles.get_markers_by_color(new_img, col, 50, tolerance=40)
        print(new_top_mark, new_bottom_mark)
        print(transformHandles.get_markers_alignment(new_top_mark, new_bottom_mark))

    
    
    new_img.show()
    new_img.save("grid_samples/res1.png")





if __name__ == '__main__':
    main()