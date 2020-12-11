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


print("Cutting Stock 2D")
print("\n###############################################")
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
    os.rename("solution.sol","solution.last")
    print("Solution written to solution.last")
    draw("out.png",tiempo)
else:
    print("NO SOLUTION")
    if(path.exists("solution.last")):
        os.remove("solution.last")
