import os

def filterNonFittingRectangles(non_filtered,max_width,max_height):
    filtered = []
    for tuple in non_filtered:
        if ((tuple[0][0]<=max_width) and (tuple[0][1] <= max_height)):
            filtered.append(tuple)
    return filtered

def parseRectanglesPlainTextInput(input):
    parsed_1 = input.replace(' ','').split(',')
    parsed = []
    for triple in parsed_1:
        splitted = triple.split('#')
        tuple = splitted[0].split(';')
        cant = splitted[1]
        width = tuple[0]
        height = tuple[1]
        parsed.append(((int(width),int(height)),int(cant)))

    return parsed   

def parseListPlainTextInput(input):
    parsed_1 = input.replace(' ','').split(',')
    parsed = []
    for item in parsed_1:
        parsed.append(int(item))
    return parsed          

anchos_muro = parseListPlainTextInput(os.getenv("ANCHO","520,286"))
altos_muro = parseListPlainTextInput(os.getenv("ALTO","240,240"))
verbose = False
threaded = True
max_threads = 2
costos_muro = parseListPlainTextInput(os.getenv("COSTO","100,70"))
# POSTERS agregar vertical y horizontal. Sintaxis =  ancho;alto#cantidad, ancho;alto#cantidad 
raw_posters_with_amount = parseRectanglesPlainTextInput(os.getenv("POSTERS","36;254#4, 254;36#4, 104;55#8, 55;104#8, 40;30#9, 30;40#9"))



