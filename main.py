from random import randint
import imagemaker as im
from PIL import Image

WIDTH = 1920
HEIGHT = 1080

START_COLOUR = (118, 150, 250)
START_LOCATIONS = [(randint(0, WIDTH-1), randint(0,HEIGHT-1))]

canvas = im.MakeCanvas(WIDTH, HEIGHT)

#must start out with one partially explored

#if has some value but not all neighbors explored
partialExplored = dict()
highestInd=0
#each will have form (x, y) where x and y are position in the image

#takenColours=set()#will only use if it is otherwise uninteresting

#value has form (r,g,b)
def OneDiffPixel(value):
    pixelMod= -9
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
    Duplicates = 0
    for col in canvas:
        for el in col:
            if el in distinctCols:
                Duplicates+=1
            else:
                distinctCols.add(el)
    return Duplicates

def AddToDict(el):
    global highestInd
    highestInd = len(partialExplored)
    partialExplored[len(partialExplored)] = el

#if numPixel is 4 will pick every 13th pixel to add to image
def MakeFromFile(fileName="P1250945.png", numPixels=27):
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
            if counter % numPixels==0:
                Explore(i, j, pix[i,j])
            counter+=1

def Main():

    MakeFromFile("P1250945.png", 7)
    print("done initializiing from file")

    for location in START_LOCATIONS:
        Explore(location[0], location[1], START_COLOUR)
    #choose from random pixel
    i=0
    while len(partialExplored) > 0:
        i+=1
        nextInd = randint(0, len(partialExplored)-1)
        nextLocation= partialExplored[nextInd]

        VisitPixel(nextLocation, nextInd)

    print("it took {} steps".format(i))
    print("there are {} duplicates".format(CheckDuplicates(canvas)))

    im.FormImage(canvas)

Main()
