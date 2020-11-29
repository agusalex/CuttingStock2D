import os
import time
from shutil import copyfile
from rectangle import Rectangle
import grapher as Grapher
import subprocess

#MURO
ancho_muro = 50
alto_muro = 50
#POSTERS
posters = [(5,5)]
#Minimos
ancho_min_poster = 5
alto_min_poster = 5




def valuesToZPLList(pos):
    tostr = ""
    for value in pos:
        tostr = tostr + str(value) + "\n"
    return tostr[0:len(tostr)-1]

def valuesToZPLTuple(pos):
    tostr = ""
    for value in pos:
        tostr = tostr + str(value[0]) + ";" +str(value[1])+ "\n"
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
            if(len(line)>1):
                recstr = line.split('#')      
                rectangles.append(
                    Rectangle(int(recstr[1]), int(recstr[2]), int(recstr[3]), int(recstr[4].split(' ')[0])))
                print(recstr[1] + ", "+recstr[2] + ", " + recstr[3] + ", " + recstr[4].split(' ')[0])
    return rectangles


print("\n###############################################")
print("Posibilidades:")
x_pos = calculateSteps(ancho_min_poster, ancho_muro)
y_pos = calculateSteps(alto_min_poster, alto_muro)
print(x_pos)
print(y_pos)
print("Posters:")
print(posters)
for x in x_pos:
    Grapher.addVline(x)
for y in y_pos:
    Grapher.addHline(y)

writeFile("posters.txt", valuesToZPLTuple(posters))
writeFile("altos.txt", valuesToZPLList(y_pos))
writeFile("anchos.txt", valuesToZPLList(x_pos))
print("###############################################")
print("Solving Problem")
filename = 'solution.sol'
correct = subprocess.run(
    ['scip','-c','read cuttingStock2d.zpl','-c','set display verblevel 3' ,'-c', 'optimize',  '-c', 'write solution {}'.format(filename),'-c','quit'])
rectangles = parseRectangles(filename)
Grapher.addRectangles(rectangles)
Grapher.draw("out.png")
print("###############################################")
print("Graph written in out.png")
