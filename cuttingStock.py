import os
import time
from shutil import copyfile
from rectangle import Rectangle
import subprocess
import numpy as np
from lib import *


# MURO
ancho_muro = 47
alto_muro = 47
# POSTERS
posters = [(7, 5), (10, 12)]
# Minimos
minimos = findMinimun(posters)
ancho_min_poster = minimos[0]
alto_min_poster = minimos[1]

print("\n###############################################")
print("Posibilidades:")
x_pos = calculateSteps(ancho_min_poster, ancho_muro)
y_pos = calculateSteps(alto_min_poster, alto_muro)
print(x_pos)
print(y_pos)
print("Posters:")
print(posters)
print("Minimos:")
print(minimos)
for x in x_pos:
    addVline(x)
for y in y_pos:
    addHline(y)

writeFile("posters.txt", valuesToZPLTuple(posters))
writeFile("altos.txt", valuesToZPLList(y_pos))
writeFile("anchos.txt", valuesToZPLList(x_pos))
print("###############################################")
print("Solving Problem")
filename = 'solution.sol'
correct = subprocess.run(
    ['scip', '-c', 'read cuttingStock2d.zpl', '-c', 'set display verblevel 3', '-c', 'optimize',  '-c', 'write solution {}'.format(filename), '-c', 'quit'])
rectangles = parseRectangles(filename)
addRectangles(rectangles)
draw("out.png")
print("###############################################")
print("Graph written in out.png")
