from PIL import Image
import sys
import os


def importImage(path):
    image = Image.open(path)
    return image


def showImage(im):
    im.show()


def saveImage(im, path):
    im.save(path)





def main():
    print("Argv length : " + str(len(sys.argv)))



if __name__ == '__main__':
    main()