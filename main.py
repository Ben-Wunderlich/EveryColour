from random import randint
from tkinter.constants import NW
import imagemaker as im
from randict import randict
from PIL import Image

from tkinter import Canvas, PhotoImage, TclError, Tk
from time import sleep

WIDTH = 500
HEIGHT = 400

VISUALIZE_PROCESS = False
START_COLOUR = (200, 200, 200)

MAKE_FROM_FILE = None
#MAKE_FROM_FILE = ("bases\\hellovader.jpg", 50)

TARGET_COLOUR = None
#TARGET_COLOUR = (250, 221, 127)#The colour it wants to go towards
#TARGET_COLOUR = (255, 255, 255)
SKEW=1#how much it wants to go towards TARGET_COLOUR

START_LOCATIONS = [(WIDTH//2, HEIGHT//2)]
#(WIDTH//2, HEIGHT//2)
#(randint(0, WIDTH-1), randint(0,HEIGHT-1))

POS_MOD=5#how much to add to pixel
NEG_MOD=-5#how much to subtract from a pixel

canvas = im.MakeCanvas(WIDTH, HEIGHT)

#must start out with one partially explored

#if has some value but not all neighbors exploreds
#this method shaves time for 1920x1080 image down to around 60secs
partialExplored = randict()
#each value will have form (x, y) where x and y are position in the image

#takenColours=set()#can be used to make all colours unique but doesnt make it look more interesting

def GetNextLocation():
        #nextInd = 0#vertical lines
        #nextInd = len(partialExplored)-1 #horizontal lines
        
        return partialExplored.GetRandomElement()#normal

        #nextInd = randint(0,4)#coral

        # if randint(0,30)==0:#inside of rock 
        #     return partialExplored.GetRandomElement()#normal
        # else:
        #     nextInd=len(partialExplored)-1


        nextLocation= partialExplored.GetElementAt(nextInd)
        return (nextLocation, nextInd)

#value has form (r,g,b)
def OneDiffPixel(value):
    pixelMod = NEG_MOD
    if(randint(0,1)==1):
        pixelMod = POS_MOD

    pixelPart = randint(0, 2)
    result = None

    if pixelPart==0:
        result= [value[0]+pixelMod, value[1], value[2]]
    elif pixelPart==1:
        result= [value[0], value[1]+pixelMod, value[2]]
    else:
        result= [value[0], value[1], value[2]+pixelMod]

    if TARGET_COLOUR is not None:
        if randint(0,1)==1 and result[pixelPart] < TARGET_COLOUR[pixelPart] and pixelMod > 0:
            result[pixelPart]+=SKEW
        elif randint(0,1)==1 and result[pixelPart] > TARGET_COLOUR[pixelPart] and pixelMod < 0:
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

def toHexa(pixVal):
    return '#%02x%02x%02x' % pixVal

def Explore(xLocation, yLocation, pixelValue, img=None):
    partialExplored.AddElement((xLocation, yLocation))
    canvas[xLocation][yLocation] = pixelValue
    if img is not None:
        img.put(toHexa(pixelValue), (xLocation, yLocation))

def VisitPixel(location, index, img=None):
    global highestInd
    newPixel = NewPixelValue(location)

    #check if filled pixel in each direction
    if ValidToExplore(location[0]+1, location[1]):#right
        Explore(location[0]+1, location[1], newPixel, img)

    elif ValidToExplore(location[0], location[1]-1):#down
        Explore(location[0], location[1]-1, newPixel, img)

    elif ValidToExplore(location[0]-1, location[1]):#left
        Explore(location[0]-1, location[1], newPixel, img)

    elif ValidToExplore(location[0], location[1]+1):#up
        Explore(location[0], location[1]+1, newPixel, img)

    else:#nowhere is valid
        partialExplored.RemoveElement(index)

def CheckDuplicates(canvas):
    distinctCols = set()
    for col in canvas:
        for el in col:
            distinctCols.add(el)
    return (WIDTH*HEIGHT) - len(distinctCols)

def RGBify(pixel):
    if len(pixel) == 3:
        return pixel
    else:#is in rgba
        return (pixel[0], pixel[1], pixel[2])

#if numPixel is 4 will pick every 4th pixel to add to image
def MakeFromFile(fileName="bases\\luca.jpg", numPixels=80, robotic=False):
    global WIDTH
    global HEIGHT
    global canvas
    global START_LOCATIONS

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
    return canvas

#not really useful anymore
def CheckForErrors(canvas):
    for col in canvas:
        for el in col:
            if(type(el) != tuple) or len(el) != 3:
                print("ERROR", el)
            for pixel in range(3):
                if type(pixel) != int:
                    print("ERROR", el)


def MakeImageBlack(img, width, height):
    for x in range(width):
        for y in range(height):
            img.put("#000000", (x,y))

def ExpandFromPixels():
    #choose from random pixel
    i=0
    while len(partialExplored) > 0:
        i+=1
        nextLocation, nextInd = GetNextLocation()

        VisitPixel(nextLocation, nextInd)
    return i

#base code from https://stackoverflow.com/a/13215255
class VisualImage(object):
    def __init__(self):
        if MAKE_FROM_FILE is not None:
            MakeFromFile(*MAKE_FROM_FILE)


        if VISUALIZE_PROCESS:
            self.root = Tk()
            self.root.configure(bg='black')
            self.paused=True

            def PauseToggle(event):
                if(event.char == 'p'):
                    self.paused = not self.paused
                if self.paused:
                    print("pauseing")
                else:
                    print("no longer paused")

            self.root.bind("<Key>", PauseToggle)
            self.canvas = Canvas(self.root, width=WIDTH, height = HEIGHT)
            self.root.protocol('WM_DELETE_WINDOW', self.DeathMarch)

            self.canvas.pack()
        for location in START_LOCATIONS:
            Explore(location[0], location[1], START_COLOUR)

        if VISUALIZE_PROCESS:
            self.img = PhotoImage(width=WIDTH, height=HEIGHT)
            MakeImageBlack(self.img, WIDTH, HEIGHT)
            self.canvas.create_image((0, 0), image=self.img, state="normal", anchor=NW)

            self.canvas.pack()
            self.root.after(1, self.animation)
            self.root.mainloop()
        else:
            print("starting image generation ({}x{}) = {:,} pixels".format(WIDTH, HEIGHT, WIDTH*HEIGHT))
            stepsTaken = ExpandFromPixels()
            print("it took {:,} steps".format(stepsTaken))
            print("there are {:,} duplicate pixels".format(CheckDuplicates(canvas)))
            print("creating image...\n")
            im.FormImage(canvas)



    def DeathMarch(self):
        if not self.paused:
            self.root.destroy()
            return
        self.paused=False
        self.root.after(20, self.DeathMarch)

    def SpinLoop(self):
        if self.paused:
            self.root.after(20, self.SpinLoop)

    def animation(self):
        #sleep(5)
        i=0
        while len(partialExplored) > 0:
            #sleep(0.001)
            if self.paused:
                self.SpinLoop()

            i+=1

            nextLocation, nextInd = GetNextLocation()
            
            try:
                VisitPixel(nextLocation, nextInd, self.img)
                self.canvas.update()
            except TclError:
                print("closed early")
                return
        print("finished")
        if input("create image from it?(y/n)") == "y":
            im.FormImage(canvas, False)


VisualImage()
