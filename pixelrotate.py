import imagemaker as im
from PIL import Image
from random import randint

#rotate pixel till highest is blue

def RotateAll(canvas, reverse=False):
    for i in range(len(canvas)):
        for j in range(len(canvas[0])):
            canvas[i][j] = rotateOnce(canvas[i][j], reverse)

def RandRotateAll(canvas):
    for i in range(len(canvas)):
        for j in range(len(canvas[0])):
            if(randint(0,1)==0):
                canvas[i][j] = rotateOnce(canvas[i][j], True)
            else:
                canvas[i][j] = rotateOnce(canvas[i][j], False)

def rotateOnce(pixel, reverse):
    if reverse:
        newPix = (pixel[2], pixel[0], pixel[1])
    else:
        newPix = (pixel[1], pixel[2], pixel[0])
    return newPix


#for pixel max 0=red, 1=green, 2=blue
def RotateMax(canvas, pixelMax):
    for i in range(len(canvas)):
        for j in range(len(canvas[0])):
            currPix = canvas[i][j]
            while currPix[pixelMax] < currPix[(pixelMax+1)%3] or currPix[pixelMax] < currPix[(pixelMax+2)%3]:
                currPix = rotateOnce(currPix, False)
            
            canvas[i][j]=currPix

def AddRotate(pixel, amountToAdd):
    newPix = ((pixel[0]+amountToAdd)%256, (pixel[1]+amountToAdd)%256, (pixel[2]+amountToAdd)%256)
    return newPix

def AddRotateAll(canvas , amountToAdd = 60):
    for i in range(len(canvas)):
        for j in range(len(canvas[0])):
            canvas[i][j] = AddRotate(canvas[i][j], amountToAdd)

def ValueRotate(pixel, part):
    addPt = pixel[part]
    newPix = ((pixel[0]+addPt)%256, (pixel[1]+addPt)%256, (pixel[2]+addPt)%256)
    return newPix

#for part 0=red, 1=green, 2=blue
def ValueAddRotateAll(canvas, part=0):
    for i in range(len(canvas)):
        for j in range(len(canvas[0])):
            canvas[i][j] = ValueRotate(canvas[i][j], part)

def ParseFile(fileName):
    img = Image.open(fileName, 'r') # Can be many different formats
    pix = img.load()
    width, height = img.size
    img.close()

    canvas = im.MakeCanvas(width, height)
    for i in range(width):
        for j in range(height):
            canvas[i][j]=pix[i,j]
    
    return canvas

def main():
    canvas = ParseFile("bases\\hellovader.jpg")
    RotateAll(canvas, True)
    #RotateMax(canvas, 2)
    #RandRotateAll(canvas)

    #AddRotateAll(canvas)
    #ValueAddRotateAll(canvas, 2)

    im.FormImage(canvas)

main()