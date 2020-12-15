from lib import filterNonFittingRectangles, parseRectanglesPlainTextInput,parseListPlainTextInput
import os

anchos_muro = parseListPlainTextInput(os.getenv("ANCHO","240,240"))
altos_muro = parseListPlainTextInput(os.getenv("ALTO","520,286"))
verbose = False
threaded = False
max_threads = 2
costos_muro = parseListPlainTextInput(os.getenv("COSTO","100,70"))
raw_posters_with_amount = parseRectanglesPlainTextInput(os.getenv("POSTERS","36;254#20, 254;36#20"))#, 104;55#8, 55;104#8, 40;30#9, 30;40#9"))

# POSTERS agregar vertical y horizontal. Sintaxis =  ancho;alto#cantidad, ancho;alto#cantidad 

