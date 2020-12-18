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
print("Running on "+str(max_threads)+" threads")
print("###############################################")
while (len(solution)>0 or start):
    start = False
    temp = []
    solutions_j = solve_threaded(i,solution,anchos_muro,verbose)
    for j in range(len(solutions_j)):
        solution_j = solutions_j[j]
        temp.append((solution_j[1],solution_j[2],solution_j[0])) #(score,restantes,indice)
    temp.sort(key=lambda tup: int(tup[0]), reverse=True)  # ordeno por costo/beneficio
    solution = temp[0][1] # Elijo el muro mejor performante, me quedo con sus posters restantes
    solution_path.append(str(i)+"-"+str(temp[0][2])) #Me guardo cual fue el elegido
    i+=1
print("##############################################################################################")
total_time = str(datetime.timedelta(seconds=(time.time() - total_start_time)))
print("Total Time: %s " % total_time)
print("Solution Path: %s " % solution_path)
text = []
pngs = []
for index in solution_path:
    pngs.append("out/{}/muro_".format(index)+index+".png")
    text.append("out/{}/muro_".format(index)+index+".sol")

combineImagesToPDF(pngs,"out/final.pdf")
combineSolutionsToTxt(text,"#Amount: {}\n#Solution Path: {}\n#Total Time: {} ".format(str(len(text)),solution_path, total_time),"out/final.txt")


