import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from rectangle import Rectangle
import random


def findMinimun(posters):
    ancho = []
    alto = []
    for tup in posters:
        ancho.append(tup[0])
        alto.append(tup[1])
    return (min(ancho), min(alto))


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


def writeFile(filename, content):
    f = open(filename, "w")
    f.write(content)
    f.close()


def calculateSteps(step, maxSize):
    w_steps = []
    w = 0
    while(w+step < maxSize):
        w_steps.append(w)
        w = w + step
    return w_steps


def parseRectangles(filename):
    rectangles = []
    with open(filename) as fp:
        line = fp.readline()
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


def draw(filename):
    plt.savefig(filename)


def addRectangles(drawlist):
  #  matplotlib.use( 'tkagg' )
    for item in drawlist:
        create_rectangle(item)


def addHline(y):
    plt.axhline(y=y, alpha=0.1, color='tab:orange')


def addVline(x):
    plt.axvline(x=x, alpha=0.1, color='tab:orange')


# plt.imsave('demo')
