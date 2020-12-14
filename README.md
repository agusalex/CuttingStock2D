
# Cutting Stock 2D

![alt text](https://github.com/agusalex/CuttingStock2D/blob/main/out/demo.jpeg?raw=true)

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
    bash run.sh "36;254#4, 254;36#4, 104;55#8, 55;104#8, 40;30#9, 30;40#9" "520,286" "240,240" "100,70"
    


## Para la proxima ejecucion con Python
    source venv/bin/activate
## Docs
https://pypi.org/project/PySCIPOpt/
