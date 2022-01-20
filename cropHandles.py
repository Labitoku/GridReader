import PIL
import sys
import os
import colorHandles

def cropTransparency(img):
    """
    Description
    -----------
    Crops the image's transparent borders.

    Parameters
    ----------
    img : Image
        The image you want to crop the transparency from.

    """

    x, y = img.size
    left = 0
    top = 0
    right = 0
    bottom = 0

    #LEFT
    for i in range(0, x):
        for j in range(0, y):
            if img.getpixel((i, j))[3] != 0:
                left = i
                break
        else:
            continue        # only executed if the inner loop did NOT break
        break               # only executed if the inner loop DID break

    #TOP
    for i in range(0, y):
        for j in range(0, x):
            if img.getpixel((j, i))[3] != 0:
                top = i
                break
        else:
            continue  
        break  

    #RIGHT
    for i in reversed(range(0, x)):
        for j in range(0, y):
            if img.getpixel((i, j))[3] != 0:
                right = i
                break
        else:
            continue
        break

    #BOTTOM
    for i in reversed(range(0, y)):
        for j in range(0, x):
            if img.getpixel((j, i))[3] != 0:
                bottom = i
                break
        else:
            continue  
        break 

    print(top, left, bottom, right)

    cropped_img = img.crop((left, top, right, bottom))
    return cropped_img


def getTransparencyMarks(img):
    """
    Description
    -----------
    Returns the image dimensions without transparency.

    Parameters
    ----------
    img : Image
        The image you want to crop the transparency from.

    """

    x, y = img.size
    left = 0
    top = 0
    right = 0
    bottom = 0

    #LEFT
    for i in range(0, x):
        for j in range(0, y):
            if img.getpixel((i, j))[3] != 0:
                left = i
                break
        else:
            continue        # only executed if the inner loop did NOT break
        break               # only executed if the inner loop DID break

    #TOP
    for i in range(0, y):
        for j in range(0, x):
            if img.getpixel((j, i))[3] != 0:
                top = i
                break
        else:
            continue  
        break  

    #RIGHT
    for i in reversed(range(0, x)):
        for j in range(0, y):
            if img.getpixel((i, j))[3] != 0:
                right = i
                break
        else:
            continue
        break

    #BOTTOM
    for i in reversed(range(0, y)):
        for j in range(0, x):
            if img.getpixel((j, i))[3] != 0:
                bottom = i
                break
        else:
            continue  
        break 

    return left, top, right, bottom

def cropByColor(img, color2crop, tolerance = 0):
    """
    Description
    -----------
    TO DO

    Parameters
    ----------
    img : Image
        The image you want to crop, until the colour is found.
    
    color2crop : array of int [r,g,b]
        The color to crop by.

    tolerance : int, optionnal
        Used to reduce the accuracy of the spotting. Default 0 means it has to be the exact same color.
    """

    x, y = img.size
    left = 0
    top = 0
    right = 0
    bottom = 0


    #LEFT
    for i in range(0, x):
        for j in range(0, y):
            if colorHandles.getTolerance(color2crop, img.getpixel((i, j)), tolerance):
                left = i
                break
        else:
            continue        # only executed if the inner loop did NOT break
        break               # only executed if the inner loop DID break

    #TOP
    for i in range(0, y):
        for j in range(0, x):
            if colorHandles.getTolerance(color2crop, img.getpixel((j, i)), tolerance):
                top = i
                break
        else:
            continue  
        break  

    #RIGHT
    for i in reversed(range(0, x)):
        for j in range(0, y):
            if colorHandles.getTolerance(color2crop, img.getpixel((i, j)), tolerance):
                right = i
                break
        else:
            continue
        break

    #BOTTOM
    for i in reversed(range(0, y)):
        for j in range(0, x):
            if colorHandles.getTolerance(color2crop, img.getpixel((j, i)), tolerance):
                bottom = i
                break
        else:
            continue  
        break 


    print(top, left, bottom, right)

    cropped_img = img.crop((left, top, right, bottom))
    return cropped_img


