from lib import findMinimun,getCantPerCutHandV
ancho_muro = 240
alto_muro = 520
# POSTERS agregar siempre vertical y horizontal, siempre numero par
posters = [(254,36),(36, 254),(104,55),(55,104),(30,40),(40,30)]
cantidades = [4,8,9]
cantidadesXPoster = getCantPerCutHandV(cantidades,posters) #(cantidad,ancho*alto)
# Minimos
minimos = findMinimun(posters)
presicion = 1 # cuanto mas alto mas dificil de resolver
ancho_min_poster = minimos[0]//presicion #minimo ancho
alto_min_poster = minimos[1]//presicion #minimo alto