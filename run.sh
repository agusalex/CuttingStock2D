#!/bin/bash
source venv/bin/activate
rm -f solution.last
POSTERS=$1
ANCHO=$2
ALTO=$3
#echo "POSTERS ${1} ANCHO ${2} ALTO ${3}"
python cuttingStock.py >> /dev/null
if test -f "solution.last"; then
    cat solution.last
fi