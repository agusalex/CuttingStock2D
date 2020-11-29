import os
import time
from shutil import copyfile
from rectangle import Rectangle
import subprocess
import numpy as np
from lib import *
from config import *

print("Cutting Stock 2D")
print("\n###############################################")
print("Constants:")
x_pos = calculateSteps(ancho_min_poster, ancho_muro, posibles_anchos_poster)
y_pos = calculateSteps(alto_min_poster, alto_muro, posibles_altos_poster)
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
addVline(ancho_muro,alpha=1,color = 'tab:red')
addHline(alto_muro,alpha=1,color = 'tab:red')
addVline(0,alpha=1,color = 'tab:red')
addHline(0,alpha=1,color = 'tab:red')
print("###############################################")
print("Writing Input Files")
writeFile("posters.txt", valuesToZPLTuple(posters))
writeFile("altos.txt", valuesToZPLList(y_pos))
writeFile("anchos.txt", valuesToZPLList(x_pos))
writeFile("maxAlto.txt",str(alto_muro))
writeFile("maxAncho.txt",str(ancho_muro))
writeFile("cantidades.txt",valuesToZPLTuple(cantidadesXPoster))
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
os.remove("posters.txt")
os.remove("altos.txt")
os.remove("anchos.txt")
os.remove("maxAlto.txt")
os.remove("maxAncho.txt")
