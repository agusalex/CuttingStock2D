import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from rectangle import Rectangle
from shutil import copyfile,rmtree
import random
import itertools
import subprocess
import time
import os
from os import path
from config import *
import time,datetime
from PIL import Image
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor


def solve(index,id,posters_with_amount,ancho_muro,alto_muro,costo_muro,verbose):

    posters_with_amount_filtered = filterNonFittingRectangles(posters_with_amount,ancho_muro,alto_muro)
    posters = extractPosters(posters_with_amount_filtered)
    anchos_altos_tuple = extractWidthAndHeight(posters, ancho_muro, alto_muro)
    anchos_posters = anchos_altos_tuple[0]
    altos_posters = anchos_altos_tuple[1]
    print("Posters:")
    print(posters_with_amount_filtered)
    print("Positions:")
    x_pos = calculateSteps( ancho_muro, anchos_posters)
    y_pos = calculateSteps( alto_muro, altos_posters)
    print(x_pos)
    print(y_pos)
    rectangles = filterOutOfRange(generatePossibleRectangles(x_pos,y_pos,posters),alto_muro,ancho_muro)
    print("###############################################")
    print("Writing Input Files")
    if not os.path.exists('out/{}'.format(id)):
        os.makedirs('out/{}'.format(id))
    else:
        rmtree('out/{}'.format(id))
        os.makedirs('out/{}'.format(id))
    writeFile("out/{}/posters_cant.txt".format(id), valuesToZPLTupleWithoutReps(posters_with_amount_filtered))
    writeFile("out/{}/rects.txt".format(id), rectanglesToZPLQuad(rectangles))
    print("###############################################")
    start_time = time.time()

    writeFile("out/{}/cuttingStock2d.zpl".format(id),readFile("cuttingStock2d.zpl"))
    solveScip("cuttingStock2d.zpl","out/{}".format(id),"solution"+ str(id) +".sol",verbose)

 
    end_time = time.time()
    if(path.exists("out/{}/solution".format(id)+ str(id) +".sol")):
        tiempo = str(datetime.timedelta(seconds=(end_time-start_time)))
        rectangles = parseRectangles("out/{}/solution".format(id)+ str(id) +".sol")
        startPlot()
        drawGuidingLines(x_pos,y_pos,ancho_muro,alto_muro)
        addRectangles(rectangles)
        print("###############################################")
        print("Model Solving Time: %s " % tiempo)
        print("###############################################")
        area = calculateArea(rectangles)
        score = area/costo_muro
        metadata = "#Type: "+str(ancho_muro)+"X"+str(alto_muro)+" - T: "+ tiempo+"\n#Area: "+str(area) + " - Cost: "+str(costo_muro)+" - Score: "+str(int(score))+ " - Inserted: "+str(len(rectangles))
        draw("out/{}/muro_".format(id)+ str(id) +".png",metadata)
        writeFile("out/{}/muro_".format(id)+ str(id) +".sol", metadata +"\n"+ rectanglesToZPLQuad(rectangles)+"\n")
        print("##############################################################################################")
        # Costo beneficio del muro y posters que faltan por colocar si se elije ese muro
        return (index,score,updatePosterCount(rectangles, posters_with_amount_filtered))
    else:
        print("NO SOLUTION")
        return ()



def solve_threaded(i,posters_with_amount,walls,verbose):
    with ProcessPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        #m = multiprocessing.Manager()
        #lock = m.Lock()
        for k in range(len(walls)):
            futures.append(executor.submit(solve, index = k, id = str(i)+"-"+str(k),
            posters_with_amount = posters_with_amount, ancho_muro=anchos_muro[k],
             alto_muro=altos_muro[k],costo_muro=costos_muro[k],verbose=verbose))
        result = []
        
        for future in concurrent.futures.as_completed(futures):
            try:
                data = future.result()
                result.append(data)
            except Exception as exc:
                print('%r generated an exception: %s' % (exc))
        return result





def solveScip(model,folder,output,verbose = False):
    if(not verbose):
        print("Solving Problem....(Enable Verbose Mode to see SCIP output)")
        subprocess.check_call(
            ['scip', '-c', 'read {}'.format(model), '-c', 'set display verblevel 3', '-c', 'optimize',  '-c', 'write solution {}'.format(output), '-c', 'quit'], stdout=subprocess.DEVNULL, cwd=folder)
    else:
        print("Solving Problem....")
        subprocess.check_call(
            ['scip', '-c', 'read {}'.format(model), '-c', 'set display verblevel 3', '-c', 'optimize',  '-c', 'write solution {}'.format(output), '-c', 'quit'], cwd=folder)
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

    

def readFile(filename):
    with open(filename, 'r+') as f:
        return f.read()


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
    ax.set_title(time.time())
    plt.axis('scaled')

def startPlot():
    plt.figure(str(time.time()))

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
    plt.axvline(x=x,label= 5, alpha=alpha, color=color)

def combineImagesToPDF(images:list,filename):
    raw = []
    for image in images:
        raw.append(Image.open(image))
    rgb = []
    for image in raw:
        rgb.append(image.convert('RGB'))
    rgb[0].save(filename,save_all=True, append_images=rgb[1:len(raw)])

def combineSolutionsToTxt(solutions:list,metadata,filename):
    final = metadata+"\n########################\n"
    for sol in solutions:
        with open(sol) as fp: 
            final +=fp.read()
    writeFile(filename,final)

# plt.imsave('demo')