#!/bin/bash
source venv/bin/activate
rm -f solution.last
export POSTERS=$1
export ANCHO=$2
export ALTO=$3
export COSTO=$4
echo "POSTERS ${1} ANCHO ${2} ALTO ${3} COSTO ${4}"
python cuttingStock.py #>> /dev/null
#if test -f "solution.last"; then
#    cat solution.last
#fi
unset POSTERS
unset ANCHO
unset ALTO
unset COSTO