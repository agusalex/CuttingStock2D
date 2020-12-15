import os
from os import path
import time
from shutil import copyfile,rmtree
from rectangle import Rectangle
import numpy as np
import multiprocessing
from lib import *
from config import *
import time,datetime

import concurrent.futures
from concurrent.futures import ProcessPoolExecutor


def solve( i,posters_with_amount,ancho_muro,alto_muro,costo_muro):

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
    id = i
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
    solveScip("cuttingStock2d.zpl","out/{}".format(id),"solution"+ str(i) +".sol",verbose)

 
    end_time = time.time()
    if(path.exists("out/{}/solution".format(id)+ str(i) +".sol")):
        tiempo = str(datetime.timedelta(seconds=(end_time-start_time)))
        rectangles = parseRectangles("out/{}/solution".format(id)+ str(i) +".sol")
        startPlot()
        drawGuidingLines(x_pos,y_pos,ancho_muro,alto_muro)
        addRectangles(rectangles)
        print("###############################################")
        print("Model Solving Time: %s " % tiempo)
        print("###############################################")
        area = calculateArea(rectangles)
        score = area/costo_muro
        metadata = "#Type: "+str(ancho_muro)+"X"+str(alto_muro)+" - T: "+ tiempo+"\n#Area: "+str(area) + " - Cost: "+str(costo_muro)+" - Score: "+str(int(score))+ " - Inserted: "+str(len(rectangles))
        draw("out/{}/muro_".format(id)+ str(i) +".png",metadata)
        writeFile("out/{}/muro_".format(id)+ str(i) +".sol", metadata +"\n"+ rectanglesToZPLQuad(rectangles)+"\n")
        print("##############################################################################################")
        # Costo beneficio del muro y posters que faltan por colocar si se elije ese muro
        return (score,updatePosterCount(rectangles, posters_with_amount_filtered))
    else:
        print("NO SOLUTION")
        return ()



def solve_threaded(walls):
    with ProcessPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        m = multiprocessing.Manager()
        #lock = m.Lock()
        for k in range(len(walls)):
            futures.append(executor.submit(solve, i = str(i)+"-"+str(k),
            posters_with_amount = solution, ancho_muro=anchos_muro[k],
             alto_muro=altos_muro[k],costo_muro=costos_muro[k]))
        result = []
        
        for future in concurrent.futures.as_completed(futures):
            try:
                data = future.result()
                result.append(data)
            except Exception as exc:
                print('%r generated an exception: %s' % (exc))
        return result


print("\nCutting Stock 2D")
print("\n###############################################")


i = 0
if not os.path.exists('out'):
    os.makedirs('out')
total_start_time = time.time()
#solution = solve(0,raw_posters_with_amount,anchos_muro[0],altos_muro[0])
solution = raw_posters_with_amount
solution_path = []
start = True
if(threaded):
    print("Running async on "+str(max_threads)+" threads")
print("###############################################")
while (len(solution)>0 or start):
    start = False
    temp = []
    if(threaded):
        solutions_j = solve_threaded(anchos_muro)
        for k in range(len(solutions_j)):
            solution_j = solutions_j[k]
            temp.append((solution_j[0],solution_j[1],k)) #(score,restantes,indice)
    else:
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
text = []
pngs = []
for index in solution_path:
    pngs.append("out/{}/muro_".format(index)+index+".png")
    text.append("out/{}/muro_".format(index)+index+".sol")

combineImagesToPDF(pngs,"out/final.pdf")
combineSolutionsToTxt(text,"out/final.txt")


