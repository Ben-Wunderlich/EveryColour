from random import randint
import imagemaker as im
from PIL import Image

WIDTH = 600
HEIGHT = 600

START_COLOUR = (200, 200, 200)

TARGET_COLOUR = None
#TARGET_COLOUR = (250, 221, 127)#The colour it wants to go towards
SKEW=1#how much it wants to go towards TARGET_COLOUR

START_LOCATIONS = [(randint(0, WIDTH-1), randint(0,HEIGHT-1))]
#(randint(0, WIDTH-1), randint(0,HEIGHT-1))

canvas = im.MakeCanvas(WIDTH, HEIGHT)

#must start out with one partially explored

#if has some value but not all neighbors explored
#this method shaves time for 1920x1080 image down to around 60secs
partialExplored = dict()
highestInd=0
#each value will have form (x, y) where x and y are position in the image

#takenColours=set()#can be used to make all colours unique but doesnt make it look more interesting

#value has form (r,g,b)
def OneDiffPixel(value):
    pixelMod = -6
    if(randint(0,1)==1):
        pixelMod = 6

    pixelPart = randint(0, 2)
    result = None

    if pixelPart==0:
        result= [value[0]+pixelMod, value[1], value[2]]
    elif pixelPart==1:
        result= [value[0], value[1]+pixelMod, value[2]]
    else:
        result= [value[0], value[1], value[2]+pixelMod]

    if TARGET_COLOUR is not None:
        if result[pixelPart] < TARGET_COLOUR[pixelPart] and pixelMod > 0:
            result[pixelPart]+=SKEW
        elif result[pixelPart] > TARGET_COLOUR[pixelPart] and pixelMod < 0:
            result[pixelPart]-=SKEW

    for part in result:
        if part > 255 or part < 0:
            return OneDiffPixel(value)
    return tuple(result)    

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
        del partialExplored[highestInd]#tried using highestInd instead of del but were both 49secs for 1920x1080
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
    print("changing to create {} which has dimensions {}x{} ({:,})".format(fileName, width, height, WIDTH*HEIGHT))

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

def ExpandFromPixels():
    #choose from random pixel
    i=0
    while len(partialExplored) > 0:
        i+=1
        #nextInd = 0#vertical lines
        #nextInt = len(partialExplored)-1 #horizontal lines
        nextInd = randint(0, len(partialExplored)-1)#normal
        #nextInd = randint(0, 1)# looks wack

        # if len(partialExplored) > 5:#coral patttern
        #     nextInd = randint(0,4)
        # else: 
        #     nextInd=0

        # if randint(0,15)==0:#inside of rock 
        #     nextInd = randint(0, len(partialExplored)-1)
        # else:
        #     nextInd=len(partialExplored)-1

        nextLocation= partialExplored[nextInd]

        VisitPixel(nextLocation, nextInd)
    return i



def Main():
    print("starting image generation ({}x{}) = {:,} pixels".format(WIDTH, HEIGHT, WIDTH*HEIGHT))

    #can only have one MakeFromFile otherwise will probably crash
    #MakeFromFile("bases\\P1250945.png", 100)
    #MakeFromFile("bases\\luca.jpg", 80)
    #MakeFromFile("bases\\viridy.png")
    #MakeFromFile("bases\\unknown.png", 200)

    for location in START_LOCATIONS:
        Explore(location[0], location[1], START_COLOUR)

    stepsTaken = ExpandFromPixels()
    #CheckForErrors(canvas)

    print("it took {:,} steps".format(stepsTaken))
    print("there are {:,} duplicate pixels".format(CheckDuplicates(canvas)))
    print("creating image...\n")
    im.FormImage(canvas)

Main()
