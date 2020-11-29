import os
import time
from shutil import copyfile
from rectangle import Rectangle
import grapher as Grapher
import subprocess


ancho_min = 36
alto_min = 254
anchoMuro = 240
altoMuro = 520


def valuesToZPLList(pos):
    tostr = ""
    for value in pos:
        tostr = tostr + str(value) + "\n"
    return tostr[0:len(tostr)-1]


def writeFile(filename, content):
    f = open(filename, "w")
    f.write(valuesToZPLList(content))
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
    with open(filename+".tbl") as fp:
        line = fp.readline()
        cnt = 1
        end = False
        while line and not end:
            line = fp.readline()
            if(line.find('v') != -1):
                cut = line[line.find('"'):len(line)]
                cut = cut.replace('"', '')
                recstr = cut.split('#')
                rectangles.append(
                    Rectangle(int(recstr[1]), int(recstr[2]), int(recstr[3]), int(recstr[4])))

            else:
                end = True
    return rectangles


print("\n###############################################")
print("Posibilidades:")
x_pos = calculateSteps(ancho_min, anchoMuro)
y_pos = calculateSteps(alto_min, altoMuro)
print(x_pos)
for x in x_pos:
    Grapher.addVline(x)
for y in y_pos:
    Grapher.addHline(y)
print(y_pos)
writeFile("altos.txt", y_pos)
writeFile("anchos.txt", x_pos)
print("###############################################")
print("Solving Problem")
filename = 'solution'
correct = subprocess.run(
    ['zimpl', '-v', '0', '-o', filename, '-t', 'mps', 'cuttingStock2d.zpl'])
rectangles = parseRectangles(filename)
print(rectangles)
Grapher.addRectangles(rectangles)
Grapher.draw("out.png")
