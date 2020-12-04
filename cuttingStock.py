import os
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
rectangles = filterOutOfRange(generatePossibleRectangles(x_pos,y_pos,posters),alto_muro,ancho_muro)
print(x_pos)
print(y_pos)
#print("rectangles:")
#print(rectangles)
for x in x_pos:
    addVline(x)
for y in y_pos:
    addHline(y)
addVline(ancho_muro,alpha=1,color = 'tab:red')
addHline(alto_muro,alpha=1,color = 'tab:red')
addVline(0,alpha=1,color = 'tab:red')
addHline(0,alpha=1,color = 'tab:red')
print("###############################################")
print("Writing Input Files")
writeFile("rects.txt", rectanglesToZPLQuad(rectangles))
print("###############################################")
print("Solving Problem")
filename = 'solution.sol'
start_time = time.time()
correct = subprocess.run(
    ['scip', '-c', 'read cuttingStock2d.zpl', '-c', 'set display verblevel 3', '-c', 'optimize',  '-c', 'write solution {}'.format(filename), '-c', 'quit'])
end_time = time.time()
tiempo = str(datetime.timedelta(seconds=(end_time-start_time)))
rectangles = parseRectangles(filename)
addRectangles(rectangles)
print("###############################################")
print("Tiempo de calculo del modelo: %s " % tiempo)
print("Graph written in out.png")
draw("out.png",tiempo)
