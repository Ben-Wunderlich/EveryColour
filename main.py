from random import randint
import imagemaker as im
from PIL import Image

WIDTH = 800
HEIGHT = 800

START_COLOUR = (200, 200, 200)
START_LOCATIONS = [(randint(0, WIDTH-1), randint(0,HEIGHT-1))]

canvas = im.MakeCanvas(WIDTH, HEIGHT)

#must start out with one partially explored

#if has some value but not all neighbors explored
#this method shaves tome for 1920x1080 image down to around 60secs
partialExplored = dict()
highestInd=0
#each value will have form (x, y) where x and y are position in the image

#takenColours=set()#will only use if it is otherwise uninteresting

#value has form (r,g,b)
def OneDiffPixel(value):
    pixelMod= -8
    if(randint(0,1)==1):
        pixelMod= 8

    pixelPart = randint(0, 2)
    result = None

    if pixelPart==0:
        result= (value[0]+pixelMod, value[1], value[2])
    elif pixelPart==1:
        result= (value[0], value[1]+pixelMod, value[2])
    else:
        result= (value[0], value[1], value[2]+pixelMod)
    
    for part in result:
        if part > 255 or part < 0:
            return OneDiffPixel(value)
    return result    

def ValidToExplore(xLocation, yLocation):
    #if first pixel at location is -1
    if xLocation > WIDTH-1 or xLocation < 0:
        return False
    if yLocation > HEIGHT-1 or yLocation < 0:
        return False

    return canvas[xLocation][yLocation][0] == -1

def NewPixelValue(location):
    currentValue = canvas[location[0]][location[1]]
    newVal = OneDiffPixel(currentValue)
    return newVal

def Explore(xLocation, yLocation, pixelValue):
    AddToDict((xLocation, yLocation))
    canvas[xLocation][yLocation] = pixelValue

def VisitPixel(location, index):
    global highestInd
    newPixel = NewPixelValue(location)

    #check if filled pixel in each direction
    if ValidToExplore(location[0]+1, location[1]):#right
        Explore(location[0]+1, location[1], newPixel)

    elif ValidToExplore(location[0], location[1]-1):#down
        Explore(location[0], location[1]-1, newPixel)

    elif ValidToExplore(location[0]-1, location[1]):#left
        Explore(location[0]-1, location[1], newPixel)

    elif ValidToExplore(location[0], location[1]+1):#up
        Explore(location[0], location[1]+1, newPixel)

    else:#nowhere is valid
        # partialExplored.remove(location)
        partialExplored[index] = partialExplored[highestInd]
        del partialExplored[highestInd]
        highestInd-=1

def CheckDuplicates(canvas):
    distinctCols = set()
    for col in canvas:
        for el in col:
            distinctCols.add(el)
    return (WIDTH*HEIGHT) - len(distinctCols)


def AddToDict(el):
    global highestInd
    highestInd = len(partialExplored)
    partialExplored[highestInd] = el

def RGBify(pixel):
    if len(pixel) == 3:
        return pixel
    else:#is in rgba
        return (pixel[0], pixel[1], pixel[2])

#if numPixel is 4 will pick every 4th pixel to add to image
def MakeFromFile(fileName="luca.jpg", numPixels=80, robotic=False):
    global WIDTH
    global HEIGHT
    global canvas

    img = Image.open(fileName, 'r') # Can be many different formats
    pix = img.load()
    width, height = img.size
    img.close()
    print("transmorfing {} which has dimensions {}x{}".format(fileName, width, height))

    WIDTH = width
    HEIGHT = height
     
    canvas = im.MakeCanvas(WIDTH, HEIGHT)

    START_LOCATIONS.clear()

    counter=0
    for i in range(width):
        for j in range(height):
            if (robotic and counter % numPixels==0) or (not robotic and randint(0, numPixels) < 1):
                Explore(i, j, RGBify(pix[i,j]))
            counter+=1

    print("done initializiing from file")

#not really useful anymore
def CheckForErrors(canvas):
    for col in canvas:
        for el in col:
            if(type(el) != tuple) or len(el) != 3:
                print("ERROR", el)
            for pixel in range(3):
                if type(pixel) != int:
                    print("ERROR", el)

def Main():
    print("starting image generation ({}x{}) = {:,} pixels".format(WIDTH, HEIGHT, WIDTH*HEIGHT))

    #can only have one MakeFromFile otherwise will probably crash
    #MakeFromFile("P1250945.png", 100)
    #MakeFromFile("luca.jpg", 80)
    #MakeFromFile("half.jpg", 2000)

    for location in START_LOCATIONS:
        Explore(location[0], location[1], START_COLOUR)

    #choose from random pixel
    i=0
    while len(partialExplored) > 0:
        i+=1
        nextInd = randint(0, len(partialExplored)-1)
        nextLocation= partialExplored[nextInd]

        VisitPixel(nextLocation, nextInd)

    #CheckForErrors(canvas)

    print("it took {:,} steps".format(i))
    print("there are {:,} duplicate pixels".format(CheckDuplicates(canvas)))
    print("creating image...\n")
    im.FormImage(canvas)

Main()
