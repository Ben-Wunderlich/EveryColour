from random import randint
import imagemaker as im
from PIL import Image

from tkinter import *
from time import sleep

WIDTH = 400
HEIGHT = 400

START_COLOUR = (200, 200, 200)
START_LOCATIONS = [(randint(0, WIDTH-1), randint(0,HEIGHT-1))]
#(randint(0, WIDTH-1), randint(0,HEIGHT-1))

canvas = im.MakeCanvas(WIDTH, HEIGHT)

#must start out with one partially explored

#if has some value but not all neighbors exploreds
#this method shaves time for 1920x1080 image down to around 60secs
partialExplored = dict()
highestInd=0
#each value will have form (x, y) where x and y are position in the image

#takenColours=set()#can be used to make all colours unique but doesnt make it look more interesting

#value has form (r,g,b)
def OneDiffPixel(value):
    pixelMod = -7
    if(randint(0,1)==1):
        pixelMod = 7

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

def toHexa(pixVal):
    return '#%02x%02x%02x' % pixVal

def Explore(xLocation, yLocation, pixelValue, img=None):
    AddToDict((xLocation, yLocation))
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


def MakeImageBlack(img, width, height):
    for x in range(width):
        for y in range(height):
            img.put("#000000", (x,y))


#base code from https://stackoverflow.com/a/13215255
class VisualImage(object):
    def __init__(self):
        self.root = Tk()
        self.root.configure(bg='black')
        self.paused=False

        def PauseToggle(event):
            if(event.char == 'p'):
                self.paused = not self.paused

        self.root.bind("<Key>", PauseToggle)
        self.canvas = Canvas(self.root, width=WIDTH, height = HEIGHT)
        self.root.protocol('WM_DELETE_WINDOW', self.DeathMarch)

        self.canvas.pack()
        for location in START_LOCATIONS:
            Explore(location[0], location[1], START_COLOUR)

        self.img = PhotoImage(width=WIDTH, height=HEIGHT)
        MakeImageBlack(self.img, WIDTH, HEIGHT)
        self.canvas.create_image((0, 0), image=self.img, state="normal", anchor=NW)

        self.canvas.pack()
        self.root.after(1, self.animation)
        self.root.mainloop()

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
            #nextInd = 0#vertical lines
            nextInd = len(partialExplored)-1 #horizontal lines
            #nextInd = randint(0, len(partialExplored)-1)#normal
            # nextInd=0
            # if len(partialExplored) > 2:#just for last pixel
            #     nextInd = randint(0, 1)# looks wack

            # if len(partialExplored) > 4:#coral patttern
            #     nextInd = randint(0,4)
            # else: 
            #     nextInd=0

            # if randint(0,15)==0:#geode
            #     nextInd = randint(0, len(partialExplored)-1)
            # else:
            #     nextInd=len(partialExplored)-1

            nextLocation= partialExplored[nextInd]


            
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
