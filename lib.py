import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from rectangle import Rectangle
import random
import itertools


def findMinimun(posters):
    ancho = []
    alto = []
    for tup in posters:
        ancho.append(tup[0])
        alto.append(tup[1])
    return (min(ancho), min(alto))

def getCantPerCutHandV(cant,cuts):
    tuplcant = []
    for i in range(len(cuts)//2):
        cut = cuts[i*2]
        tuplcant.append((cant[i],cut[0]*cut[1]))
    return tuplcant


def getXorYPosters(posters, maximo, coordenada):
    posicionesPosters = []
    for pos in posters:
        if coordenada == 'ancho':
            if pos[0] < maximo:
                posicionesPosters.append(pos[0])
        else:
            if pos[1] < maximo:
                posicionesPosters.append(pos[1])
    return posicionesPosters

def valuesToZPLList(pos):
    tostr = ""
    for value in pos:
        tostr = tostr + str(value) + "\n"
    return tostr[0:len(tostr)-1]


def valuesToZPLTuple(pos):
    tostr = ""
    for value in pos:
        tostr = tostr + str(value[0]) + ";" + str(value[1]) + "\n"
    return tostr[0:len(tostr)-1]

def rectanglesToZPLQuad(rectangles):
    tostr = ""
    for value in rectangles:
        tostr = tostr + str(value.x) + ";" + str(value.y) + ";" + str(value.width) + ";" + str(value.height) + "\n"
    return tostr[0:len(tostr)-1]
    
def posterToTxt(posters):
    tostr = ""
    for value in posters:
        posterVariaton1 = str(value[0]) + ";"+ str(value[1])
        posterVariaton2 = str(value[1]) + ";"+ str(value[0])
        if(tostr.find(posterVariaton1) == -1 and tostr.find(posterVariaton2) == -1 ):
            tostr = tostr + str(value[0]) + ";"+ str(value[1]) +"\n"
    return tostr[0:len(tostr)-1]

def writeFile(filename, content):
    f = open(filename, "w")
    f.write(content)
    f.close()

def findMultiples(start,max): 
    multiples = set()
    temp = start 
    while(temp<=max-start):
        multiples.add(temp)
        temp = temp+start
    return multiples

def filterOutOfRange(rectangles,max_height,max_width):
    rects = []
    for rectangle in rectangles:
        if(rectangle.x+rectangle.width<=max_width):
            if(rectangle.y+rectangle.height<=max_height):
                rects.append(rectangle)
    return rects

def calculateSteps(maxSize, posterSizes):
    w_steps : set = set()
    for poster in posterSizes:
        w_steps = w_steps | set(findMultiples(poster,maxSize))
    w_steps.add(0)
    return w_steps

def generatePossibleRectangles(x,y,posters):
    rectangles = []
    for quad in set(itertools.product(x, y , posters)):
        rectangles.append(Rectangle(quad[0],quad[1],quad[2][0],quad[2][1]))
    return rectangles


def parseRectangles(filename):
    rectangles = []
    with open(filename) as fp:
        line = fp.readline()
        line = fp.readline()
        cnt = 1
        end = False
        print("\n###############################################")
        print("Solution:")
        while line and not end:
            line = fp.readline()
            if(len(line) > 1):
                recstr = line.split('#')
                rectangles.append(
                    Rectangle(int(recstr[1]), int(recstr[2]), int(recstr[3]), int(recstr[4].split(' ')[0])))
                print(recstr[1] + ", "+recstr[2] + ", " +
                      recstr[3] + ", " + recstr[4].split(' ')[0])
    return rectangles


def create_rectangle(rectangle: Rectangle):
    # get the right map, and get the color from the map
    color = matplotlib.cm.jet(
        rectangle.width + rectangle.height + random.randint(0, 100))
    rec = plt.Rectangle((rectangle.x, rectangle.y), rectangle.width,
                        rectangle.height, color=color, zorder=1, alpha=0.25)
    add_shape(rec)


def add_shape(patch):
    ax = plt.gca()
    ax.add_patch(patch)
    plt.axis('scaled')


def draw(filename,metadata):
    plt.text(0,0 , metadata, fontsize=12)
    plt.savefig(filename)


def addRectangles(drawlist):
    for item in drawlist:
        create_rectangle(item)


def addHline(y,alpha = 0.2, color ='tab:orange'):
    plt.axhline(y=y, alpha=alpha, color=color)


def addVline(x,alpha = 0.2, color ='tab:orange'):
    plt.axvline(x=x, alpha=alpha, color=color)


# plt.imsave('demo')
