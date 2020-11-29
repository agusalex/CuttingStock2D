
# Cutting Stock 2D

 - Paquetes requeridos(Si se ejecuta desde python):  
	 - matplotlib y numpy, el script en la seccion **Python** los instala y todo lo que se necesita para
   ejecutarse 

## Ubuntu 18/20
Descargar https://www.scipopt.org/download.php?fname=SCIPOptSuite-7.0.1-Linux.deb

**Python**

    sudo dpkg -i SCIPOptSuite-7.0.1-Linux.deb
    sudo apt-get install python3-pip python3-venv
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
    python cuttingStock.py
    


## Para la proxima ejecucion con Python
    source venv/bin/activate
## Docs
https://pypi.org/project/PySCIPOpt/
