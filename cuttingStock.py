import os
from shutil import copyfile
from pyscipopt import Model
from rectangle import Rectangle
from grapher import draw

#model = Model("CuttingStock")  # model name is optional
#a = model.addVar("a", vtype="CONTINUOUS")
#b = model.addVar("b", vtype="CONTINUOUS")
#o = model.addVar("c", vtype="CONTINUOUS")
#set anchoMuro := {0..520};
#set altoMuro := {0..240};
#posters = [(254,36),(36,254)]
ancho_min = 36
alto_min = 254
anchoMuro = 240
altoMuro = 520
alto = 240;
x_pos = []
y_pos = []

print("\n###############################################")
print("Posibilidades:")
x = 0
while(x+ancho_min < anchoMuro):
    x_pos.append(x)
    x = x + ancho_min
y = 0
while(y+alto_min < altoMuro):
    y_pos.append(y)
    y = y + alto_min

print(x_pos)    
print(y_pos)

print("###############################################")






#model.readProblem("cuttingStock.zpl")
#model.optimize()
#Busco solucion e imprimo puntos
#print("a: {}".format(sol[a]))
#print("b: {}".format(sol[b]))
#print("o: {}".format(sol[o]))

#model.setObjective(o,"maximize")

#model.addCons(4>=a*2 + b + o)
#model.addCons(5>=a*3 + b + o)
#model.addCons(1<=a*3 + b - o)


#model.addCons(-a -b -c - o>= -2)
#model.addCons(-16*a -4*b -c - o>= -2)
#model.addCons(-4*a -2*b -c +o <= -2)
#model.addCons(-9*a -3*b -c +o <= -2)

#
#model.readProblem("ejemplo.zpl")