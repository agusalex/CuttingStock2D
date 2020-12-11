from lib import getXorYPosters,extractPosters, filterNonFittingPosters
ancho_muro = 240
alto_muro = 520
# POSTERS agregar vertical y horizontal. ((ancho, alto), cantidad)
raw_posters_cant = [((36,254),4),((254,36),4),((104,55),8),((55,104),8),((40,30),9),((30,40),9)]
posters_cant = filterNonFittingPosters(raw_posters_cant,ancho_muro,alto_muro)
posters = extractPosters(posters_cant)

anchos_posters = getXorYPosters(posters,ancho_muro,'ancho')
altos_posters = getXorYPosters(posters,alto_muro,'alto')
