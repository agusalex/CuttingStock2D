from lib import findMinimun,getCantPerCutHandV,getPosicionesFactibles
ancho_muro = 240
alto_muro = 520
# POSTERS agregar siempre vertical y horizontal, siempre numero par
posters = [(254,36),(36, 254)]
cantidades = [20]
cantidadesXPoster = getCantPerCutHandV(cantidades,posters) #(cantidad,ancho*alto)
#Posibles anchos y altos de posters que entran en el muro
posibles_anchos_poster = getPosicionesFactibles(posters,ancho_muro,'ancho')
posibles_altos_poster = getPosicionesFactibles(posters,alto_muro,'alto')
# Minimos
minimos = findMinimun(posters)
presicion = 1 # cuanto mas alto mas dificil de resolver
ancho_min_poster = minimos[0]//presicion #minimo ancho
alto_min_poster = minimos[1]//presicion #minimo alto
