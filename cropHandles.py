import PIL
import sys
import os


def crop_n_save(img, crop_dim, offset = (0, 0), full_cell = True):
    """
    Description
    -----------
    Crops the image cell by cell, according to the dimensions passed in.

    Parameters
    ----------
    img : Image
        The image of the grid you want to crop cells from.

    crop_dim : tuple(int, int)
        Size of the cells to crop from the image.

    offset : tuple(int, int), optionnal
        Let the function slighlty offset each cut. No offset by default, cells are right next to each other.

    full_cell : bool, optionnal
        Tells the function if it can cut a cell when there is not enough room for it (when it reaches the end of the image).
    """
    x, y = img



    return 0





