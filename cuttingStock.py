import os
from os import path
import time
from shutil import copyfile
from rectangle import Rectangle
import numpy as np
from lib import *
from config import *
import time,datetime

def solve(i,posters_with_amount,ancho_muro,alto_muro,costo_muro):
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
    writeFile("posters_cant.txt", valuesToZPLTupleWithoutReps(posters_with_amount_filtered))
    writeFile("rects.txt", rectanglesToZPLQuad(rectangles))
    print("###############################################")
    start_time = time.time()
    solveScip("cuttingStock2d.zpl","out/solution"+ str(i) +".sol",verbose)
    if(path.exists("out/solution"+ str(i) +".sol")):
        end_time = time.time()
        tiempo = str(datetime.timedelta(seconds=(end_time-start_time)))
        rectangles = parseRectangles("out/solution"+ str(i) +".sol")
        startPlot()
        drawGuidingLines(x_pos,y_pos,ancho_muro,alto_muro)
        addRectangles(rectangles)
        print("###############################################")
        print("Model Solving Time: %s " % tiempo)
        os.remove("out/solution"+ str(i) +".sol")
        print("###############################################")
        area = calculateArea(rectangles)
        score = area/costo_muro
        draw("out/muro_"+ str(i) +".png","T: "+ tiempo+" - Area: "+str(area)+"- Cost: "+str(costo_muro)+" - Score: "+str(int(score)))
        writeFile("out/muro_"+ str(i) +".sol", rectanglesToZPLQuad(rectangles))
        writeFile("out/solution.last", rectanglesToZPLQuad(rectangles))
        print("Solution written to muro_"+ str(i) +".sol")
        print("Graph written to muro_"+ str(i) +".sol")
        print("##############################################################################################")
        # Costo beneficio del muro y posters que faltan por colocar si se elije ese muro
        return (score,updatePosterCount(rectangles, posters_with_amount_filtered))
    else:
        print("NO SOLUTION")
        if(path.exists("out/solution.last")):
            os.remove("out/solution.last")
        return []




print("Cutting Stock 2D")
print("\n###############################################")
print("###############################################")

i = 0
total_start_time = time.time()

#solution = solve(0,raw_posters_with_amount,anchos_muro[0],altos_muro[0])
solution = raw_posters_with_amount
solution_path = []
start = True
while (len(solution)>0 or start):
    start = False
    temp = []
    for j in range(len(anchos_muro)): # resuelvo con cada tipo de muro
       solution_j = solve(str(i)+"-"+str(j),solution,anchos_muro[j],altos_muro[j],costos_muro[j]) 
       temp.append((solution_j[0],solution_j[1], j)) #(score,restantes,indice)
    temp.sort(key=lambda tup: int(tup[0]), reverse=True)  # ordeno por costo/beneficio
    solution = temp[0][1] # Elijo el muro mejor performante, me quedo con sus posters restantes
    solution_path.append(str(i)+"-"+str(temp[0][2])) #Me guardo cual fue el elegido para despues borrar los que no hacen falta
    i+=1
total_time = time.time() - total_start_time
print("##############################################################################################")
print("Total Time: %s " % total_time)
print("Solution Path: %s " % solution_path)

