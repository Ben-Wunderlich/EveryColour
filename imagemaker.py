import numpy as np
import copy
from imageio import imwrite
import random
import string
import os.path as op
from os import remove, rename, mkdir
from PIL import Image
from pathvalidate import sanitize_filename

#a 3 by 3 canvas looks like [[(-1, -1, -1), (-1, -1, -1), (-1, -1, -1)], [(-1, -1, -1), (-1, -1, -1), (-1, -1, -1)], [(-1, -1, -1), (-1, -1, -1), (-1, -1, -1)]]
def MakeCanvas(x, y):
    arr = []
    for _ in range(x):
        arr.append([])
        for _ in range(y):
            arr[-1].append((-1,-1,-1))
    return arr


def DefaultName(size=10):  
    options = string.ascii_lowercase + string.digits + string.ascii_uppercase
    return ''.join([random.choice(options)for n in range(size)]) 

def GetSaveName(defaultName):
    inp = input("enter new name or press enter or press enter to save as {}\n".format(defaultName))
    if inp == "":
        inp = defaultName

    while NameIsTaken(MakeNameProper(inp)):
        inp = input("'{}' is taken, enter new name or press enter to save as {}\n".format(inp,defaultName))
        inp = sanitize_filename(inp)
        if inp == "":
            inp = defaultName

    print("saving image '{}'...\n".format(inp))
    return MakeNameProper(inp)

def MakeNameProper(fileName):
    return "results\\{}.png".format(fileName)


def NameIsTaken(fullPathName):
    return op.exists(fullPathName)

def CanvasToPixels(canvas):
    nuCanvas = copy.deepcopy(canvas)

    for x, line in enumerate(canvas):
        for y, element in enumerate(line):
            if element:
                nuCanvas[x][y]=[255, 255, 255]
            else:
                nuCanvas[x][y]=[0, 0, 0]
    return nuCanvas

def FormImage(canvas, ask=True):
    #canvas = CanvasToPixels(canvas)
    npCanvas = np.asarray(canvas)

    if not op.exists("results"):
        mkdir("results")

    #this is here because I visualized my array differently than the people who made the modules
    npCanvas = np.swapaxes(npCanvas,0,1)

    img = npCanvas.astype(np.uint8)
    fileName = MakeNameProper(DefaultName())
    
    imwrite(fileName, img)
    print("image created")
    print("\n opening image...")
    #open image
    im = Image.open(fileName)  
    im.show()
    if(ask):
        inp = input("type 'del' to delete that image or 're' to rename it: ")
    else:
        inp = "keep"
    if inp.lower() == "del":
        remove(fileName)
        print("file deleted")
    else:
        print("image kept")
    if inp.lower() == "re":
        newName = GetSaveName(fileName)
        rename(fileName, newName)


