import os
from shutil import copyfile
from pyscipopt import Model
from rectangle import Rectangle
from grapher import draw

#model = Model("CuttingStock")  # model name is optional
#a = model.addVar("a", vtype="CONTINUOUS")
#b = model.addVar("b", vtype="CONTINUOUS")
#o = model.addVar("c", vtype="CONTINUOUS")


model.readProblem("cuttingStock.zpl")
model.optimize()
sol = model.getBestSol()
#Busco solucion e imprimo puntos
print("\n\n###############################################")
print("Solucion:")
print("a: {}".format(sol[a]))
print("b: {}".format(sol[b]))
print("o: {}".format(sol[o]))
print("###############################################")








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