def getColorMarks(img, color2crop, tolerance = 0):    
    """
    Description
    -----------
    TO DO 

    Parameters
    ----------
    img : Image
        The image you want to crop, until the colour is found.
    
    color2crop : array of int [r,g,b]
        The color to crop by.

    tolerance : int, optionnal
        Used to reduce the accuracy of the spotting. Default 0 means it has to be the exact same color.
    """

    x, y = img.size
    left = 0
    top = 0
    right = 0
    bottom = 0


    #LEFT
    for i in range(0, x):
        for j in range(0, y):
            if colorHandles.getTolerance(color2crop, img.getpixel((i, j)), tolerance):
                left = i
                break
        else:
            continue        # only executed if the inner loop did NOT break
        break               # only executed if the inner loop DID break

    #TOP
    for i in range(0, y):
        for j in range(0, x):
            if colorHandles.getTolerance(color2crop, img.getpixel((j, i)), tolerance):
                top = i
                break
        else:
            continue  
        break  

    #RIGHT
    for i in reversed(range(0, x)):
        for j in range(0, y):
            if colorHandles.getTolerance(color2crop, img.getpixel((i, j)), tolerance):
                right = i
                break
        else:
            continue
        break

    #BOTTOM
    for i in reversed(range(0, y)):
        for j in range(0, x):
            if colorHandles.getTolerance(color2crop, img.getpixel((j, i)), tolerance):
                bottom = i
                break
        else:
            continue  
        break 


    return left, top, right, bottom
    
def cropByMarks(img, left, top, right, bottom):
    cropped_img = img.crop((left, top, right, bottom))
    return cropped_img



def getCellsQty(img, crop_dim, offset = (0, 0), full_cell = True):
    x, y = img.size

    
    cell_qty_x = int(x / crop_dim[0])
    cell_qty_y = int(y / crop_dim[1])

    x = x - cell_qty_x * offset[0]
    y = y - cell_qty_y * offset[1]

    cell_qty_x = int(x / crop_dim[0])
    cell_qty_y = int(y / crop_dim[1])

    if full_cell:
        if x % crop_dim[0] != 0:
            cell_qty_x -= 1

        if y % crop_dim[1] != 0:
            cell_qty_y -= 1

    return cell_qty_x, cell_qty_y



def cropNSave(img, crop_pos, crop_dim, cell_qty_x, cell_qty_y, offset = (0, 0), full_cell = True, name="img"):
    """
    Description
    -----------
    Crops the image cell by cell, and saves each of them.

    Parameters
    ----------
    img : Image
        The image of the grid you want to crop cells from.

    crop_pos : tuple(int, int)
        Position to move from one cell to another.

    crop_dim : tuple(int, int)
        Size of the cells to crop from the image. If cells are strictly next to each other, set crop_dim to crop_pos.

    offset : tuple(int, int), optionnal
        Let the function slighlty offset each cut. No offset by default, cells are right next to each other.

    full_cell : bool, optionnal
        Tells the function if it can cut a cell when there is not enough room for it (when it reaches the end of the image).
    """
    #cell_qty_x, cell_qty_y = getCellsQty(img, crop_dim, offset, full_cell)

    """x0 = i * pos_cell[0] + self.offset_cell[0] 
    y0 = j * pos_cell[1] + self.offset_cell[1] 
    x1 = x0 + self.size_cell[0] 
    y1 = y0 + self.size_cell[1]"""

    for i in range(0, cell_qty_x):
        left = i * crop_pos[0] + offset[0]
        right = left + crop_dim[0]

        for j in range(0, cell_qty_y):
            top = j * crop_pos[1] + offset[1]
            bottom = top + crop_dim[1]


            new_img = img.crop((left, top, right, bottom))
            #new_img.save(f"grid_samples/resCrops/{name}_{i}_{j}.png")
            new_img.save(f"{name}_{i}_{j}.png")

    return 0


