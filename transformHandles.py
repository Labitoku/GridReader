from PIL import Image
from PIL import ImageColor
import math
import sys
import os
import colorHandles



def get_markers_by_color(img: Image, color2mark, approximation_area_size, tolerance = 0):
    """
    Description
    -----------
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
    top_mark = (x, y)
    bottom_mark = (x, y)

    approx_top_start = (0, 0)
    approx_top_end = (0, 0)
    approx_bottom_start = (0, 0)
    approx_bottom_end = (0, 0)
    
    for i in range(0, approximation_area_size):
        for j in range(0, approximation_area_size):
            if colorHandles.get_tolerance(color2mark, img.getpixel((j, i)), tolerance) and j < top_mark[0]:
                top_mark = (j, i)
                approx_top_start = (j - approximation_area_size, i - approximation_area_size)
                approx_top_end = (approx_top_start[0] + 2 * approximation_area_size, approx_top_start[1] + 2 * approximation_area_size)


    for i in range(y - approximation_area_size, y):
        for j in range(0, approximation_area_size):
            if  colorHandles.get_tolerance(color2mark, img.getpixel((j, i)), tolerance) and j < bottom_mark[0]:
                bottom_mark = (j, i)
                approx_bottom_start = (j - approximation_area_size, i - approximation_area_size)
                approx_bottom_end = (approx_bottom_start[0] + 2 * approximation_area_size, approx_bottom_start[1] + 2 * approximation_area_size)

    print(top_mark, bottom_mark)
    print(img.getpixel(top_mark), img.getpixel(bottom_mark))
    return top_mark, bottom_mark


def adjust_transform(img, top_mark, bottom_mark):
    """
    Description
    -----------
    Rotates the image, based on the two markes passed in parameters.

    Parameters
    ----------
    img : Image
        The image of the grid you want to adjust.

    top_mark : tuple(int, int)
        Coordinates of the top mark on the grid.

    bottom_mark : tuple(int, int)
        Coordinates of the bottom mark on the grid.
    """

    adj = bottom_mark[1] - top_mark[1]
    opp = bottom_mark[0] - top_mark[0]
    h = math.sqrt(adj**2 + opp**2)
    angle = math.acos(adj / h)
    deg_angle = math.degrees(angle)

    #new_img = img.rotate(0 - deg_angle if deg_angle > 0 else deg_angle)
    new_img = img.rotate(0 - deg_angle if deg_angle > 0 else deg_angle, resample=Image.BICUBIC, expand=True)

    print(f"Adj : {adj}\nOpp : {opp}\nHyp : {h}\nAngle (radians) : {angle}\nAngle (degrés) : {deg_angle}")

    return new_img


def get_markers_alignment(top_mark, bottom_mark):
    return top_mark[0] == bottom_mark[0]
