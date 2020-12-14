import os
from os import path
import time
from shutil import copyfile
from rectangle import Rectangle
import subprocess
import numpy as np
from lib import *
from config import *
import time,datetime

def solve(i,posters_cant):
    startPlot()
    posters = extractPosters(posters_cant)
    anchos_posters = getXorYPosters(posters,ancho_muro,'ancho')
    altos_posters = getXorYPosters(posters,alto_muro,'alto')
    print("Posters:")
    print(posters)
    print("Positions:")
    x_pos = calculateSteps( ancho_muro, anchos_posters)
    y_pos = calculateSteps( alto_muro, altos_posters)
    print(x_pos)
    print(y_pos)
    rectangles = filterOutOfRange(generatePossibleRectangles(x_pos,y_pos,posters),alto_muro,ancho_muro)
    drawGuidingLines(x_pos,y_pos,ancho_muro,alto_muro)
    print("###############################################")
    print("Writing Input Files")
    writeFile("posters_cant.txt", valuesToZPLTupleWithoutReps(posters_cant))
    writeFile("rects.txt", rectanglesToZPLQuad(rectangles))
    print("###############################################")
    print("Solving Problem")
    filename = 'solution.sol'
    start_time = time.time()
    subprocess.run(
        ['scip', '-c', 'read cuttingStock2d.zpl', '-c', 'set display verblevel 3', '-c', 'optimize',  '-c', 'write solution {}'.format(filename), '-c', 'quit'])
    if(path.exists("solution.sol")):
        end_time = time.time()
        tiempo = str(datetime.timedelta(seconds=(end_time-start_time)))
        rectangles = parseRectangles(filename)
        addRectangles(rectangles)
        print("###############################################")
        print("Tiempo de calculo del modelo: %s " % tiempo)
        print("Graph written in out.png")
        os.remove("solution.sol")
        print("Solution written to solution.last")
        draw("out_"+ str(i) +".png",str(i)+"-"+tiempo)
        writeFile("solution"+ str(i) +".sol", rectanglesToZPLQuad(rectangles))
        writeFile("solution.last", rectanglesToZPLQuad(rectangles))
        return updatePosterCount(rectangles,posters_cant)
    else:
        print("NO SOLUTION")
        if(path.exists("solution.last")):
            os.remove("solution.last")
        return []


print("Cutting Stock 2D")
print("\n###############################################")
print("###############################################")
i = 0
total_start_time = time.time()
solution = solve(0,posters_cant_start)
while (len(solution)>0):
    i+=1
    solution = solve(i,solution)
total_time = time.time() - total_start_time
print("###############################################")
print("###############################################")
print("Tiempo TOTAL de calculo del modelo: %s " % total_time)

