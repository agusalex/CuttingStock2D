from lib import findMinimun,getCantPerCutHandV,getXorYPosters
ancho_muro = 240
alto_muro = 520
# POSTERS agregar siempre vertical y horizontal, siempre numero par
posters = [(40,30)]
#cantidades = [20,20]
#cantidadesXPoster = getCantPerCutHandV(cantidades,posters) #(cantidad,ancho*alto)
#Posibles anchos y altos de posters que entran en el muro
anchos_poster = getXorYPosters(posters,ancho_muro,'ancho')
altos_posters = getXorYPosters(posters,alto_muro,'alto')
