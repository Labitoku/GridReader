from PIL import Image
from PIL import ImageColor

import sys
import os



def get_tolerance(source_color, check_color, tolerance = 0):



    check_new_format = [check_color[0], check_color[1], check_color[2]]

    if check_new_format[0] in range(source_color[0] - tolerance, source_color[0] + tolerance):
        if check_new_format[1] in range(source_color[1] - tolerance, source_color[1] + tolerance):
            if check_new_format[2] in range(source_color[2] - tolerance, source_color[2] + tolerance):
                print(source_color, check_new_format)
                return True

    return False

    #return check_new_format[0] < source_color[0] - tolerance or check_new_format[0] > source_color[0] + tolerance or check_new_format[1] < source_color[1] - tolerance or check_new_format[1] > source_color[1] + tolerance or check_new_format[2] < source_color[2] - tolerance or check_new_format[2] > source_color[2] + tolerance

    """if check_new_format[0] > 150 and check_new_format[1] < 100 and  check_new_format[2] < 100:
        print(check_new_format)

    return source_color == check_new_format"""



def get_markers_by_color(img: Image, color2mark, approximation_area_size, tolerance = 0):
    """
    Detects markers on the grid, and returns the leftest point for each of them.

    Parameters
    ----------
    img : Image
        The image of the grid you want to process.

    color2mark : array of int [r, g, b]
        The color to spot on the grid.

    approximation_area_size : int
        Used to inspect specific areas instead of all the image. 
        Basically, indicates the dimensions of the two left corners for the function to search markers.

    tolerance : int, optionnal
        Used to reduce the accuracy of the spotting. Default 0 means it has to be the exact same color.
    """


    x, y = img.size
    print(x, y)


    top_mark = (x, y)
    bottom_mark = (x, y)

    approx_top_start = (0, 0)
    approx_top_end = (0, 0)
    approx_bottom_start = (0, 0)
    approx_bottom_end = (0, 0)
    
    for i in range(0, approximation_area_size):
        for j in range(0, 200):
            if get_tolerance(color2mark, img.getpixel((j, i)), tolerance) and j < top_mark[0]:
                top_mark = (i, j)
                approx_top_start = (i - approximation_area_size, j - approximation_area_size)
                approx_top_end = (approx_top_start[0] + 2 * approximation_area_size, approx_top_start[1] + 2 * approximation_area_size)


    for i in range(y - approximation_area_size, y):
        for j in range(0, approximation_area_size):
            if  get_tolerance(color2mark, img.getpixel((j, i)), tolerance) and j < bottom_mark[0]:
                bottom_mark = (i, j)
                approx_bottom_start = (i - approximation_area_size, j - approximation_area_size)
                approx_bottom_end = (approx_bottom_start[0] + 2 * approximation_area_size, approx_bottom_start[1] + 2 * approximation_area_size)

    print(top_mark, bottom_mark)
    return top_mark, bottom_mark

