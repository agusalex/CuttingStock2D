import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from rectangle import Rectangle
import random
import itertools
import subprocess

def solveScip(model,output,verbose = False):

    if(not verbose):
        print("Solving Problem....(Enable Verbose Mode to see SCIP output)")
        subprocess.check_call(
            ['scip', '-c', 'read {}'.format(model), '-c', 'set display verblevel 3', '-c', 'optimize',  '-c', 'write solution {}'.format(output), '-c', 'quit'], stdout=subprocess.DEVNULL)
    else:
        print("Solving Problem....")
        subprocess.check_call(
            ['scip', '-c', 'read {}'.format(model), '-c', 'set display verblevel 3', '-c', 'optimize',  '-c', 'write solution {}'.format(output), '-c', 'quit'])

def extractWidthAndHeight(rectangles, max_width, max_height):
    postersWidth = []
    postersHeight = []
    for pos in rectangles:
        if pos[0] < max_width:
            postersWidth.append(pos[0])
        if pos[1] < max_height:
            postersHeight.append(pos[1])
    return (postersWidth,postersHeight)

def valuesToZPLList(pos):
    tostr = ""
    for value in pos:
        tostr = tostr + str(value) + "\n"
    return tostr[0:len(tostr)-1]

def valuesToZPLTuple(posters):
    tostr = ""
    for value in posters:
        tostr = tostr + str(value[0]) + ";" + str(value[1]) + "\n"
    return tostr[0:len(tostr)-1]

def rectanglesToZPLQuad(rectangles):
    tostr = ""
    for value in rectangles:
        tostr = tostr + str(value.x) + ";" + str(value.y) + ";" + str(value.width) + ";" + str(value.height) + "\n"
    return tostr[0:len(tostr)-1]

def extractPosters(rect_amount):
    posters = []
    for tuple in rect_amount:
        posters.append(tuple[0])
    return posters

def calculateArea(rectangles:list):
    area = 0
    for rect in rectangles:
        area = area + (rect.width * rect.height)
    return area

def filterNonFittingRectangles(non_filtered,max_width,max_height):
    filtered = []
    for tuple in non_filtered:
        if ((tuple[0][0]<=max_width) and (tuple[0][1] <= max_height)):
            filtered.append(tuple)
    return filtered
    
def valuesToZPLTupleWithoutReps(posters):
    tostr = ""
    for value in posters:
        posterVariaton1 = str(value[0][0]) + ";"+ str(value[0][1])
        posterVariaton2 = str(value[0][1]) + ";"+ str(value[0][0])
        if(tostr.find(posterVariaton1) == -1 and tostr.find(posterVariaton2) == -1 ):
            tostr = tostr + str(value[0][0]) + ";"+ str(value[0][1]) + ";"+ str(value[1]) +"\n"
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
    w_steps_list = list(w_steps)
    w_steps_list.sort()
    return w_steps_list

def generatePossibleRectangles(x,y,posters):
    rectangles = []
    for quad in set(itertools.product(x, y , posters)):
        rectangles.append(Rectangle(quad[0],quad[1],quad[2][0],quad[2][1]))
    return rectangles

def hasHowManyOfThisRectangle(rectangles,width,height):
    amount = 0
    for rect in rectangles:
        if((rect.width == width and rect.height == height) or (rect.width == height and rect.height == width )):
            amount +=1
    return amount

def updatePosterCount(rectangles:list,posters_cant:list):
    new = []
    for poster in posters_cant:
        amountFound = hasHowManyOfThisRectangle(rectangles,poster[0][0],poster[0][1])
        new_poster = ((poster[0][0],poster[0][1]),(poster[1] - amountFound))
        if(new_poster[1]>0):
            new.append(new_poster)
    return new

def parseListPlainTextInput(input):
    parsed_1 = input.replace(' ','').split(',')
    parsed = []
    for item in parsed_1:
        parsed.append(int(item))
    return parsed       

def parseRectanglesPlainTextInput(input):
    parsed_1 = input.replace(' ','').split(',')
    parsed = []
    for triple in parsed_1:
        splitted = triple.split('#')
        tuple = splitted[0].split(';')
        cant = splitted[1]
        width = tuple[0]
        height = tuple[1]
        parsed.append(((int(width),int(height)),int(cant)))

    return parsed        

def parseRectangles(filename):
    rectangles = []
    with open(filename) as fp:
        line = fp.readline()
        line = fp.readline()
        cnt = 1
        end = False
        while line and not end:
            line = fp.readline()
            if(len(line) > 1):
                recstr = line.split('#')
                rectangles.append(
                    Rectangle(int(recstr[1]), int(recstr[2]), int(recstr[3]), int(recstr[4].split(' ')[0])))
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

def startPlot():
    plt.figure()

def draw(filename,metadata):
    plt.title(metadata)
    plt.savefig(filename)
    plt.close

def drawGuidingLines(x_pos, y_pos, width_max,height_max):
    for x in x_pos:
        addVline(x)
    for y in y_pos:
        addHline(y)
    addVline(width_max,alpha=1,color = 'tab:red')
    addHline(height_max,alpha=1,color = 'tab:red')
    addVline(0,alpha=1,color = 'tab:red')
    addHline(0,alpha=1,color = 'tab:red')

def addRectangles(drawlist):
    for item in drawlist:
        create_rectangle(item)


def addHline(y,alpha = 0.2, color ='tab:orange'):
    plt.axhline(y=y, alpha=alpha, color=color)


def addVline(x,alpha = 0.2, color ='tab:orange'):
    plt.axvline(x=x, alpha=alpha, color=color)


# plt.imsave('demo')