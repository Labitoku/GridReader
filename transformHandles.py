from PIL import Image
from PIL import ImageColor
import math
import sys
import os



def get_tolerance(source_color, check_color, tolerance = 0):
    check_new_format = [check_color[0], check_color[1], check_color[2]]

    if check_new_format[0] in range(source_color[0] - tolerance, source_color[0] + tolerance):
        if check_new_format[1] in range(source_color[1] - tolerance, source_color[1] + tolerance):
            if check_new_format[2] in range(source_color[2] - tolerance, source_color[2] + tolerance):
                #print(source_color, check_new_format)
                return True

    return False



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
        Used to reduce the accuracy of the spotting. Default 0 means it has to be the exact same color.Ajout 
    """

    x, y = img.size
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


def adjust_transform(img, top_mark, bottom_mark):

    adj = bottom_mark[0] - top_mark[0]
    opp = bottom_mark[1] - top_mark[1]
    h = math.sqrt(adj**2 + opp**2)
    angle = math.cos(adj / h)
    new_img = img.rotate(0 - angle if angle > 0 else angle)

    print("Adj : ", str(adj), "\nOpp : ", str(opp), "\nHyp : ", str(h), "\nAngle : ", str(angle))

    return new_img




def get_markers_alignment(top_mark, bottom_mark):
    return top_mark[1] == bottom_mark[1]
