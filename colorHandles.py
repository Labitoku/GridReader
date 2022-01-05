import PIL
import os
import sys


def get_tolerance(source_color, check_color, tolerance = 0):
    """
    Description
    -----------
    Detects markers on the grid, and returns the leftest point for each of them.

    Parameters
    ----------
    source_color : array of int [r, g, b]
        The color to compare with.

    check_color : array of int [r, g, b]
        The color compared with source.

    tolerance : int, optionnal
        Used to reduce the accuracy of the spotting. Default 0 means it has to be the exact same color.
    """
    check_new_format = [check_color[0], check_color[1], check_color[2]]

    if check_new_format[0] in range(source_color[0] - tolerance, source_color[0] + tolerance):
        if check_new_format[1] in range(source_color[1] - tolerance, source_color[1] + tolerance):
            if check_new_format[2] in range(source_color[2] - tolerance, source_color[2] + tolerance):
                #print(source_color, check_new_format)
                return True

    return False